from pathlib import Path

from django.core.files import File


def get_html_file() -> File:
    """
    Get a dummy ``File`` of a valid html file.

    :return: A dummy archive ``File``
    """
    file = Path(__file__).resolve().parents[0] / "fixtures" / "dummy_archive.html"
    return File(
        file=open(file),
        name=file.name
    )


__all__ = [
    'get_html_file'
]
