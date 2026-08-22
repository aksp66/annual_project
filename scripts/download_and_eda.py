#!/usr/bin/env python
"""Download Fashion-MNIST and CIFAR-10, run basic EDA, save JSON report and sample images."""
import os
import json
from pathlib import Path

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def run():
    try:
        import torch
        from torchvision import datasets
        from torchvision.transforms import ToPILImage
        import numpy as np
    except Exception as e:
        print('Required packages missing:', e)
        print('Please install torch and torchvision (see requirements.txt)')
        raise

    root = Path('data') / 'raw'
    ensure_dir(root)

    reports_dir = Path('reports')
    ensure_dir(reports_dir)
    samples_dir = reports_dir / 'samples'
    ensure_dir(samples_dir)

    results = {}

    def summarize_dataset(ds):
        info = {}
        data = np.array(ds.data) if hasattr(ds, 'data') else None
        targets = np.array(ds.targets) if hasattr(ds, 'targets') else None
        if data is not None:
            info['shape'] = list(data.shape)
            info['dtype'] = str(data.dtype)
        if targets is not None:
            uniques, counts = np.unique(targets, return_counts=True)
            info['n_classes'] = int(len(uniques))
            info['class_counts'] = {int(u): int(c) for u, c in zip(uniques, counts)}
        return info

    # Fashion-MNIST
    print('Downloading Fashion-MNIST...')
    fm_train = datasets.FashionMNIST(root=str(root), train=True, download=True)
    fm_test = datasets.FashionMNIST(root=str(root), train=False, download=True)
    print('Downloaded Fashion-MNIST')

    results['fashion_mnist'] = {
        'train': summarize_dataset(fm_train),
        'test': summarize_dataset(fm_test),
    }

    # Save sample images
    pil = ToPILImage()
    fm_sample_dir = samples_dir / 'fashion_mnist'
    ensure_dir(fm_sample_dir)
    for i in range(min(9, len(fm_train))):
        img, target = fm_train[i]
        if not hasattr(img, 'save'):
            img = pil(torch.tensor(img).unsqueeze(0).float())
        img.save(fm_sample_dir / f'sample_{i}_class_{target}.png')

    # CIFAR-10
    print('Downloading CIFAR-10...')
    cif_train = datasets.CIFAR10(root=str(root), train=True, download=True)
    cif_test = datasets.CIFAR10(root=str(root), train=False, download=True)
    print('Downloaded CIFAR-10')

    results['cifar10'] = {
        'train': summarize_dataset(cif_train),
        'test': summarize_dataset(cif_test),
    }

    cif_sample_dir = samples_dir / 'cifar10'
    ensure_dir(cif_sample_dir)
    # CIFAR train data stored as ds.data (numpy H x W x C)
    for i in range(min(9, len(cif_train))):
        img, target = cif_train[i]
        if hasattr(img, 'save'):
            img.save(cif_sample_dir / f'sample_{i}_class_{target}.png')
        else:
            try:
                from PIL import Image
                Image.fromarray(img).save(cif_sample_dir / f'sample_{i}_class_{target}.png')
            except Exception as e:
                print(f'Warning: could not save CIFAR-10 sample {i} (class {target}):', e)

    # Disk usage: estimate sizes of dataset folders
    def folder_size(path: Path):
        total = 0
        for p in path.rglob('*'):
            if p.is_file():
                try:
                    total += p.stat().st_size
                except Exception:
                    pass
        return total

    results['disk_usage_bytes'] = {
        'data_raw': folder_size(Path('data') / 'raw'),
        'reports_samples': folder_size(samples_dir),
    }

    out = reports_dir / 'datasets_report.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print('EDA complete. Report saved to', out)


if __name__ == '__main__':
    run()
