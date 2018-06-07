import requests
import csv
import sys
from time import sleep
from bs4 import BeautifulSoup

def scrape(num_pages=1, tx_limit=1):
  api_url = "https://etherscan.io/contractsVerified/"
  req_delay = 0.1
  print("Parsing %d pages with with tx count >= %d..." % (num_pages, tx_limit))
  print("We wait for %0.1f sec between each request to be civil!" % req_delay)

  with open('data.csv', 'w') as csvfile:
    fieldnames = ['addr', 'contract_name', 'compiler', 'balance', 'tx_count', 'settings', 'date_verified']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, num_pages):
      url = api_url + str(i)

      # NOTE: sleep for [req_delay] between requests to avoid getting flagged
      sleep(req_delay)
      resp = requests.get(url)
      print("URL: %s, Status: %s" % (url, resp.status_code))

      c = resp.content
      soup = BeautifulSoup(c, 'html.parser')

      for row in soup.select('table.table-hover tbody tr'):
        cells = row.findAll('td')
        cells = map(lambda x: x.text, cells)
        addr, contract_name, compiler, balance, tx_count, settings, date_verified = cells

        if int(tx_count) > tx_limit:
          writer.writerow({
            'addr': addr,
            'contract_name': contract_name,
            'compiler': compiler,
            'balance': balance,
            'tx_count': tx_count,
            'settings': settings,
            'date_verified': date_verified,
          })

def main():
  if len(sys.argv) > 2:
    scrape(int(sys.argv[1]), int(sys.argv[2]))
  elif len(sys.argv) == 2:
    scrape(int(sys.argv[1]))
  else:
    scrape()

if __name__ == "__main__":
  main()
