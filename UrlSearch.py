import requests
import re


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
        self.title = None
        self.link = None
        self.citation_text = None
        self.request_page = None
        self.request_page_text = None
        self.list_of_citas = []
        self.all_citas = []
        self.all_references = []
        self.your_article = []
    def get_page(self, url=None):
        if self.url == None and url == None:
            raise NoUrlError('Provide a Url')
        if self.url == None:
            self.url = url
        
        self.request_page = requests.get(self.url)
        
        self.request_page_text = self.request_page.text
    def get_cita_inds(self):
        if self.request_page == None:
            self.get_page()
        pat = 'class="nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit nova-v-citation-item__context-body'
        x = re.finditer(pat, self.request_page_text)
        for i in x:
            self.list_of_citas.append(i.span())
    
    def get_cita_text(self, ind_end):
        x = re.search('</div>', self.request_page_text[ind_end:])
        dv_start = x.span()[0]
        c_text = self.request_page_text[ind_end+1:ind_end+dv_start]
        return c_text

    def get_title_and_link(self, ind_end):
        pattern = '<a class="nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare"'
        x = re.search(pattern, self.request_page_text[ind_end:])
        pat_start = x.span()[0]
        y = re.search('</a>', self.request_page_text[ind_end:])
        pat_end = y.span()[0]
        needed_str = self.request_page_text[ind_end+pat_start:ind_end+pat_end]
        link_span = re.search('href=".*"', needed_str)
        link_start = link_span.span()[0] + 6
        link_end = link_span.span()[1]
        link = needed_str[link_start:link_end-1]

        title_s = re.search('>', needed_str)
        title = needed_str[title_s.span()[0]+1:]
        return link, title
    
    def get_all_citas(self):
        if self.list_of_citas == [] and self.request_page == None:
            self.get_cita_inds()
        
        for i in self.list_of_citas:
            link, title = self.get_title_and_link(i[1])
            cita_text = self.get_cita_text(i[1])
            self.all_citas.append({'citation_text':cita_text, 'link':link, 'title':title})

    def get_all_ref(self):
        return 0

    def get_your_paper(self):
        return 0
'''
file1 = open("MyFile.txt","a",encoding='utf8') 
myob = UrlSearch('https://www.researchgate.net/publication/229643636_Intellectual_capital_The_new_wealth_of_organizations/citations')
print(myob.list_of_citas, len(myob.list_of_citas))
myob.get_all_citas()

print(len(myob.list_of_citas))
lengt=len(myob.list_of_citas)
i=0
while i < lengt:
	j=0
	while j <lengt:
		if myob.all_citas[i]["title"]==myob.all_citas[j]["title"] or myob.all_citas[i]["link"]==myob.all_citas[j]["link"]:
			myob.all_citas[i]["citation_text"]=myob.all_citas[i]["citation_text"]+"\n \n\n"+(myob.all_citas[j]["citation_text"])
			print("******************")
			print(myob.all_citas[i]["citation_text"]+"\n"+(myob.all_citas[j]["citation_text"]))
			print("index= ",i,j)
			if j!=i and j>i:
				del myob.all_citas[j]
				lengt=lengt-1
		j=j+1
	i=i+1
cursor=[]
for i in range(lengt):
	cursor.append(myob.all_citas[i])
print(cursor[0]["citation_text"])
'''

''' 
referanslar
key word search
paper linkler for download
download graph

 BUg ########################################### 
/citations
/references

'''