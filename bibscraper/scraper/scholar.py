from scholarly import scholarly


class ScholarScraper:
    def __init__(self, user_id: str) -> None:
        self.author = scholarly.search_author_id(id=user_id, filled=True)

    def get_publications(self) -> list[dict]:
        return [pub["bib"] for pub in self.author["publications"] if "bib" in pub]
