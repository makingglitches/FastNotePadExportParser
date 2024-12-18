
class SqlResult:
    def __init__(self, data=None, error=None):
        self.data = data
        self.error = error
        self.success = error is None

    def __repr__(self):
        return f"<SqlResult success={{self.success}}, data={{self.data}}, error={{self.error}}>"
    