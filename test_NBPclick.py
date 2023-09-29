from NBPclick import validate_currency, check_currency_code_exists
import pytest


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
