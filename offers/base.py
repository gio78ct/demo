class Source:
    name = "base"

    def available(self):
        return True

    def search(self, query, limit=50):
        raise NotImplementedError
