import re
import requests



class KeySearch(object):
    def __init__(self, query):
        self.query = query
        self.search_query = '%20'.join(self.query.split(' '))
        self.link = 'https://www.researchgate.net/search.Search.html?type=publication&query=' + self.search_query
        self.pat = '<a class="nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare"'
        self.lst = []
        self.request_page = None
        self.request_text = None
        self.search_results = []
    def __str__(self):
        return self.search_query

    def get_page(self):
        self.request_page = requests.get(self.link)
        self.request_text = self.request_page.text

    def fill_lst(self):
        if self.request_page == None:
            self.get_page()
        indexes = re.finditer(self.pat, self.request_text)
        for i in indexes:
            self.lst.append(i.span())
        self.lst = self.lst[:-5]
    
    def fill_results(self):
        if self.request_text == None:
            self.fill_lst()
        regions = []
        for i in self.lst:
            y = re.search('</a>', self.request_text[i[1]:])
            y = y.span()
            search_region = self.request_text[i[0]:i[1]+y[1]]
            regions.append(search_region)
        
        for region in regions:
            l_s = re.search('href="', region)
            l_s = l_s.span()[1]
            l_e = re.search('[?]', region)
            l_e = l_e.span()[0]
            link = region[l_s:l_e]
            t_s = re.search('>', region)
            t_s = t_s.span()[1]
            t_e = re.search('</a>', region)
            t_e = t_e.span()[0]
            title = region[t_s:t_e]
            search_result = {'link':link, 'title':title}
            self.search_results.append(search_result)


#a = KeySearch('AI, IOT')
#a.fill_results()
#print(a.search_results)




