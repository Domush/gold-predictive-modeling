import sys
from pathlib import Path

import pandas as pd

VALID_TIMEFRAMES = {
    '1m': '1min',
    '1min': '1min',
    '5m': '5min',
    '5min': '5min',
    '15m': '15min',
    '15min': '15min',
    '30m': '30min',
    '30min': '30min',
    '1h': '1h',
    '1d': '1d',
    '1w': 'W',
    '1m': 'M',
}

FEATHER_FILENAME = 'XAU_1m_data.feather'
DATA_DIR = Path(__file__).resolve().parent / 'data'
FEATHER_PATH = DATA_DIR / FEATHER_FILENAME


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Feather file not found: {path}")

    df = pd.read_feather(path)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
    elif not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError('Feather file does not contain a Date column or datetime index.')

    return df


def resample_data(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    tf = VALID_TIMEFRAMES.get(timeframe.lower())
    if tf is None:
        raise ValueError(f"Unsupported timeframe '{timeframe}'. Valid options: {', '.join(sorted(VALID_TIMEFRAMES))}")

    if tf == '1min':
        return df

    agg = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
    }
    resampled = df.resample(tf).agg(agg).dropna()
    return resampled


def get_last_30_closes(timeframe: str) -> pd.Series:
    df = load_data(FEATHER_PATH)
    sampled = resample_data(df, timeframe)
    return sampled['Close'].tail(30)


def main() -> int:
    print('Available timeframes: 1m, 5m, 15m, 30m, 1h, 1d, 1w, 1m')
    timeframe = input('Enter timeframe: ').strip()
    try:
        closes = get_last_30_closes(timeframe)
    except Exception as exc:
        print(f'Error: {exc}')
        return 1

    if closes.empty:
        print('No closing data available for the selected timeframe.')
        return 1

    rounded_closes = [round(float(value), 2) for value in closes.tolist()]
    print(f'Last {len(rounded_closes)} closes for {timeframe}:')
    print(rounded_closes)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
