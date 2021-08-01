import requests
from bs4 import BeautifulSoup

# first sandwiches
# 1. get all the URLs for the sandwiches
# 2. iterate through them while checking the calories
# now we have all the calories for the sandwiches

# have to check netpincer for the prices


def get_product_category_by_name(name: str):
    if name == 'szendvicsek-es-wrapek':
        return 'product-category-1'


def get_products_html():
    return requests.get('https://www.mcdonalds.hu/termekek/')


products_html = get_products_html()

product_category = get_product_category_by_name('szendvicsek-es-wrapek')

sandwiches_soup = BeautifulSoup(products_html.text, 'html.parser')

products = sandwiches_soup.find_all('div', {'id': product_category})[0].ul

products_dict = {}

for child in products:
    product_page = requests.get('https://www.mcdonalds.hu' + child.article.a['href'])
    product_soup = BeautifulSoup(product_page.text, 'html.parser')
    product_name = child.article.a['href'].split('/')[-1]

    # there's a tr in the thead
    calorie = product_soup.find_all('table', {'class': 'nutrition-table'})[0].find_all('tr')[2].find_all('td')[1].text

    products_dict[product_name] = calorie

# you can sort dicts starting from Python 3.7+
sorted_calories = {k: v for k, v in sorted(products_dict.items(), key=lambda item: item[1], reverse=True)}

for key, value in sorted_calories.items():
    print(key, value)


