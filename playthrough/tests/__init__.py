from pytest import mark

from genki.tests.base import GenkiTestBase


@mark.usefixtures('django_db_setup')
class PlaythroughTestBase(GenkiTestBase):
    pass
