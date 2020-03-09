import re
import requests
import file_utils
from time import sleep
from random import uniform
from bs4 import BeautifulSoup as bs


def get_html(url, useragent=None, proxy=None):
    t = uniform(2, 6)
    sleep(t)
    session = requests.Session()
    request = session.get(url=url, headers=useragent, proxies=proxy)
    if request.status_code == 200:
        return bs(request.text, 'lxml')
    else:
        print("Error " + str(request.status_code))
        return request.status_code


def get_pagination_index_models(soup):
    try:
        pagination = soup.find_all('div', class_='btnCell')[-1]
        pagination_links = pagination.find('a')['href']
        count = re.search(r'\d*$', pagination_links)
        return int(count[0])
    except:
        return 1


def parser_errors(soup, brand_name, model_name):
    result = []
    erc_list = soup.find('div', class_='ercList')
    erc_row = erc_list.find_all('li')
    for erc_li in erc_row:
        caption = erc_li.find('span').text.strip()
        if caption == 'Image:':
            img = erc_li.find('img')['src']
            value = file_utils.save_img(img, brand_name, model_name)
        else:
            value = re.sub(caption.strip(), '', erc_li.text).strip()
        result.append({
            'caption': caption[0:-1],
            'value': value,
        })
    return result


def get_modules(soup, parser_class_name):
    prod_list = []
    brand_list = soup.find('ul', class_=str(parser_class_name))
    brands = brand_list.find_all('li')
    for brand in brands:
        name = brand.find('a').text.strip()
        href = brand.find('a')['href']
        prod_list.append({
            'name': re.sub(r'^\d+.', '', name).strip(),
            'href': 'https://printcopy.info/' + href,
        })
    return prod_list


def get_partcodes(soup, brand_name, model_name, module):
    data = []
    img = ''
    figure_url = soup.find('figure')
    url = figure_url.find('img')['src']
    if url != '':
        img = file_utils.save_img(url, brand_name, model_name)

    table = soup.find('table', class_='tblPL')
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        data.append({
            'module': module,
            'partcode': cols[1].text.strip(),
            'name': cols[2].text.strip(),
            'desc': cols[3].text.strip(),
            'img': img
        })

    return data
