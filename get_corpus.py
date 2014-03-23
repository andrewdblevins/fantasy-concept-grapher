from bs4 import BeautifulSoup
import urllib2
"http://www.bardwood.com/magical_lore/stones.html"
url = "http://www.bardwood.com/magical_lore/wood-trees.html"

content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content)

for link in soup.find_all('a'):
	    print(link.get('href'))


print(soup.get_text())
