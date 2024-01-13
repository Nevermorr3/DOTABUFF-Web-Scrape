# Importing libraries
import random
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Defining headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}


# Defining function to scrape data
def scrape_data(url):
    all_data = []

    # Initialize delay and max retries
    base_delay = 15
    max_retries = 3
    current_page = 1

    while True:
        # Construct the URL for the current page
        page_url = f"{url}?page={current_page}"

        # Make a request to the URL
        response = requests.get(page_url, headers=headers)

        # Check if the page exists
        if response.status_code != 200:
            print(f"Failed to fetch data from {page_url}. Status code: {response.status_code}")

            # Check if it's a rate-limiting issue (HTTP 429)
            if response.status_code == 429 and max_retries > 0:
                retry_after = int(response.headers.get('Retry-After', base_delay))
                print(f"Rate-limited. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                max_retries -= 1
                continue  # Retry the request

            break  # Break the loop if the page doesn't exist or max retries exceeded

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data from the table with a specific class
        table = soup.find('table', class_='table table-striped table-condensed recent-esports-matches')

        # Iterate over rows
        for row in table.find_all('tr'):
            # Extracting each td element
            tds = row.find_all('td')

            # Skip rows with insufficient columns
            if len(tds) < 8:
                continue

            # Extracting information from each required td element
            second_td_span_text = tds[1].find('span').get_text(strip=True) if tds[1].find('span') else ''

            third_td_a_text = tds[2].find('a').get_text(strip=True) if tds[2].find('a') else ''
            third_td_time_title = tds[2].find('time').get('title') if tds[2].find('time') else ''

            fourth_td_a_text = tds[3].find('a').get_text(strip=True) if tds[3].find('a') else ''
            fourth_td_small_text = tds[3].find('small').get_text(strip=True) if tds[3].find('small') else ''

            fifth_td_img_src_list = [img['src'] for img in tds[4].find('div').find_all('img')] if tds[4].find(
                'div') else []

            sixth_td_img_src_list = [img['src'] for img in tds[5].find('div').find_all('img')] if tds[5].find(
                'div') else ''

            eighth_td_text = tds[7].get_text(strip=True)

            # Append the extracted data as a tuple
            all_data.append((
                second_td_span_text,
                third_td_a_text, third_td_time_title,
                fourth_td_a_text, fourth_td_small_text,
                fifth_td_img_src_list,
                sixth_td_img_src_list,
                eighth_td_text
            ))

        # Check if the <span class="next"> exists in the pagination
        next_span = soup.find('span', class_='next')
        if not next_span:
            print("No more next page. Exiting loop.")
            break

        # Move to the next page
        current_page += 1

        # Randomize delay between 15 and 60 seconds
        delay = random.uniform(base_delay, base_delay * 4)
        print(f"Delaying for {delay} seconds before the next request.")
        time.sleep(delay)

    return all_data


# Scraping the data from URL
url_to_scrape = "https://dotabuff.com/esports/matches"
result = scrape_data(url_to_scrape)

# Initialize column names for the extracted data
columns = [
        'League',
        'Match_ID', 'Date_Time',
        'Series', 'Region',
        'Won',
        'Lost',
        'Duration'
    ]

# Add the extracted data to a DataFrame
result_df = pd.DataFrame(result, columns=columns)

# Convert 'Match_ID' column to string for consistency
result_df['Match_ID'] = result_df['Match_ID'].astype(str)

# Drop duplicates based on the 'Match_ID' column
result_df = result_df.drop_duplicates(subset='Match_ID')

# Check if previously scraped data exists. If true, add the newly scraped data to it. If not, add it to a new DataFrame

# Specify the existing Excel file path
existing_excel_file_path = 'DOTA Esports Data.xlsx'

# Read the existing data from Excel into a DataFrame
try:
    existing_df = pd.read_excel(existing_excel_file_path)
except FileNotFoundError:
    # If the file doesn't exist, create an empty DataFrame
    existing_df = result_df

# Convert 'Match_ID' column to string for consistency
existing_df['Match_ID'] = existing_df['Match_ID'].astype(str)

# Concatenate the existing data and new data
combined_df = pd.concat([existing_df, result_df], ignore_index=True)

# Drop duplicates based on the 'Match_ID' column
combined_df = combined_df.drop_duplicates(subset='Match_ID')

# Write the combined data to Excel
combined_df.to_excel(existing_excel_file_path, index=False)

print(f"New data has been added to {existing_excel_file_path}")
