from bs4 import BeautifulSoup
import PopHttp

class RootParser():

    def __init__(self, servername, path):
        self.set_target(servername, path)

    def set_target(self, servername, path):
        self.servername = servername
        self.path = path

    def __get_details(self, link):
        path = link[28:]
        category = link[link.index('Vinyl_') + 6 :link.index('/1/')]
        category = category.replace('Pop','').replace('POP','')
        category = category.strip('- ')
        link_details = [path,category]

        return link_details

    # Get all Pop value blocks from html
    def __get_links(self, parser):
        block = []
        for row in parser.find_all(class_="catrow"):
            link = row.a.get('href')
            block.append(self.__get_details(link))

        return block

    # Retrieve Page and parse content
    def parse_target(self):
        page = PopHttp.Page(self.servername, self.path)
        response = page.get_as_string()
        parser = BeautifulSoup(response)
        links = self.__get_links(parser)

        return links
