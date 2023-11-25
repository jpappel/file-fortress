import magic


def get_mime_type(file_head: bytes) -> str:
    """
    Checks bytes to determine its MIME type
    """
    return magic.from_buffer(file_head, mime=True)
