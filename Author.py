import re
import requests
import ciref

class Author(object):
  def __init__(self, link):
    self.link = link
    self.text = None
    self.indicies = []
    self.publications = []
  

  def get_page(self):
    self.text = requests.get(self.link).text

  def first(self):
    self.get_page()
    k = re.search('<div id="research-items">', self.text)
    if (k == None):
        return -1
    self.text = self.text[k.span()[0]:]
    return 0
    
  def find_divs(self):
    
    fi1 = re.finditer('<div', self.text)
    fi2 = re.finditer('</div>', self.text)
    list_of_divs = []
    
    for i in fi1:
      list_of_divs.append(i.span())
    for i in fi2:
      list_of_divs.append(i.span())
    list_of_divs = sorted(list_of_divs)
    list_of_divs.pop(0)
    sc = [(0,24)]
    pat_stack = '<div class="nova-o-stack__item">'
    for i in list_of_divs:
      i_s, i_e = i
      if self.text[i_s:i_e] == '</div>':
        popped = sc.pop()
        if len(sc) == 0:
          break
        d_i, d_e = popped
        if self.text[d_i:d_i + len(pat_stack)] == pat_stack:
          self.indicies.append((d_i,i_e))
      else:
        sc.append(i)
    
  def fill_publications(self):
    k = self.first()
    if k == -1:
        return -1
    self.find_divs()
    for i in self.indicies:
      lt = ciref.title_and_link(self.text[i[0]:i[1]])
      lt['link'] = lt['link'][29:]
      self.publications.append(lt)






# a = Author('https://www.researchgate.net/profile/Hatice_Kose')

# a.fill_publications()
# print(a.publications)