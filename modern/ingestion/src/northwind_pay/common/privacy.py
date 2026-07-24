"""Contract-approved privacy transformations.

Implemented from ``contracts/types/01-card-settlement/privacy.yaml``: HMAC-SHA-256
tokenization for the PAN, last-four retention, and CPF masking. The key is read
from the environment and a missing key fails closed, exactly as the contract's
``missing_key_behavior`` requires.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re

TOKEN_PATTERN = re.compile(r"^tok_[0-9a-f]{24}$")
MASKED_CPF_PATTERN = re.compile(r"^\*{7}[0-9]{4}$")


class PrivacyError(ValueError):
    """A privacy transformation cannot be performed safely."""

    def __init__(self, message: str) -> None:
        # Messages never carry the value being transformed; the contract
        # prohibits PAN and CPF in error messages.
        super().__init__(message)


def _key(variable: str) -> bytes:
    value = os.environ.get(variable)
    if not value:
        raise PrivacyError(f"tokenization key is not configured: {variable}")
    return value.encode("utf-8")


def tokenize_pan(pan: str, *, key_variable: str = "NWP_TOKENIZATION_KEY") -> str:
    """Return ``tok_`` plus the first 24 lowercase hex characters of the HMAC."""

    if not pan.isdigit() or len(pan) != 16:
        raise PrivacyError("PAN is not sixteen digits")
    digest = hmac.new(_key(key_variable), pan.encode("ascii"), hashlib.sha256)
    token = f"tok_{digest.hexdigest()[:24]}"
    if not TOKEN_PATTERN.match(token):
        raise PrivacyError("derived card token does not match the contract")
    return token


def pan_last4(pan: str) -> str:
    if not pan.isdigit() or len(pan) != 16:
        raise PrivacyError("PAN is not sixteen digits")
    return pan[-4:]


def mask_cpf(cpf: str) -> str:
    """Return seven asterisks followed by the last four digits."""

    if not cpf.isdigit() or len(cpf) != 11:
        raise PrivacyError("CPF is not eleven digits")
    masked = f"{'*' * 7}{cpf[-4:]}"
    if not MASKED_CPF_PATTERN.match(masked):
        raise PrivacyError("derived masked CPF does not match the contract")
    return masked


def assert_no_restricted_values(payload: str, restricted: tuple[str, ...]) -> None:
    """Refuse if any restricted value survived into a candidate output.

    Scanning the complete candidate before publication mirrors the legacy
    privacy boundary: nothing partial is published and nothing is redacted
    after the fact.
    """

    for value in restricted:
        if value and value in payload:
            raise PrivacyError(
                "a restricted value reached a candidate sanitized output"
            )
