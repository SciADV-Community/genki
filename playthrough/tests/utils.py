from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile


def get_xml_file() -> InMemoryUploadedFile:
    """
    Get a dummy ``InMemoryUploadedFile`` of a valid xml file.

    :return: A dummy ``InMemoryUploadedFile``
    """
    file = BytesIO()
    # TODO: Add data here
    file.seek(0)
    return InMemoryUploadedFile(
        file, None, 'file.xml', 'application/xml', len(file.getvalue()), None
    )


__all__ = [
    'get_xml_file'
]
