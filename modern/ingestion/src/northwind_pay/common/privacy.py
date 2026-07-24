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
DOCUMENT_TOKEN_PATTERN = re.compile(r"^doc_[0-9a-f]{24}$")
ACCOUNT_TOKEN_PATTERN = re.compile(r"^tedacct_[0-9a-f]{24}$")
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


def tokenize_document(
    document: str,
    *,
    key_variable: str = "NWP_DOCUMENT_TOKEN_KEY",
) -> str:
    """Return ``doc_`` plus the first 24 lowercase hex characters of the HMAC.

    One correlation scope covers both payer and payee documents, so the same
    party tokenizes identically on either side of an event.
    """

    if not document.isdigit() or len(document) not in {11, 14}:
        raise PrivacyError("document is not an eleven or fourteen digit identifier")
    digest = hmac.new(_key(key_variable), document.encode("ascii"), hashlib.sha256)
    token = f"doc_{digest.hexdigest()[:24]}"
    if not DOCUMENT_TOKEN_PATTERN.match(token):
        raise PrivacyError("derived document token does not match the contract")
    return token


def mask_document(document: str) -> str:
    """Mask by length: seven asterisks for a CPF, ten for a CNPJ."""

    if not document.isdigit() or len(document) not in {11, 14}:
        raise PrivacyError("document is not an eleven or fourteen digit identifier")
    stars = 7 if len(document) == 11 else 10
    return f"{'*' * stars}{document[-4:]}"


def tokenize_account(
    ispb: str,
    branch: str,
    account: str,
    *,
    key_variable: str = "NWP_TED_ACCOUNT_TOKEN_KEY",
) -> str:
    """Return ``tedacct_`` plus the first 24 hex characters of the HMAC.

    The contract's canonical input is ``ispb:branch:account``, so the same
    account number at two institutions tokenizes differently. Hashing the
    account alone would silently correlate unrelated parties.
    """

    if not account.isdigit() or len(account) != 12:
        raise PrivacyError("account number is not twelve digits")
    if not ispb.isdigit() or len(ispb) != 8:
        raise PrivacyError("institution code is not eight digits")
    if not branch.isdigit() or len(branch) != 4:
        raise PrivacyError("branch code is not four digits")
    canonical = f"{ispb}:{branch}:{account}"
    digest = hmac.new(_key(key_variable), canonical.encode("ascii"), hashlib.sha256)
    token = f"tedacct_{digest.hexdigest()[:24]}"
    if not ACCOUNT_TOKEN_PATTERN.match(token):
        raise PrivacyError("derived account token does not match the contract")
    return token


def tokenize_with_prefix(
    value: str,
    *,
    prefix: str,
    key_variable: str,
) -> str:
    """Return ``<prefix>_`` plus the first 24 lowercase hex characters of the HMAC.

    The shared shape for the several contract-approved tokenizations that differ
    only in prefix, key, and canonical input. Each keeps its own key so a token
    from one scope cannot be correlated with another.
    """

    if not value:
        raise PrivacyError("tokenization input is empty")
    digest = hmac.new(_key(key_variable), value.encode("ascii"), hashlib.sha256)
    token = f"{prefix}_{digest.hexdigest()[:24]}"
    if not re.match(rf"^{prefix}_[0-9a-f]{{24}}$", token):
        raise PrivacyError("derived token does not match the contract")
    return token
