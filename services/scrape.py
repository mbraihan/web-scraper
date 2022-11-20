import contextlib
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

    def get_p_h_tag_data(self, soup):
        available_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

        null_values = ['null', 'Null', 'NULL', 'none',
                    'None', 'NONE', 'nil', 'Nil', 'NIL', '']
        data = {tag: [tag_data.text.strip() for tag_data in soup.find_all(tag) if tag_data.text.strip() not in null_values] for tag in available_tags}

        return data or {}

    def get_links(self, soup, url):
        data = {}
        link_count = 1
        url = url = f'https://{network_service.get_domain_name(url)}'
        with contextlib.suppress(Exception):
            for link in soup.find_all('a', href=True):
                if '#' in link['href']:
                    continue
                elif '/' in link['href'][0]:
                    c_url = url + link['href']
                    variable = f'link-{str(link_count)}'
                    link_count += 1
                    data[variable] = str(c_url) + link['href']
                else:
                    variable = f'link-{str(link_count)}'
                    link_count += 1
                    data[variable] = link['href']
        return data or {}

    def get_image_data(self, soup, url):
        data = {}
        image_count = 1
        url = f'https://{network_service.get_domain_name(url)}'
        with contextlib.suppress(KeyError):
            for link in soup.find_all('img'):
                if '/' in link['src'][0]:
                    if '/' in link['src'][1]:
                        var2 = f'img-{str(image_count)}'
                        data[var2] = 'https:'+link['src']
                        image_count += 1

                    if '/' not in link['src'][1]:
                        var2 = f'img-{str(image_count)}'
                        data[var2] = str(url) + link['src']
                        image_count += 1
                else:
                    var2 = f'img-{str(image_count)}'
                    data[var2] = link['src']
                    image_count += 1
        return data or {}

    def get_data(self, url):
        data = {}
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                bs4_soup = BeautifulSoup(res.text, 'lxml')
                data['seo'] = self.get_seo_data(bs4_soup)
                data['p_h_tags'] = self.get_p_h_tag_data(bs4_soup)
                data['images'] = self.get_image_data(bs4_soup, url)
                data['links'] = self.get_links(bs4_soup, url)
                return data or {}
            else:
                return self.get_request_error_msg()
        except requests.exceptions.RequestException:
            return self.get_request_error_msg()

    def get_request_error_msg(self):
        return {
            'status': 'error',
            'message': 'Error in scraping the data',

        }
