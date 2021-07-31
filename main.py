import requests
from bs4 import BeautifulSoup

# first sandwiches
# 1. get all the URLs for the sandwiches
# 2. iterate through them while checking the calories
# now we have all the calories for the sandwiches

# have to check netpincer for the prices

sandwiches_html = requests.get('https://www.mcdonalds.hu/termekek/szendvicsek-es-wrapek')

soup = BeautifulSoup(sandwiches_html.text, 'html.parser')

result = soup.find_all('div', {'id': 'product-category-1'})

products = result[0].ul

for child in products:
    print(child.article.a['href'])
