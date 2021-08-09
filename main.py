import sys
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# TODO: do something with products that have different names across netpincer and mcdonalds.hu

# first sandwiches
# 1. get all the URLs for the sandwiches
# 2. iterate through them while checking the calories
# now we have all the calories for the sandwiches

# have to check netpincer for the prices

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_product_category_by_name(name: str):
    if name == 'szendvicsek-es-wrapek':
        return 'product-category-1'


def get_products_html():
    print(bcolors.OKBLUE + 'https://www.mcdonalds.hu/termekek/ HTML lekérése...' + bcolors.ENDC)
    print()
    return requests.get('https://www.mcdonalds.hu/termekek/')


def get_menus_json():
    return requests.get('https://hu.fd-api.com/api/v5/vendors/g9oz?include=menus&language_id=3&dynamic_pricing=0&'
                        'opening_type=delivery&basket_currency=HUF').json()


def get_calories(products_dict):
    for ul in uls:
        for child in ul:
            product_page_response = requests.get('https://www.mcdonalds.hu' + child.article.a['href'])
            product_soup = BeautifulSoup(product_page_response.text, 'html.parser')
            product_name = child.article.a['href'].split('/')[-1].replace('maestro-', '')
            if 'glutenmentes' in product_name:
                continue

            # there's a tr in the thead
            calorie = product_soup.find_all('table', {'class': 'nutrition-table'})[0].find_all('tr')[2].find_all('td')[
                1].text

            products_dict[product_name] = {'calorie': calorie}


def get_prices(products_dict):
    for item in get_menus_json()['data']['menus'][0]['menu_categories'][2]['products']:
        product_name = item['name'].replace(' ', '-').lower().replace('®', '')
        if product_name in products_dict:
            products_dict[product_name]['price'] = item['product_variations'][0]['price']
            products_dict[product_name]['value'] = int(products_dict[product_name]['calorie']) / \
                                                   int(products_dict[product_name]['price'])

products_response = get_products_html()

if products_response.status_code != 200:
    print(bcolors.FAIL + 'A McDonald\'s weboldalát nem sikerült elérni...' + bcolors.ENDC)
    sys.exit(1)

product_category = get_product_category_by_name('szendvicsek-es-wrapek')

sandwiches_soup = BeautifulSoup(products_response.text, 'html.parser')

uls = sandwiches_soup.find_all('div', {'id': product_category})[0].find_all('ul')

products_dict = {}

get_calories(products_dict)

print(bcolors.OKGREEN + 'A következő adatokat kaptuk: ' + bcolors.ENDC)


# now let's get the stuff from netpincer
get_prices(products_dict)


# you can sort dicts starting from Python 3.7+
sorted_calories = {k: v for k, v in sorted(filter(lambda x: 'price' in x[1], products_dict.items()), key=lambda item: item[1]['value'], reverse=True)}

print(tabulate([[key, value['calorie'], value['price'], value['value']] for key, value in sorted_calories.items() if 'price' in value], headers=['Termék', 'Kcal', 'Price', 'Value']))
