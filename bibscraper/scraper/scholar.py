import logging
import time
from typing import Optional, Dict, Any
from scholarly import scholarly


logger = logging.getLogger(__name__)


class ScholarScraper:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.author: Optional[Dict[str, Any]] = None
        self._fetch_author_data()

    def _fetch_author_data(self, max_retries: int = 3, base_delay: float = 2.0) -> None:
        """
        Fetch author data with retry logic and exponential backoff.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
        """
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Attempting to fetch Google Scholar data for user {self.user_id} (attempt {attempt + 1}/{max_retries + 1})")
                self.author = scholarly.search_author_id(id=self.user_id, filled=True)
                logger.info("Successfully fetched Google Scholar data")
                return
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Attempt {attempt + 1} failed: {error_msg}")
                
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Failed to fetch Google Scholar data after {max_retries + 1} attempts")
                    raise ScholarFetchException(f"Unable to fetch Google Scholar data for user {self.user_id}: {error_msg}") from e

    def get_publications(self) -> list[dict]:
        """Get publications from the author data."""
        if not self.author or "publications" not in self.author:
            return []
        return [pub["bib"] for pub in self.author["publications"] if "bib" in pub]

    def get_citation_stats(self) -> Dict[str, Any]:
        """
        Get citation statistics from the author data.
        
        Returns:
            Dictionary with citation stats or empty dict if data unavailable
        """
        if not self.author:
            return {}
        
        return {
            "citedby": self.author.get("citedby", 0),
            "hindex": self.author.get("hindex", 0),
            "i10index": self.author.get("i10index", 0),
        }


class ScholarFetchException(Exception):
    """Exception raised when Google Scholar data cannot be fetched."""
    pass
