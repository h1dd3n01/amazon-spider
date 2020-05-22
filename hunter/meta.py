check_year = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013']
check_ram = ['4GB RAM', '8GB RAM', '12GB RAM', '16GB RAM', '24GB RAM', '32GB RAM', '4GB', '8GB',
             '16GB', '24GB', '32GB']

check_ssd = ['128GB SSD', '128GB', '128 GB', '256GB SSD', '256GB', '512GB', '512GB SSD', '2TB Fusion', '1TB HDD',
             '32GB Storage', '64GB Storage', '1TB+256GB SSHD',
             '128GB Storage', '256GB Storage', '512GB Storage', '64GB SSD', '64GB', '1TB HDD', '1TB+256GB',
             '1TB+512GB']

check_cpu = ['Core i7-8750', 'Intel Celeron 3865U', 'Intel Core i5-8250', 'Core i7-8550U', 'Intel i5-10210U',
             'Intel Core i9-9980HK', 'Intel Core i7-7200U', 'Intel Core i7-7500U', 'Core i7-8750H',
             'Core i7-8750', 'Intel Core i3-5005U', 'Core i7-9700K', 'Intel i5-9300H', 'Intel Core-i7-7700'
                                                                                       'Intel Core i7-8550',
             'Intel Dual Core N4000', 'Intel Core i7-8750H', 'Intel i9-9880H', 'Intel Xeon E5-1660V3 Octa-Core',
                                                             'Intel Dual Core', 'Intel Celeron',
             'Intel Pentium N4200',
             'Intel Core i5',
             'Intel Core i7', 'Intel Core i3', 'Core i5', 'Core i7', 'Core i3', ]

check_screen = ['13.3', '15.4', '6.5', '4.7', '10.5', '7.9', '4-inch', '6.1-inch', '11.6', '12.5', '15.6',
                '17.3', '14', '10.6']

check_apple_product = ['Apple Macbook Pro', 'Apple iPod Touch', 'Apple Mac Mini Slimline Desktop PC', 'Apple Mac Pro',
                       'Apple iPad Pro', 'Apple iMac', 'Apple iPod Touch'
                                                       'Apple iPhone 6s', 'MacBook Pro', 'iPod Touch']

from itertools import chain


def parse_meta(item, brand):
    title = item['title']
    ssd = [i for i in check_ssd if i in title]
    cpu = [i for i in check_cpu if i in title]
    ram = [i for i in check_ram if i in title]
    screen = [i for i in check_screen if i in title]
    year = [i for i in check_year if i in title.replace('(', '').replace(')', '')]
    if '£' in item['price']:
        price = item['price'].replace('£', '').replace('\n', '').replace(',', '')
        price = str(float(price) * 1.07).partition('.')[0]
    else:
        price = item['price'].replace('$', '').replace('\n', '').replace(',', '')
        price = str(float(price) * 0.9).partition('.')[0]
    if brand.lower() == 'apple':
        title = [i for i in check_apple_product if i in title]
    else:
        title = title.split('"')[0]
        title = [title.replace(i, '') for i in chain(check_year,
                                                     check_screen,
                                                     check_ram,
                                                     check_ssd,
                                                     check_cpu)]

    return {
        'title': title[0] if len(title) > 0 else item['title'],
        'ssd': ssd[0] if len(ssd) > 0 else '',
        'cpu': cpu[0] if len(cpu) > 0 else '',
        'ram': ram[0] if len(ram) > 0 else '',
        'screen': screen[0] if len(screen) > 0 else '',
        'year': year[0] if len(year) > 0 else '',
        'price': int(price)
    }
