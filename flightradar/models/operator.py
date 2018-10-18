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
    def create_from_search(detail: dict, **kwargs):
        """Static method for Operator instance creation from search results."""
        return Operator(kwargs['res_label'], detail['iata'], detail['logo'],
                        kwargs['res_name'])
