"""Расчёты для учебного конвертера валют."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from types import MappingProxyType
from typing import Mapping


RATES_TO_RUB: Mapping[str, Decimal] = MappingProxyType(
    {
        "RUB": Decimal("1"),
        "USD": Decimal("82.50"),
        "EUR": Decimal("97.00"),
        "CNY": Decimal("11.50"),
    }
)


def convert_currency(
    amount: str | int | Decimal,
    source_currency: str,
    target_currency: str,
    rates: Mapping[str, Decimal] = RATES_TO_RUB,
) -> Decimal:
    """Конвертирует положительную сумму между двумя валютами.

    Args:
        amount: Сумма в исходной валюте.
        source_currency: Код исходной валюты.
        target_currency: Код целевой валюты.
        rates: Стоимость единицы каждой валюты в рублях.

    Returns:
        Сумма в целевой валюте, округлённая до копеек.

    Raises:
        TypeError: Сумма или коды валют имеют неподдерживаемый тип.
        ValueError: Сумма некорректна или код валюты неизвестен.
    """
    if isinstance(amount, bool) or not isinstance(amount, (str, int, Decimal)):
        raise TypeError("Сумма должна быть строкой, целым числом или Decimal")
    if not isinstance(source_currency, str) or not isinstance(target_currency, str):
        raise TypeError("Коды валют должны быть строками")

    normalized_amount = str(amount).strip().replace(",", ".")
    try:
        decimal_amount = Decimal(normalized_amount)
    except InvalidOperation as error:
        raise ValueError("Введите корректную сумму") from error

    if not decimal_amount.is_finite() or decimal_amount <= 0:
        raise ValueError("Сумма должна быть положительным конечным числом")

    source = source_currency.strip().upper()
    target = target_currency.strip().upper()
    if source not in rates or target not in rates:
        raise ValueError("Выбрана неизвестная валюта")

    converted = decimal_amount * rates[source] / rates[target]
    return converted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_amount(amount: Decimal) -> str:
    """Форматирует сумму с двумя знаками после запятой без экспоненты."""
    return format(amount, ".2f")
