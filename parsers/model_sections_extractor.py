from bs4 import BeautifulSoup

class ModelSectionsExtractor:
    def __init__(self, content):
        self.content = content

    def _extract_links_from_html(self, html):
        href_values = []
        soup = BeautifulSoup(html, 'html.parser')
        ul_tag = soup.find('ul', id='primary-navigation')

        if ul_tag:
            li_tags = ul_tag.find_all('li')

            for li in li_tags[:4]:
                a_tag = li.find('a')
                href = a_tag.get('href') if a_tag else None
                href_values.append(href)

        return href_values

    def _add_additional_links(self, links):
        links.append('/plussize/')
        links.append('/women/')

    def get_section_links(self):
        parent_category_links = self._extract_links_from_html(self.content)
        self._add_additional_links(parent_category_links)

        return parent_category_links
