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

    def get_whois_data(self, url):
        domain_name = self.get_domain_name(url)
        request_url = self.WHOIS_URL + domain_name
        try:
            response = requests.get(request_url, timeout=5)
            if response.status_code != 200:
                return self.get_request_error_msg()

            bs4_soup = BeautifulSoup(response.text, 'lxml')
            whois_data = bs4_soup.find(
                'pre').text if bs4_soup.find('pre') else ''
            whois_data = whois_data.splitlines()
            whois_data = [x.split(':') for x in whois_data]
            whois_data = [x for x in whois_data if len(
                x) == 2 and x[0] != '']
            whois_data = {x[0].strip(): x[1].strip() for x in whois_data}
            return whois_data
        except requests.exceptions.RequestException:
            return self.get_request_error_msg()

    def get_data(self, url):
        data = {'whois_info': self.get_whois_data(url)}
        data['network_info'] = self.get_network_info(url)
        return data or self.get_request_error_msg()

    def get_request_error_msg(self):
        return {
            'status': 'error',
            'message': 'Error in getting network information'
        }