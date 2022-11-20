from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class NetworkService:
    SERVICE_URL = 'http://ip-api.com/json/'

    WHOIS_URL = 'https://www.whois.com/whois/'

    def get_domain_name(self, url):
        return urlparse(url).netloc

    def get_network_info(self, url):
        request_url = self.SERVICE_URL + self.get_domain_name(url)
        try:
            response = requests.get(request_url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return self.get_request_error_msg()
        except requests.exceptions.RequestException:
            return self.get_request_error_msg()
