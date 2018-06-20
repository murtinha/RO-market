import requests
import json
import re
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'my-app/0.0.1',
    'cookie': '__cfduid=dd2bc98b37a58f03b9074d7a4fd137ea21527513404; _ga=GA1.2.279426244.1527513406; fluxSessionData=6df671d7359a7e03c118711b9ba030d5; _gid=GA1.2.1024025882.1528670382; cookiescriptaccept=visit',
}

def get_item(item_id):
    market = requests.get('https://www.novaragnarok.com/?module=vending&action=item&id=%s'% item_id, headers = headers)
    s = BeautifulSoup(market.text, 'html.parser')
    name = s.h2.span.a.text
    img = 'https://www.novaragnarok.com/%s' % s.h2.img['src']
    h_table = s.find_all('table', class_='horizontal-table')
    thead = h_table[1].thead
    ths = thead.tr.find_all('th')
    for n in range(len(ths)):
        if ths[n].a:
            if 'Price' in ths[n].a.text:
                index = n
                break
    tbody = h_table[1].tbody
    tr = tbody.find_all('tr')[0]
    td = tr.find_all('td')[index].span
    return dict(name = name, price = td.text, image = img)

def get_transaction_history(item_id):
    thistory = []
    page = 1

    while len(thistory) < 15:
        market = requests.get('https://www.novaragnarok.com/?module=vending&action=itemhistory&id=%s&p=%s'% (item_id, page), headers = headers)
        s = BeautifulSoup(market.text, 'html.parser')
        h2s = s.find_all('h2')

        for h2 in h2s:
            if 'Transaction History' in h2.text:
                hasTransaction = True
                break
            else:
                hasTransaction = False

        if hasTransaction:
            tables = s.find_all('table', class_='horizontal-table')
            if len(tables) <= 1:
                break
            trs = tables[1].tbody.find_all("tr")
            for idx in range(len(trs)):
                tds = trs[idx].find_all("td")
                date = re.match('.{8}', tds[0].text.strip()).group(0)
                price = tds[1].text.strip()
                thistory.append(dict(data = date, price = price))
            page = page + 1
        else:
            break
    print thistory

get_transaction_history(4040)
