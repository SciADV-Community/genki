import pytest
from django.db.models import Model
from django.core.exceptions import ValidationError

from genki.models import DiscordIDField, HexColourField


def test_colour():
    class DummyModel(Model):
        colour = HexColourField()

    # Valid Cases
    model = DummyModel(colour='0000FF')
    model.full_clean()

    # Invalid Cases
    model.colour = 'Invali'
    with pytest.raises(ValidationError):
        model.full_clean()
    model.colour = '000000FF'
    with pytest.raises(ValidationError):
        model.full_clean()


def test_discord():
    class DummyModel(Model):
        discordID = DiscordIDField()

    # Valid Cases
    model = DummyModel(discordID='93043948775305216')
    model.full_clean()
    model.discordID = '93043948775305216123819'
    model.full_clean()

    # Invalid Cases
    model.discordID = '9304394877530521'
    with pytest.raises(ValidationError):
        model.full_clean()
    model.discordID = '93043948775abc216'
    with pytest.raises(ValidationError):
        model.full_clean()
