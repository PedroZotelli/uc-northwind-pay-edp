"""Brazilian document validation and contract-approved masking.

Mod-11 check-digit validation is implemented from the contract's own rules. A
document is validated *before* it is masked: masking an invalid identifier
would launder bad data into a well-formed output.
"""

from __future__ import annotations

CNPJ_LENGTH = 14
CPF_LENGTH = 11

CNPJ_WEIGHTS_FIRST = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
CNPJ_WEIGHTS_SECOND = (6, *CNPJ_WEIGHTS_FIRST)


class DocumentError(ValueError):
    """A document identifier is not valid under its contract.

    Messages never carry the value; the privacy contracts prohibit restricted
    identifiers in error messages.
    """


def _mod11_digit(digits: str, weights: tuple[int, ...]) -> int:
    total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def validate_cnpj(value: str) -> str:
    """Validate a 14-digit CNPJ, including both Mod-11 check digits."""

    if len(value) != CNPJ_LENGTH or not value.isdigit():
        raise DocumentError("CNPJ is not fourteen digits")
    if len(set(value)) == 1:
        raise DocumentError("CNPJ is a repeated digit")
    if _mod11_digit(value[:12], CNPJ_WEIGHTS_FIRST) != int(value[12]):
        raise DocumentError("CNPJ first check digit is wrong")
    if _mod11_digit(value[:13], CNPJ_WEIGHTS_SECOND) != int(value[13]):
        raise DocumentError("CNPJ second check digit is wrong")
    return value


def validate_cpf(value: str) -> str:
    """Validate an 11-digit CPF, including both Mod-11 check digits."""

    if len(value) != CPF_LENGTH or not value.isdigit():
        raise DocumentError("CPF is not eleven digits")
    if len(set(value)) == 1:
        raise DocumentError("CPF is a repeated digit")
    for length in (9, 10):
        weights = tuple(range(length + 1, 1, -1))
        if _mod11_digit(value[:length], weights) != int(value[length]):
            raise DocumentError("CPF check digit is wrong")
    return value


def mask_cnpj(value: str) -> str:
    """Return ten asterisks followed by the last four digits."""

    validate_cnpj(value)
    return f"{'*' * 10}{value[-4:]}"
