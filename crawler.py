import requests
import json
from bs4 import BeautifulSoup

def get_item(item_id):
    headers = {
        'user-agent': 'my-app/0.0.1',
        'cookie': '__cfduid=dd2bc98b37a58f03b9074d7a4fd137ea21527513404; _ga=GA1.2.279426244.1527513406; fluxSessionData=6df671d7359a7e03c118711b9ba030d5; _gid=GA1.2.1024025882.1528670382; cookiescriptaccept=visit',
    }

    market = requests.get('https://www.novaragnarok.com/?module=vending&action=item&id=%s'% item_id)
    s = BeautifulSoup(market.text, 'html.parser')
    name = s.h2.span.a.text
    img = 'https://www.novaragnarok.com/%s' % s.h2.img['src']
    h_table = s.find_all('table', class_='horizontal-table')
    thead = h_table[1].thead
    ths = thead.tr.find_all('th')
    for n in range(len(ths) - 1):
        if ths[n].a:
            if 'Price' in ths[n].a.text:
                index = n
                break
    tbody = h_table[1].tbody
    tr = tbody.find_all('tr')[0]
    td = tr.find_all('td')[index].span
    return dict(name = name, price = td.text, image = img)

