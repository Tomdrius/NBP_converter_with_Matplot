from NBPtk import validate_currency, check_currency_code_exists, validate_date, get_exchange_rate, extract_currency_rates
import pytest, requests, json
from datetime import datetime


def test_4_letters():
    currency = "ASDF"
    with pytest.raises(ValueError) as e:
        validate_currency(currency)
    assert "Invalid currency format. Please provide a 3-letter currency code." in str(e.value)
    assert e.type == ValueError

def test_2_letters():
    currency = "DF"
    with pytest.raises(ValueError) as e:
        validate_currency(currency)
    assert "Invalid currency format. Please provide a 3-letter currency code." in str(e.value)
    assert e.type == ValueError

def test_3_letters():
    currency = "ASF"
    got = validate_currency(currency)
    expected = None
    assert got == expected

def test_numbers():
    currency = "123"
    with pytest.raises(ValueError) as e:
        validate_currency(currency)
    assert "Invalid currency format. Please provide a 3-letter currency code." in str(e.value)
    assert e.type == ValueError

def test_special_signs():
    currency = "?!@"
    with pytest.raises(ValueError) as e:
        validate_currency(currency)
    assert "Invalid currency format. Please provide a 3-letter currency code." in str(e.value)
    assert e.type == ValueError

def test_check_currency_code_exists(tmpdir):
    with tmpdir.as_cwd():
        with open('currency_codes.txt', 'w') as file:
            file.write("USD\nEUR\nJPY")
        expected = ["USD", "EUR", "JPY"]
        got = check_currency_code_exists()
        assert got == expected

def test_too_old_date():
    input_date_start = "2000-10-02"
    input_date_end = "2000-10-02"
    with pytest.raises(ValueError) as e:
        validate_date(input_date_start, input_date_end)
    assert "Invalid year. Please provide a year after 2001." in str(e.value)
    assert e.type == ValueError

def test_future_date():
    input_date_start = "2012-10-02"
    input_date_end = "2033-10-02"
    with pytest.raises(ValueError) as e:
        validate_date(input_date_start, input_date_end)
    assert "Invalid date. Please provide a date in the past." in str(e.value)
    assert e.type == ValueError

def test_today_date():
    input_date_start = "2023-09-29"
    input_date_end = "2023-09-29"
    got = validate_date(input_date_start, input_date_end)
    expected = "2023-09-29", "2023-09-29"
    assert got == expected

def test_wrong_format_date():
    input_date_start = "201210-2"
    input_date_end = "2033-10-02"
    with pytest.raises(ValueError) as e:
        validate_date(input_date_start, input_date_end)
    assert "Invalid date format. Please provide the date in YYYY-MM-DD format." in str(e.value)
    assert e.type == ValueError


@pytest.mark.parametrize("input_date_start, input_date_end, expected",
                         [("2023-09-28", "2023-09-29", ("2023-09-28", "2023-09-29")),
                          ("2023-02-11", "2023-09-30", ("2023-02-11", "2023-09-30")),
                          ("2002-01-01", "2002-06-13", ("2002-01-01", "2002-06-13")),
                          ("2012-02-29", "2022-09-29", ("2012-02-29", "2022-09-29")),
                          ("2013-02-28", "2013-09-28", ("2013-02-28", "2013-09-28")),
                          ("2022-12-24", "2022-12-31", ("2022-12-24", "2022-12-31")),
                         ])
def test_correct_date(input_date_start, input_date_end, expected):
    got = validate_date(input_date_start, input_date_end)
    assert got == expected


def test_wrong_format_date_with_letters():
    input_date_start = "2033-10-02"
    input_date_end = "adbasdf"
    with pytest.raises(ValueError) as e:
        validate_date(input_date_start, input_date_end)
    assert "Invalid date format. Please provide the date in YYYY-MM-DD format." in str(e.value)
    assert e.type == ValueError

def test_correct_inputs():
    url = "http://api.nbp.pl/api/exchangerates/rates/a/gbp/2012-01-01/2012-01-31/?format=json"
    got = get_exchange_rate("GBP", "2012-01-01", "2012-01-31")
    expected = requests.get(url).json()
    assert got == expected

def test_weekends_dates():
    with pytest.raises(ValueError) as e:
        get_exchange_rate(1, 2, 3)
    assert "No data. You probably chose a day off." in str(e.value)
    assert e.type == ValueError


@pytest.mark.parametrize("valid_resp, expected",[
    ({"rates": [{"mid": 3.5}, {"mid": 4.0}]}, [3.5, 4.0]),
     ({"rates": [{"mid": 0.1}, {"mid": 10.2}]}, [0.1, 10.2]),
     ({"rates": [{"mid": 0.0}, {"mid": 7.7}]}, [0.0, 7.7]),
     ({"rates": [{"mid": -1.0}, {"mid": 7.7}]}, [-1.0, 7.7]),
     ({"rates": [{"mid": 200.2}, {"mid": 337.7}]}, [200.2, 337.7]),
    ])
def test_extract_currency_with_valid_data(valid_resp, expected):
    got = extract_currency_rates(valid_resp)
    assert got == expected


def test_extract_currency_with_empty_rates():
    empty_resp = {"rates": []}
    expected = []
    got = extract_currency_rates(empty_resp)
    assert got == expected

def test_extract_currency_no_data():
    with pytest.raises(KeyError) as e:
        invalid_resp = {}
        extract_currency_rates(invalid_resp)
    assert "Empty key" in str(e.value)

def test_extract_currency_rates_wrong_data():
    with pytest.raises(TypeError) as e:
        invalid_resp = {"rates": "invalid_data"}
        extract_currency_rates(invalid_resp)
    assert "Invalid data" in str(e.value)
