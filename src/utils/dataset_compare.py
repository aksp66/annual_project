import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def _read(path: str) -> pd.DataFrame:
    if path.endswith('.parquet'):
        return pd.read_parquet(path)
    else:
        return pd.read_csv(path)


def summarize_df(df: pd.DataFrame) -> Dict[str, Any]:
    summary = {}
    summary['rows'] = int(df.shape[0])
    summary['cols'] = int(df.shape[1])
    summary['columns'] = list(df.columns)
    summary['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
    summary['missing'] = {col: int(df[col].isna().sum()) for col in df.columns}
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        desc = df[numeric_cols].describe().to_dict()
        summary['numeric_describe'] = desc
    else:
        summary['numeric_describe'] = {}
    return summary


def compare_datasets(path_a: str, path_b: str, sample_n: int = 1000) -> Dict[str, Any]:
    """Compare two datasets (CSV or Parquet) and return a JSON-friendly report.

    The report includes shapes, column differences, dtype differences,
    missing value counts, and simple numeric summaries.
    """
    a = _read(path_a)
    b = _read(path_b)

    report: Dict[str, Any] = {}
    report['a_path'] = path_a
    report['b_path'] = path_b
    report['a_summary'] = summarize_df(a)
    report['b_summary'] = summarize_df(b)

    cols_a = set(a.columns)
    cols_b = set(b.columns)
    report['columns_only_in_a'] = sorted(list(cols_a - cols_b))
    report['columns_only_in_b'] = sorted(list(cols_b - cols_a))
    report['common_columns'] = sorted(list(cols_a & cols_b))

    dtype_diffs = {}
    for col in report['common_columns']:
        da = str(a[col].dtype)
        db = str(b[col].dtype)
        if da != db:
            dtype_diffs[col] = {'a': da, 'b': db}
    report['dtype_differences'] = dtype_diffs

    # Missing value differences for common columns
    missing_diff = {}
    for col in report['common_columns']:
        ma = int(a[col].isna().sum())
        mb = int(b[col].isna().sum())
        if ma != mb:
            missing_diff[col] = {'a_missing': ma, 'b_missing': mb}
    report['missing_differences'] = missing_diff

    # For numeric common columns, compare basic statistics
    numeric_common = [c for c in report['common_columns'] if np.issubdtype(a[c].dtype, np.number) and np.issubdtype(b[c].dtype, np.number)]
    numeric_stats = {}
    for col in numeric_common:
        sa = a[col].dropna().astype(float)
        sb = b[col].dropna().astype(float)
        numeric_stats[col] = {
            'a_mean': float(sa.mean()) if len(sa) else None,
            'b_mean': float(sb.mean()) if len(sb) else None,
            'a_std': float(sa.std()) if len(sa) else None,
            'b_std': float(sb.std()) if len(sb) else None,
        }
    report['numeric_comparison'] = numeric_stats

    # Row-level comparison: sample hashes on common columns
    if len(report['common_columns']) > 0:
        cols = report['common_columns']
        try:
            ha = (a[cols].astype(str).fillna('')).apply(lambda row: '||'.join(row.values), axis=1)
            hb = (b[cols].astype(str).fillna('')).apply(lambda row: '||'.join(row.values), axis=1)
            set_a = set(ha.sample(n=min(len(ha), sample_n), random_state=0).tolist())
            set_b = set(hb.sample(n=min(len(hb), sample_n), random_state=0).tolist())
            report['sample_row_overlap'] = {
                'sample_size_a': min(len(ha), sample_n),
                'sample_size_b': min(len(hb), sample_n),
                'overlap_count': int(len(set_a & set_b)),
            }
        except Exception:
            report['sample_row_overlap'] = {'error': 'could not compute sample overlap'}

    return report


if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Compare two datasets and print a JSON report')
    parser.add_argument('a', help='Path to first dataset (CSV or Parquet)')
    parser.add_argument('b', help='Path to second dataset (CSV or Parquet)')
    parser.add_argument('--sample', type=int, default=1000, help='Number of rows to sample for overlap check')
    args = parser.parse_args()
    rep = compare_datasets(args.a, args.b, sample_n=args.sample)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
