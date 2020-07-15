from django.core.exceptions import ValidationError

from pytest import raises

from genki.validators import hex_validator


def test_hex_validator():
    hex_validator('0000FF')
    with raises(ValidationError):
        hex_validator('Invali')
    with raises(ValidationError):
        hex_validator('0000FFFF')
