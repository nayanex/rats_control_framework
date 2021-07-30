class ValuesMixin:
    """"A class which includes a method to return all "public" properties of the class."""

    @classmethod
    def values(cls) -> list:
        """"Returns all public properties of the class, except this method."""
        return [
            value
            for key, value in vars(cls).items()
            if not key.startswith("_") and key != "values"
        ]
