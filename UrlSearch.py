import requests
import re
import ciref


class Error(Exception):
    pass

class NoUrlError(Error):
    def __init__(self, expression):
        self.expression = expression

class InvalidUrlError(Error):
    def __init__(self, expression):
        self.expression = expression


class UrlSearch(object):
    def __init__(self, url=None):
        
        self.url = url
        self.request_page_text = None
        self.request_page = None

        self.cita_page = None
        self.ref_page = None
        self.page = None
        
        self.title = None
        self.download_link = None

        self.all_citas = []
        self.all_references = []
        self.your_article = {}
    
    def get_page(self, url=None):
        if self.url == None and url == None:
            raise NoUrlError('Provide a Url')
        if self.url == None:
            self.url = url
        
        self.request_page = requests.get(self.url)
        if self.request_page.status_code != 200:
            raise InvalidUrlError('Invalid Url')
        self.request_page_text = self.request_page.text
    
    def find_title(self, s):
        pat = '<h1 class="nova-e-text nova-e-text--size-xl nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-grey-900 research-detail-header-section__title">'
        x = re.search(pat, s)
        start = x.span()[1]
        end = re.search('</h1>', s[start:]).span()[0] + start
        return s[start:end]
        
    def fill_blanks(self):
        if self.request_page_text == None:
            self.get_page()
        a = self.request_page_text.find('<div class="lite-tabs__tab js-target-citations lite-page-visible">')
        b = self.request_page_text.find('<div class="lite-tabs__tab js-target-references">')
        if a == -1:
            b = self.request_page_text.find('<div class="lite-tabs__tab js-target-references lite-page-visible">')
            if b == -1:
                self.page = self.request_page_text
            else:
                self.page = self.request_page_text[:b]
                self.ref_page = self.request_page_text[b:]
        else:
            self.page = self.request_page_text[:a]
            self.cita_page = self.request_page_text[a:b]
            self.ref_page = self.request_page_text[b:]


        self.title = self.find_title(self.page)
        self.download_link = ciref.download_link(self.page)
        self.your_article['title'] = self.title
        self.your_article['download_link'] = self.download_link


        if self.ref_page != None:
            refers = ciref.Refs(self.ref_page)
            refers.do_work()
            self.all_references = refers.refs
        if self.cita_page != None:
            citas = ciref.Citas(self.cita_page)
            citas.do_work()
            self.all_citas = citas.all_citas
        

    @staticmethod
    def download(url):
        x = requests.get(url)
        s = x.text
        return ciref.download_link(s)


#url = 'https://www.researchgate.net/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan'
#myob = UrlSearch(url)
#myob.fill_blanks()
#print(myob.your_article)
#print(myob.all_citas)
#print(myob.all_references)
# url = 'https://www.researchgate.net/publication/347261078_Recognition_of_Turkish_Sign_Language_TID_Using_sEMG_Sensor'

# print(UrlSearch.download(url))
