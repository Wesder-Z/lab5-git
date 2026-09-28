"""Тесты расчётов конвертера валют."""

import unittest
from decimal import Decimal

from currency import RATES_TO_RUB, convert_currency, format_amount


class CurrencyConversionTests(unittest.TestCase):
    """Проверяет конвертацию и обработку ошибочных данных."""

    def test_converts_dollars_to_rubles(self) -> None:
        self.assertEqual(convert_currency("100", "USD", "RUB"), Decimal("8250.00"))

    def test_converts_between_foreign_currencies(self) -> None:
        self.assertEqual(convert_currency("97", "EUR", "USD"), Decimal("114.05"))

    def test_accepts_decimal_comma(self) -> None:
        self.assertEqual(convert_currency("82,50", "RUB", "USD"), Decimal("1.00"))

    def test_normalizes_currency_codes(self) -> None:
        self.assertEqual(convert_currency(10, " rub ", "rub"), Decimal("10.00"))

    def test_rejects_non_numeric_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "корректную сумму"):
            convert_currency("десять", "RUB", "USD")

    def test_rejects_non_positive_amounts(self) -> None:
        for amount in ("0", "-1"):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError, "положительным"):
                    convert_currency(amount, "RUB", "USD")

    def test_rejects_non_finite_amounts(self) -> None:
        for amount in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError, "конечным"):
                    convert_currency(amount, "RUB", "USD")

    def test_rejects_unknown_currency(self) -> None:
        with self.assertRaisesRegex(ValueError, "неизвестная валюта"):
            convert_currency("100", "GBP", "RUB")

    def test_rejects_bool_and_float_amounts(self) -> None:
        for amount in (True, 10.5):
            with self.subTest(amount=amount):
                with self.assertRaises(TypeError):
                    convert_currency(amount, "RUB", "USD")

    def test_rejects_non_string_currency_code(self) -> None:
        with self.assertRaisesRegex(TypeError, "Коды валют"):
            convert_currency("100", 1, "RUB")  # type: ignore[arg-type]

    def test_rates_cannot_be_changed(self) -> None:
        with self.assertRaises(TypeError):
            RATES_TO_RUB["USD"] = Decimal("1")  # type: ignore[index]

    def test_formats_large_amount_without_exponent(self) -> None:
        self.assertEqual(format_amount(Decimal("1234567.89")), "1234567.89")


if __name__ == "__main__":
    unittest.main()
