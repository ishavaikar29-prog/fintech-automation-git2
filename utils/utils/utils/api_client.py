import logging
import requests
from utils.utils import retry
from utils.error_handler import log_error, log_info

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, headers=None, timeout=20):
        self.headers = headers or {}
        self.timeout = timeout

    @retry(tries=4, delay=2, backoff=2, allowed_exceptions=(Exception,), logger=logging.getLogger("api_client"))
    def fetch(self, url):
        try:
            log_info(f"Fetching URL: {url}")
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, list) else [data]
        except Exception as e:
            log_error(f"API fetch failed for {url}", e)
            raise
