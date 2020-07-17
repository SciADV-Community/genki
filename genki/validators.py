from django.core.validators import RegexValidator


def hex_validator(colour: str):
    """
    Call :class:`~django.core.validators.RegexValidator`
    to validate a hex colour value.
    :param name: The colour to be validated.
    :raises ValidationError: If the colour is invalid.
    """
    RegexValidator(
        regex=r'^[A-Fa-f\d]{6}$',
        message='Invalid hex colour.',
        code='invalid_hex_colour'
    ).__call__(colour)


def discord_id_validator(_id: str):
    """
    Call :class:`~django.core.validators.RegexValidator`
    to validate a discord ID.
    :param name: The ID to be validated.
    :raises ValidationError: If the ID is invalid.
    """
    RegexValidator(
        regex=r'^\d{17,}$',
        message='Invalid Discord ID.',
        code='invalid_id_colour'
    ).__call__(_id)


__all__ = [
    'hex_validator', 'discord_id_validator'
]
