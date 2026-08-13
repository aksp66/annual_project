#!/usr/bin/env python
"""Small wrapper script to compare two datasets using the project's utility."""
from src.utils.dataset_compare import compare_datasets
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Compare two datasets (CSV/Parquet)')
    parser.add_argument('a')
    parser.add_argument('b')
    parser.add_argument('--sample', type=int, default=1000)
    parser.add_argument('--out', help='Write JSON report to file')
    args = parser.parse_args()
    rep = compare_datasets(args.a, args.b, sample_n=args.sample)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(rep, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(rep, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
