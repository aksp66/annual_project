import math

import torch
from torch import nn


class SinusoidalTimeEmbedding(nn.Module):
    """Embedding sinusoïdal du pas de temps t (cf. Vaswani et al. 2017 / Ho et al. 2020)."""

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        device = t.device
        half_dim = self.dim // 2
        freqs = torch.exp(-math.log(10000) * torch.arange(half_dim, device=device) / (half_dim - 1))
        args = t.float().unsqueeze(-1) * freqs.unsqueeze(0)
        return torch.cat([torch.sin(args), torch.cos(args)], dim=-1)


class ResidualBlock(nn.Module):
    """Bloc conv + injection de l'embedding temporel + connexion résiduelle."""

    def __init__(self, in_channels: int, out_channels: int, time_emb_dim: int, num_groups: int = 8):
        super().__init__()
        self.norm1 = nn.GroupNorm(num_groups, in_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.time_proj = nn.Linear(time_emb_dim, out_channels)
        self.norm2 = nn.GroupNorm(num_groups, out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.act = nn.SiLU()
        self.skip = (
            nn.Conv2d(in_channels, out_channels, kernel_size=1) if in_channels != out_channels else nn.Identity()
        )

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor) -> torch.Tensor:
        h = self.conv1(self.act(self.norm1(x)))
        h = h + self.time_proj(self.act(t_emb)).unsqueeze(-1).unsqueeze(-1)
        h = self.conv2(self.act(self.norm2(h)))
        return h + self.skip(x)


class Downsample(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, kernel_size=3, stride=2, padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class Upsample(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = nn.functional.interpolate(x, scale_factor=2, mode="nearest")
        return self.conv(x)


class UNet(nn.Module):
    """Petit U-Net de débruitage : prédit le bruit ajouté à x_t sachant t.

    Architecture from scratch : blocs résiduels + embedding temporel sinusoïdal,
    downsampling/upsampling avec skip connections (pas d'attention, pour rester
    entraînable sur CPU — cf. HISTORY.md).
    """

    def __init__(
        self,
        in_channels: int = 1,
        base_channels: int = 32,
        channel_mults: tuple[int, ...] = (1, 2, 4),
        num_res_blocks: int = 2,
    ):
        super().__init__()
        time_emb_dim = base_channels * 4

        self.time_embed = nn.Sequential(
            SinusoidalTimeEmbedding(base_channels),
            nn.Linear(base_channels, time_emb_dim),
            nn.SiLU(),
            nn.Linear(time_emb_dim, time_emb_dim),
        )

        self.init_conv = nn.Conv2d(in_channels, base_channels, kernel_size=3, padding=1)

        channels = [base_channels * m for m in channel_mults]

        # Down path
        self.down_blocks = nn.ModuleList()
        self.downsamples = nn.ModuleList()
        skip_channels = [base_channels]
        cur_ch = base_channels
        for i, ch in enumerate(channels):
            level_blocks = nn.ModuleList()
            for _ in range(num_res_blocks):
                level_blocks.append(ResidualBlock(cur_ch, ch, time_emb_dim))
                cur_ch = ch
                skip_channels.append(cur_ch)
            self.down_blocks.append(level_blocks)
            if i < len(channels) - 1:
                self.downsamples.append(Downsample(cur_ch))
                skip_channels.append(cur_ch)
            else:
                self.downsamples.append(None)

        # Bottleneck
        self.mid_block1 = ResidualBlock(cur_ch, cur_ch, time_emb_dim)
        self.mid_block2 = ResidualBlock(cur_ch, cur_ch, time_emb_dim)

        # Up path (mirror)
        self.up_blocks = nn.ModuleList()
        self.upsamples = nn.ModuleList()
        for i, ch in reversed(list(enumerate(channels))):
            level_blocks = nn.ModuleList()
            for _ in range(num_res_blocks + 1):
                level_blocks.append(ResidualBlock(cur_ch + skip_channels.pop(), ch, time_emb_dim))
                cur_ch = ch
            self.up_blocks.append(level_blocks)
            if i > 0:
                self.upsamples.append(Upsample(cur_ch))
            else:
                self.upsamples.append(None)

        self.out_norm = nn.GroupNorm(8, cur_ch)
        self.out_act = nn.SiLU()
        self.out_conv = nn.Conv2d(cur_ch, in_channels, kernel_size=3, padding=1)

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        t_emb = self.time_embed(t)
        h = self.init_conv(x)
        skips = [h]

        for level_blocks, downsample in zip(self.down_blocks, self.downsamples):
            for block in level_blocks:
                h = block(h, t_emb)
                skips.append(h)
            if downsample is not None:
                h = downsample(h)
                skips.append(h)

        h = self.mid_block1(h, t_emb)
        h = self.mid_block2(h, t_emb)

        for level_blocks, upsample in zip(self.up_blocks, self.upsamples):
            for block in level_blocks:
                h = block(torch.cat([h, skips.pop()], dim=1), t_emb)
            if upsample is not None:
                h = upsample(h)

        return self.out_conv(self.out_act(self.out_norm(h)))
