from bs4 import BeautifulSoup
import PopHttp
import PopClass
import RootParser
import re

class Parser():

    def __init__(self, category, servername, path):
        self.set_target(servername, path)
        self.category = category
        index = int(path[-2]) + 1
        self.nextpath = path[:-2] + str(index) + path[-1:]

    def set_target(self, servername, path):
        self.servername = servername
        self.path = path

    # Use regular expression to fetch number
    def __get_number(self, block):
        n = block.find(class_="txsmall").get_text()
        i = re.search('[A-Z]', n)
        number = n
        if i:
            number = n[:i.start()]
        return number

    # Get the various pop details, generate pop object and add to array
    def __parse_details(self, blocks):
        pops = []
        for block in blocks:
            name = block.find(class_="itemlisttext-ext-new").b.get_text()
            number = self.__get_number(block)
            value = block.find(class_="valuebar").get_text()
            if value == 'N/D':
                value = 0.0
            else:
                value = float(value[1:].replace(',',''))
            is_variant = False
            if '(' in name:
                is_variant = True
            url = block.find('a').get('href')
            pop = PopClass.Pop(self.category, name, number, value, is_variant, url)
            pops.append(pop)

        return pops

    # Get all Pop value blocks from html
    def __get_blocks(self, parser):
        block = []
        for row in parser.find_all(class_="itemrow-ext"):
            block.append(row)

        return self.__parse_details(block)

    def __is_next(self, parser):
        for tag in parser.find_all('a'):
            if self.nextpath in tag.get('href'):
                return True

        return False

    def __create_parser(self, link, pops):
        next_parser = Parser(self.category, self.servername, link)
        next_pops = next_parser.parse_target()
        for next_pop in next_pops:
            pops.append(next_pop)

        return pops

    # Retrieve Page and parse content
    def parse_target(self):
        print(self.path+ ' is being parsed')
        page = PopHttp.Page(self.servername, self.path)
        response = page.get_as_string()
        parser = BeautifulSoup(response)

        # Parse the page
        pops = self.__get_blocks(parser)

        # Television is exception with subcategories
        if self.path == '/guide/PopVinyl_PopTelevision/1/':
            root_parser = RootParser.RootParser(self.servername, self.path)
            links = root_parser.parse_target()
            for link in links:
                pops = self.__create_parser(link[0],pops)

        # Check if there is another link to the same category is included
        if self.__is_next(parser):
            pops = self.__create_parser(self.nextpath, pops)

        return pops
