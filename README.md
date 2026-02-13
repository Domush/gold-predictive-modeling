# Gold Futures Backtester Pro

A modern, elegant desktop application for backtesting predictive Python functions on historical gold futures prices.

## Features

- **Modern GUI**: Elegant dark-themed interface built with PySide6.
- **Real-time Visualization**: Dynamic charts using `pyqtgraph` that update as the backtest progresses.
- **Multi-Timeframe Support**: Backtest across 1m, 5m, 15m, 30m, 1h, and 1d timeframes simultaneously.
- **Integrated Code Editor**: Syntax-highlighted editor with validation and history tracking.
- **Multithreaded Engine**: High-performance backtesting that keeps the UI responsive.
- **Data Management**: Efficient loading of large CSV datasets with Feather format conversion for speed.
- **Customizable Logic**: User-defined success thresholds and auto-abort parameters.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gold-predictive-modeling.git
   cd gold-predictive-modeling
   ```

2. Install dependencies:
   ```bash
   pip install pyside6 pyqtgraph pandas numpy pygments feather-format
   ```

3. Ensure the data file exists at `data/XAU_1m_data.csv`.

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Select the desired timeframes in the sidebar.
3. Write or edit your predictive function in the editor. The function must follow the signature:
   ```python
   def predict(ohlcv_data):
       # ohlcv_data is a numpy array of the last 10 rows
       # returns a predicted price (float)
       pass
   ```
4. Click **Update / Validate** to check for syntax errors.
5. Click **Start Backtest** to begin.
6. Use the **Stop** button to halt a running backtest.

## UI Controls

- **Start Backtest**: Enabled only after successful code validation.
- **Stop**: Enabled only while a backtest is in progress.
- **Update / Validate**: Compiles the current code and saves it to history if changed.
- **Backtest History**: Click any revision to revert the editor to that version.

## Project Structure

- `main.py`: Main application entry point and UI logic.
- `data_engine.py`: Data loading and resampling engine.
- `highlighter.py`: Syntax highlighter for the code editor.
- `data/`: Directory for historical datasets.
