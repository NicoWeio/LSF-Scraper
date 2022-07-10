import requests
from rich import print
from bs4 import BeautifulSoup

BASE_URL = 'https://www.lsf.tu-dortmund.de/qisserver/rds'

def find_events(name, semester):
    queryparams = {
        'state': 'wsearchv',
        'search': '1',
        'subdir': 'veranstaltung',
        'alias_pord.pordnr': 'r_zuordpos.pordnr',
        'veranstaltung.dtxt': name.lower(),
        'veranstaltung.semester': semester,
        'alias_pord.pordnr': 'r_zuordpos.pordnr',
        'P_start': '0',
        'P_anzahl': '10',
        'P.sort': '',
        '_form': 'display',
    }


    req = requests.get(BASE_URL, params=queryparams)
    assert name.lower() in req.text

    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    events = [
        {
            'name': row.find('a').text,
            'url': row.find('a').get('href'),
        }
        for row in rows[1:]
    ]
    return events

def get_event_details(url):
    req = requests.get(event['url'])
    soup = BeautifulSoup(req.text, 'html.parser')

    return {
        'person': soup.find('td', headers='persons_1').text.strip(),
    }


for year in range(2015, 2022+1):
    try:
        event = find_events('Höhere Quantenmechanik', f'{year}1')[0]
        details = get_event_details(event['url'])
        print(f"SS{year}: {details['person']}")
    except IndexError:
        print(f"SS{year}: no event found")
