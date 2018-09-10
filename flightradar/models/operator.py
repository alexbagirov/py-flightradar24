class Operator:
    """Class for storing Operator info."""
    def __init__(self, label: str, iata: str, logo: str, name: str):
        self.label = label
        self.iata = iata
        self.logo = logo
        self.name = name

    def __str__(self) -> str:
        return self.label

    @staticmethod
    def create_from_search(label: str, detail: dict, name: str, **_):
        """Static method for Operator instance creation from search results."""
        return Operator(label, detail['iata'], detail['logo'], name)
