class HttpUnauthorized(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class RecordNotFoundError(Exception):
    """Raise when record does not exist in DB"""
