import re


def download_link(s):
  pat = '<a class="nova-c-button nova-c-button--align-center nova-c-button--radius-m nova-c-button--size-m nova-c-button--color-blue nova-c-button--theme-solid nova-c-button--width-full js-target-download-btn-'
        
  s1 = re.search(pat, s)
  if s1 == None:
    return 'No downloadable Content'
  start = s1.span()[0]
  s = s[start:]
  s2 = re.search('href="', s)
  s2 = s2.span()
  s = s[s2[1]:]
  end = s.find('"')
  link = 'https://www.researchgate.net/' + s[:end]
  return link


def find_divs(div_list1, div_list2):
        res = []
        pt1 = 0
        pt2 = 0
        stack = []
        while pt1 < len(div_list1) and pt2 < len(div_list2):
            s1 = div_list1[pt1][0]
            s2 = div_list2[pt2][0]
            if s1 < s2:
                stack.append(pt1)
                pt1 += 1
            else:
                if len(stack) == 0:
                    return res
                last = stack.pop()
                pt2 += 1
                if div_list1[last][2] == 1:
                    res.append((div_list1[last][0], s2))
        return res


def find_texts(s):
    text_pat = '<div class="nova-e-text nova-e-text--size-m nova-e-text--family-sans-serif nova-e-text--spacing-none nova-e-text--color-inherit nova-v-citation-item__context-body">'
    text_list = []
    k = re.finditer(text_pat, s)
    for i in k:
        text_start = i.span()[1]
        text_end = re.search('</div>',s[text_start:]).span()[0] + text_start
        text_list.append(s[text_start:text_end])
    return text_list

def title_and_link(s):
        full_text_available = False
        if 'Full-text available' in s:
            full_text_available = True
        pat = '<a class="nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare"'
        k = re.search(pat, s)
        if k == None:
            return False
        s = s[k.span()[0]:]
        link_start = re.search('href="', s).span()[1]
        link_end = re.search('"', s[link_start:]).span()[0] + link_start
        title_start = re.search('>', s[link_end:]).span()[0] + link_end
        title_end = re.search('</a>', s).span()[0]
        # print(parap[link_start:link_end])
        # print(parap[title_start:title_end])
        link = 'https://www.researchgate.net/' + s[link_start:link_end]
        title = s[title_start+1:title_end]
        return {'title':title, 'link':link, 'full_text':full_text_available}


class Refs(object):
    def __init__(self, ref_page=None):
        self.ref_page = ref_page
        self.refs = []
    
    def do_work(self):
        lst1 = []
        lst2 = []
        self.ref_page = self.ref_page + '<div'
        a1 = re.finditer('<div', self.ref_page)
        a2 = re.finditer('</div', self.ref_page)
        a3 = re.finditer('<div class="nova-o-stack__item">', self.ref_page)
        for i in a1:
            tupl = (i.span()[0], i.span()[1], 0)
            lst1.append(tupl)

        for i in a2:
            lst2.append(i.span())

        for i in a3:
            tupl = (i.span()[0], i.span()[1]-28, 0)
            if tupl in lst1:
                ind = lst1.index(tupl)
                lst1[ind] = (i.span()[0], i.span()[1]-28, 1)
        divs = find_divs(lst1, lst2)
        for i in divs:
            k = title_and_link(self.ref_page[i[0]:i[1]])
            if k != False:
                self.refs.append(k)


class Citas(object):
    def __init__(self, cita_page):
        self.cita_page = cita_page
        self.all_citas = []
        self.seperator = '<div class="nova-o-stack__item publication-citations__item publication-citations__item--redesign">'
    def do_work(self):
        lst1 = []
        lst2 = []
        a1 = re.finditer('<div', self.cita_page)
        a2 = re.finditer('</div>', self.cita_page)
        a3 = re.finditer(self.seperator, self.cita_page)

        for i in a1:
            tupl = (i.span()[0], i.span()[1], 0)
            lst1.append(tupl)

        for i in a2:
            lst2.append(i.span())

        for i in a3:
            tupl = (i.span()[0], i.span()[1]-94, 0)
            if tupl in lst1:
                ind = lst1.index(tupl)        
                lst1[ind] = (i.span()[0], i.span()[1]-94, 1)
        res = find_divs(lst1, lst2)
        for i in res:
            cita_region = self.cita_page[i[0]:i[1]]
            dct = title_and_link(cita_region)
            texts = find_texts(cita_region)
            dct['citation_text'] = texts
            self.all_citas.append(dct)

