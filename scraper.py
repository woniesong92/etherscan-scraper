import requests
import csv
import sys
from bs4 import BeautifulSoup

def scrape(num_pages=1, tx_limit=1):
  print("Parsing %d pages with with tx count >=%d...\n" % (num_pages, tx_limit))
  api_url = "https://etherscan.io/contractsVerified/"

  with open('data.csv', 'w') as csvfile:
    fieldnames = ['addr', 'contract_name', 'compiler', 'balance', 'tx_count', 'settings', 'date_verified']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(num_pages):
      url = api_url + str(i)
      print("Scraping: %s..." % url)
      resp = requests.get(url)
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
