from torch import nn


class Generator(nn.Module):
    """Générateur DCGAN : z (latent_dim, 1, 1) -> image 32x32x1 dans [-1, 1]."""

    def __init__(self, latent_dim: int = 100, base_channels: int = 64, out_channels: int = 1):
        super().__init__()
        self.net = nn.Sequential(
            # z -> 4x4
            nn.ConvTranspose2d(latent_dim, base_channels * 4, kernel_size=4, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(base_channels * 4),
            nn.ReLU(inplace=True),
            # 4x4 -> 8x8
            nn.ConvTranspose2d(base_channels * 4, base_channels * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(base_channels * 2),
            nn.ReLU(inplace=True),
            # 8x8 -> 16x16
            nn.ConvTranspose2d(base_channels * 2, base_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(base_channels),
            nn.ReLU(inplace=True),
            # 16x16 -> 32x32
            nn.ConvTranspose2d(base_channels, out_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.Tanh(),
        )

    def forward(self, z):
        return self.net(z)
