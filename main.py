import requests
from rich import print
from bs4 import BeautifulSoup

EVENTNAME = 'höhere quantenmechanik'

queryparams = {
    'state': 'wsearchv',
    'search': '1',
    'subdir': 'veranstaltung',
    'alias_pord.pordnr': 'r_zuordpos.pordnr',
    'veranstaltung.dtxt': EVENTNAME,
    'veranstaltung.semester': '20171',
    'alias_pord.pordnr': 'r_zuordpos.pordnr',
    'P_start': '0',
    'P_anzahl': '10',
    'P.sort': '',
    '_form': 'display',
}

baseUrl = 'https://www.lsf.tu-dortmund.de/qisserver/rds'

req = requests.get(baseUrl, params=queryparams)
assert EVENTNAME in req.text

soup = BeautifulSoup(req.text, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')[1:]
# names = [row.find('a').text for row in rows]
events = [
    {
        'name': row.find('a').text,
        'url': row.find('a').get('href'),
    }
    for row in rows
]
print(events)


event = events[0] # TEST

eventPage = requests.get(event['url'])
eventSoup = BeautifulSoup(eventPage.text, 'html.parser')

eventPerson = eventSoup.find('td', headers='persons_1')
print(eventPerson.text.strip())
