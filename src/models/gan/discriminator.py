from torch import nn


class Discriminator(nn.Module):
    """Discriminateur DCGAN : image 32x32x1 -> logit (réel vs généré, avant sigmoïde)."""

    def __init__(self, base_channels: int = 64, in_channels: int = 1):
        super().__init__()
        self.net = nn.Sequential(
            # 32x32 -> 16x16 (pas de BatchNorm sur la première couche, cf. Radford et al. 2015)
            nn.Conv2d(in_channels, base_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # 16x16 -> 8x8
            nn.Conv2d(base_channels, base_channels * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(base_channels * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # 8x8 -> 4x4
            nn.Conv2d(base_channels * 2, base_channels * 4, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(base_channels * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # 4x4 -> 1x1 (logit)
            nn.Conv2d(base_channels * 4, 1, kernel_size=4, stride=1, padding=0, bias=False),
        )

    def forward(self, x):
        return self.net(x).view(-1, 1).squeeze(1)
