import http.client

class Page:

    def __init__(self, servername, path):
        self.set_target(servername, path)

    def set_target(self, servername, path):
        self.servername = servername
        self.path = path.replace(' ','%20')

    def __get_page(self):

        server = http.client.HTTPConnection(self.servername)
        server.putrequest('GET', self.path)
        server.putheader('Accept', 'text/html')
        server.endheaders()

        return server.getresponse()

    def get_as_string(self):
        page = ''
        reply = self.__get_page()

        if reply.status != 200:
            page = 'Error sending request {0} {1}'.format(reply.status, reply.reason)
        else:
            data = reply.readlines()
            reply.close()
            for line in data:
                page += line.decode('utf-8')
        return page
