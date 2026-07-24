"""Exact money and COBOL overpunch decoding.

Independent of the legacy Java implementation: the rules come from
``contracts/types/01-card-settlement/layout.yaml``, not from Java source. Every
amount is a ``Decimal`` with exactly two fractional digits; binary floating
point never touches a monetary value.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

POSITIVE_CHARACTERS = "{ABCDEFGHI"
NEGATIVE_CHARACTERS = "}JKLMNOPQR"
SCALE = 2


class MoneyError(ValueError):
    """A monetary field is not representable under the contract."""


def decode_overpunch(encoded: str, *, scale: int = SCALE) -> Decimal:
    """Decode one signed-overpunch field into an exact Decimal.

    The final character carries both the last digit and the sign, indexed zero
    through nine in the positive and negative strings.
    """

    if not encoded:
        raise MoneyError("overpunch field is empty")
    digits, sign_character = encoded[:-1], encoded[-1]
    if digits and not digits.isdigit():
        raise MoneyError("overpunch field has a non-digit body")

    if sign_character.isdigit():
        # A trailing plain digit is not a valid overpunch encoding under this
        # contract; the sign must always be carried.
        raise MoneyError("overpunch field does not carry a sign")
    if sign_character in POSITIVE_CHARACTERS:
        last, negative = POSITIVE_CHARACTERS.index(sign_character), False
    elif sign_character in NEGATIVE_CHARACTERS:
        last, negative = NEGATIVE_CHARACTERS.index(sign_character), True
    else:
        raise MoneyError("overpunch sign character is not in the contract")

    try:
        unscaled = Decimal(f"{digits}{last}")
    except InvalidOperation as exc:
        raise MoneyError("overpunch field is not numeric") from exc
    value = unscaled.scaleb(-scale)
    return -value if negative else value


def quantized(value: Decimal, *, scale: int = SCALE) -> Decimal:
    """Return the value at exact contract scale, refusing any rounding."""

    exponent = Decimal(1).scaleb(-scale)
    if value != value.quantize(exponent):
        raise MoneyError("monetary value does not fit the contract scale")
    return value.quantize(exponent)


def render(value: Decimal, *, scale: int = SCALE) -> str:
    """Render money as canonical scale-two text, matching the CSV contract."""

    return f"{quantized(value, scale=scale):.{scale}f}"


def parse_unsigned(digits: str) -> int:
    """Parse a zero-padded unsigned integer field."""

    if not digits.isdigit():
        raise MoneyError("unsigned integer field has a non-digit character")
    return int(digits)
