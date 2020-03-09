import get_proxy
import http_utils as parser
import file_utils


def get_save_links():
    url = 'https://printcopy.info/?mod=pc'
    proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
    useragent = {'User-Agent': get_proxy.get_useregent_list()}
    brand_list = parser.get_brand_model_links(parser.get_html(url, useragent, proxy), 'brandList')

    for brand in brand_list:
        print(brand['name'])
        proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
        useragent = {'User-Agent': get_proxy.get_useregent_list()}

        # присваиваем html страницу в переменную soup
        soup = parser.get_html(brand['href'], useragent, proxy)
        page_count = parser.get_pagination_index_models(soup)
        print(page_count)
        model_link = parser.get_brand_model_links(soup, 'modelList')
        file_utils.save_model_links_csv(model_link, brand['name'], brand['name'])
        if page_count > 1:
            for i in range(page_count):
                index = i + 2
                if index <= page_count:
                    model_link = parser.get_brand_model_links(
                        parser.get_html(brand['href'] + f'&page={index}', useragent, proxy),
                        'modelList')
                    file_utils.save_model_links_csv(model_link, brand['name'], brand['name'])


def parser_models():
    file_index = 0
    model_links = file_utils.load_links_brand()
    for brand in model_links:
        brand_name = brand[0]
        for model in brand:
            file_index += 1
            proxy = {'http': 'http://' + get_proxy.get_proxies_list()}
            useragent = {'User-Agent': get_proxy.get_useregent_list()}
            # присваиваем html страницу в переменную soup
            soup = parser.get_html(model['href'], useragent, proxy)
            model_name = model['name']
            print(str(file_index) + '. ' + model_name)
            modules = parser.get_modules(soup, 'pcToc')

            for module in modules:
                module_name = module['name']
                soup = parser.get_html(module['href'], useragent, proxy)
                file_utils.save_partcode(parser.get_partcodes(soup, brand_name['brand'], model_name, module_name),
                                         brand_name['brand'], model_name)


def main():
    parser_models()


if __name__ == '__main__':
    main()
