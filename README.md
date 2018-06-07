# Etherscan Scraper

Parse [Verified Contract](https://etherscan.io/contractsVerified) on Ethereum and filter by transaction count.

## Usage

1. Install necessary packages

    ```
    $ pip install -r requirements.txt
    ```

2. Run the script

    ```
    // Parse 1 page of verified contracts that have at least 10 transactions
    $ python scraper.py 1 10
    ```

3. Inspect `data.csv`
