from pathlib import Path

from src.data.dataset import get_dataloaders, load_config

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "data.yaml"


def test_dataloaders_shape_and_range():
    config = load_config(CONFIG_PATH)
    train_loader, val_loader, test_loader = get_dataloaders(config)

    batch_x, batch_y = next(iter(train_loader))
    assert batch_x.shape == (config["batch_size"], 1, config["image_size"], config["image_size"])
    assert batch_y.shape == (config["batch_size"],)

    # Normalisation (mean=0.5, std=0.5) -> pixels dans [-1, 1]
    assert batch_x.min() >= -1.0 - 1e-5
    assert batch_x.max() <= 1.0 + 1e-5


def test_train_val_split_sizes():
    config = load_config(CONFIG_PATH)
    train_loader, val_loader, test_loader = get_dataloaders(config)

    n_train = len(train_loader.dataset)
    n_val = len(val_loader.dataset)
    n_test = len(test_loader.dataset)

    assert n_train + n_val == 60000
    assert n_test == 10000
    assert n_val == int(60000 * config["val_split"])


def test_split_is_reproducible_with_seed():
    config = load_config(CONFIG_PATH)
    train_loader_a, _, _ = get_dataloaders(config)
    train_loader_b, _, _ = get_dataloaders(config)

    indices_a = list(train_loader_a.dataset.indices)
    indices_b = list(train_loader_b.dataset.indices)
    assert indices_a == indices_b
