from django.core.exceptions import ValidationError

from pytest import raises

from genki.validators import hex_validator, discord_id_validator


def test_hex_validator():
    hex_validator('0000FF')
    with raises(ValidationError):
        hex_validator('Invali')
    with raises(ValidationError):
        hex_validator('0000FFFF')


def test_discord_id_validator():
    discord_id_validator('93043948775305216')
    discord_id_validator('93043948775305216123819')
    with raises(ValidationError):
        discord_id_validator('9304394877530521')
    with raises(ValidationError):
        discord_id_validator('93043948775abc216')
