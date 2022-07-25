"""Custom form fields."""

from django.db.models import CharField

from genki import validators


class DiscordIDField(CharField):
    """A :class:`~django.forms.CharField` for Discord IDs."""

    default_validators = (validators.discord_id_validator,)

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 32
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs


class HexColourField(CharField):
    """A :class:`~django.forms.CharField` for Hex Colours."""

    default_validators = (validators.hex_validator,)

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs


__all__ = ["DiscordIDField", "HexColourField"]
