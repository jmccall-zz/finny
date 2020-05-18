'''
Seeking alpha scraper stufff
'''
import logging
import re
import requests

from bs4 import BeautifulSoup

def get_div_years_of_growth(symbol):
    ''' Return number of consecutive years of dividend growth for a symbol '''
    logger = logging.getLogger('finny')

    url = 'https://dividendhistory.org/payout/{}/'.format(symbol)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.body.find(id="dividend_table").tbody

    div_history = []

    for row in table:
        if not row or row.name != 'tr':
            logger.debug('Not a valid row: %s', row)
            continue

        line = row.get_text()
        parts = [x for x in line.split('\n') if x]
        if len(parts) not in (3, 4):
            logger.debug('Weird line: %s', parts)
            continue

        ex_div_date = parts[0] # 'yyyy-mm-dd'
        payout_date = parts[1] # 'yyyy-mm-dd'
        amount = float(re.match(r'\$(\d+\.\d+)', parts[2]).group(1)) # '$0.4233'
        percent_change = 0
        if len(parts) == 4:
            match = re.match(r'-?\d+\.\d{2}', parts[3])
            percent_change = match.group(0) if match, else 0

        # import pdb; pdb.set_trace()
        logger.debug('Data: %s', parts)

    return r
