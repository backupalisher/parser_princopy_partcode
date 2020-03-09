import re
import os
import csv
import glob
import time
import shutil
import requests


def save_model_links_csv(prods, brand_name, model_name):
    for prod in prods:
        if not os.path.exists(brand_name):
            os.mkdir(brand_name)
        with open(os.path.join(os.path.dirname(__file__), brand_name, model_name), 'a', encoding='utf-8') as file:
            add_data = csv.writer(file, delimiter=';', lineterminator='\n')
            add_data.writerow((prod['name'], prod['href']))


def save_partcode(data, brand_name, model_name):
    for pc in data:
        base_dir = os.path.dirname(__file__)
        base_dir = f'{base_dir}\parse\{brand_name}'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        fn = f'{base_dir}\{model_name}.csv'
        with open(fn, 'a',
                  encoding='utf-8') as file:
            add_data = csv.writer(file, delimiter=';', lineterminator='\n')
            add_data.writerow((pc['module'], pc['partcode'], pc['name'], pc['desc'], pc['img']))


def spaseSub(text):
    result = re.sub('\s', '', text)
    return result


def load_link(file_name):
    model_link = []
    with open(file_name, 'r', newline='') as file:
        line_read = csv.reader(file, delimiter=';', lineterminator='\n')
        for row in line_read:
            model_link.append({
                'brand': os.path.basename(file_name),
                'name': row[0],
                'href': row[1],
            })
    return model_link


def load_links_brand():
    models_links = []
    files = glob.glob('./links/*')
    for f in files:
        models_links.append(load_link(os.path.join(os.path.dirname(__file__), f)))
    return models_links


def save_img(url, brand_name, model_name):
    fn = ''
    r = requests.get('http://printcopy.info/' + url, stream=True)
    if r.status_code == 200:
        timestamp = str(round(time.time() * 1000))

        base_dir = os.path.dirname(__file__)
        base_dir = f'{base_dir}\parse\{brand_name}_image'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        fn = f'{base_dir}\{model_name}_{timestamp}.png'

        with open(fn, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        fn = f'{brand_name}_image\{model_name}_{timestamp}.png'
        print(fn)
    return fn
