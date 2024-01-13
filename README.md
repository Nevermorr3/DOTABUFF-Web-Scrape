# Dota 2 Esports Matches Scraper

## Description
The 'DOTABUFF Esports Data Scrape.py' Python script scrapes data from the DOTABUFF Esports matches webpage, extracts information about DOTA 2 Esports matches, and stores it in a Pandas DataFrame. The script then appends this new DataFrame to an existing one and writes the merged DataFrame to an Excel file, removing any duplicate entries based on the 'Match_ID' column. If no Excel file exists, the script writes the new DataFrame to an Excel file after removing any duplicate entries based on the 'Match_ID' column. 

The 'Data Pre-processing.py' Python script takes the Excel file, converts it into a DataFrame and cleans the data to produce a new DataFrame with the columns ('Match_ID', 'Series', 'Region', 'Date', 'Time', 'Won', 'Lost', 'Duration'). This DataFrame is then written to a new Excel file that contains the cleaned data.

## Usage
1. Install the required dependencies:
    1. pip install requests beautifulsoup4 pandas
2. Run the script in the order:
    1. DOTABUFF Esports Data Scrape.py
    2. Data Pre-processing.py


## Dependencies
- [requests](https://docs.python-requests.org/en/latest/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [pandas](https://pandas.pydata.org/)

## Notes
- Pycharm is reccomended for running the scripts.
- Ensure that both 'DOTABUFF Esports Data Scrape.py' and 'Data Pre-processing.py' are in the same folder.
- Check 'requirements.txt' and ensure that the right versions of dependencies are installed.
- Ensure that your web scraping complies with the website's terms of service and policies.
- The script may need adjustments if the website's structure changes.
  

## Contributing
- **Contributions are not accepted for this project.**
- This project is intended for personal or private use and is not open for external contributions. If you have questions or feedback, feel free to reach out to the project owner directly.
- Thank you for your understanding.

## License
This project does not have a specific license. It means that users are not granted any rights to use, modify, or distribute the code.



