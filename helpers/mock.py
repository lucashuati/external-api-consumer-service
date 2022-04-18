class MockResponse:
    def __init__(self, data=None):
        self.data = data or []

    def json(self):
        return self.data


class MockRequest:
    pass
