from pyshorteners import Shortener
link = 'http://www.google.com'
s = Shortener('Tinyurl')
print(s.short(link))
link = 'https://www.ptt.cc/'
s = Shortener('Tinyurl')
print(s.short(link))
