import requests
from bs4 import BeautifulSoup
from services.network import NetworkService

network_service = NetworkService()


class DataScrapingService:
    def get_seo_data(self, soup):
        title = soup.select('title')
        data = {'title': title[0].getText() if title else ''}

        meta_description = soup.select('meta[name=description]')
        data['description'] = meta_description[0]['content'] if meta_description else ''

        for c1_data in soup.find_all('meta', content=True, property="og:locale"):
            data["language"] = c1_data['content']

        for c2_data in soup.find_all('meta', content=True, property="og:type"):
            data["type"] = c2_data['content']

        for c3_data in soup.find_all('meta', content=True, property="og:site_name"):
            data["site_name"] = c3_data['content']

        for c4_data in soup.find_all('meta', content=True, property="og:url"):
            data["site_url"] = c4_data['content']

        for c5_data in soup.find_all('meta', content=True, property="og:title"):
            data["site_title"] = c5_data['content']

        for c6_data in soup.find_all('meta', content=True, property="og:description"):
            data["site_description"] = c6_data['content']

        for c7_data in soup.find_all('meta', content=True, property="article:modified_time"):
            data["last_modified_time"] = c7_data['content']

        return data or {}
