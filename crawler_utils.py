from pyshorteners import Shortener
domain = 'https://www.ptt.cc'
def calc_len(string):
    def chr_width(o):
        global widths
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1
    return sum(chr_width(ord(c)) for c in string)


def pretty_print(push, title, date, author, href):
    try:
        link = domain + href
        s = Shortener('Tinyurl')
        URL = s.short(link)
        print(URL)
    except:
        URL = link
        print(link)
    pattern = '*%s*\n作者:%s\n推文數:%s\n日期:%s\n連結:\n%s\n'
    string = pattern % (title, author, push, date, URL)
    return string
