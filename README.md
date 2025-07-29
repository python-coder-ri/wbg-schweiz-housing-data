# WBG Schweiz Scraper 🇩🇪

A Python-based web scraper designed to extract publicly available data from the German housing cooperative website [wbg-schweiz.ch](https://www.wbg-schweiz.ch). This tool helps collect information such as organization names, addresses, contact details, and descriptions.

##  Features

- Scrapes cooperative housing listings
- Extracts:
  - Organization name
  - Address
  - City, Postal code
  - Contact number (if available)
  - Website (if provided)
  - Description / additional notes
- Outputs structured data to CSV/Excel
- Easy to customize for similar German sites

##  Technologies Used

- Python 3
- requests
- BeautifulSoup
- pandas
- Optional: selenium (if used in your script)

##  Folder Structure

/wbg-schweiz-scraper │ ├── wbg_scraper.py         # Main scraping script ├── data_sample.csv        # Sample output data ├── README.md              # Project overview ├── .gitignore             # Ignore Python cache and venv └── LICENSE                # MIT license

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/python-coder-ri/wbg-schweiz-scraper.git
   cd wbg-schweiz-scraper

## Install required libraries

pip install -r requirements.txt

## Run the script

python wbg_scraper.py

## License

This project is licensed under the MIT License. See the LICENSE file for details.
