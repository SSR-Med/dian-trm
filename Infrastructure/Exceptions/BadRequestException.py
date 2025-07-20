class BadRequestException(Exception):
    def __init__(self, message: str = "Bad Request", detail: dict = None):
        self.message = message
        self.detail = detail if detail is not None else {"error": message}
        super().__init__(self.message)