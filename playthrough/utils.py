from html.parser import HTMLParser
from typing import Set
from playthrough.models import Archive


def get_users_in_archive(archive: Archive) -> Set[str]:
    """Index the users in the file of an archive.

    :param archive: the `playthrough.models.Archive` to index.
    :return: List of user IDs found in the archive.
    """
    if not archive.file:
        return list()

    class UserIndexParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "span":
                for attr in attrs:
                    if attr[0] == "data-user-id":
                        users.add(attr[1])

        def handle_endtag(self, tag):
            pass

        def handle_data(self, data):
            pass
    users = set()
    archive.file.open(mode='r')
    parser = UserIndexParser()
    parser.feed(archive.file.read())
    archive.file.close()
    return users
