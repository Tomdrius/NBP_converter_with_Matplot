# NBP Currency Exchange Rates

This Python application allows you to fetch and display currency exchange rates from the National Bank of Poland (NBP).
The script allows to select two currencies and a date range. It will retrieve and display the exchange rates for those currencies over the specified time period. It also has the capability to plot the data using Matplotlib.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

---

## Requirements

- Python 3.x
- Libraries specified in `requirements.txt`

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment: `python -m venv venv`.
4. Activate the virtual environment:

   - **Windows**: `venv\Scripts\activate`
   - **Linux/macOS**: `source venv/bin/activate`

5. Install the required libraries: `pip install -r requirements.txt`.

## Usage

1. Run the program: `python main.py`.
2. The GUI window will open.
3. Provide the necessary information:
   - Currency (default: USD)
   - Start date (default: 7 days ago)
   - End date (default: today)
4. Click the "Show" button to retrieve and display the exchange rates.

## Configuration

You can modify the default currency and date range by changing the values in the `main.py` file.

```python
DEFAULT_CURRENCY = "USD"
DATA_FORMAT = "%Y-%m-%d"

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
