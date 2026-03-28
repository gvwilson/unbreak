class QueryBuilder:
    def __init__(self):
        self.filters = []
        self.limit_val = None

    def filter(self, condition):
        self.filters.append(condition)
        # BUG: filter() modifies self but returns None implicitly;
        # BUG: chaining .limit() on None raises AttributeError

    def limit(self, n):
        self.limit_val = n
        return self

    def build(self):
        return {"filters": self.filters, "limit": self.limit_val}


query = QueryBuilder().filter("age > 18").limit(10).build()
print(query)
