import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to scrape data from a given URL and save it to a CSV file
def scrape_monarch_data(url):
    # Step 1: Send a GET request to fetch the content of the page
    response = requests.get(url)

    # Step 2: Check if the request was successful (status code 200 means success)
    if response.status_code == 200:
        # Step 3: Parse the HTML content using BeautifulSoup for easy navigation
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 4: Locate the first table on the page, which contains the monarch sightings data
        table = soup.find('table')

        if table is not None:  # Check if a table was found
            # Step 5: Initialize an empty list to hold the extracted data rows
            rows = []

            # Step 6: Loop through all rows in the table, starting from the second row (skipping header)
            for tr in table.find_all('tr')[1:]:
                # Extract all cells in the current row
                cells = tr.find_all('td')

                # Ensure the row has enough columns before extracting data
                if len(cells) > 3:
                    # Step 7: Extract and clean the relevant data from each cell (removing extra whitespace)
                    date = cells[1].text.strip()  # Date of the sighting
                    town = cells[2].text.strip()  # Town where the sighting occurred
                    state = cells[3].text.strip()  # State where the sighting occurred
                    latitude = cells[4].text.strip()  # Latitude of the sighting location
                    longitude = cells[5].text.strip()  # Longitude of the sighting location
                    sighting = cells[6].text.strip()  # Number of sightings

                    # Append the cleaned data as a new row in the list
                    rows.append([date, state, town, longitude, latitude, sighting])

            # Step 8: Create a Pandas DataFrame using the list of rows
            df = pd.DataFrame(rows, columns=["Date", "State", "Town", "Longitude", "Latitude", "Sighting"])

            # Generate a unique file name based on the year and map type from the URL
            if 'season=' in url and 'map=' in url and 'year=' in url:
                season = url.split('season=')[1].split('&')[0]  # Get the season (spring or fall)
                map_type = url.split('map=')[1].split('&')[0]  # Get the map type (monarch-adult or monarch-egg)
                year = url.split('year=')[1].split('&')[0]  # Get the year

                # Create a file name using the season, map type, and year
                filename = f"{map_type}_{season}_{year}.csv"
            else:
                filename = "monarch_data.csv"  # Default name if URL is unexpected

            # Step 9: Save the DataFrame to a CSV file
            df.to_csv(filename, index=False)
            print(f"Data successfully saved to {filename}")

        else:
            print("No data table found on the page.")
    else:
        # If the request failed, print the status code for debugging purposes
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# List of URLs to scrape
urls = [
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-adult-fall&year=2023&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-egg-fall&year=2023&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=milkweed-fall&year=2023&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=milkweed&year=2023&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-adult-spring&year=2023&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-egg-spring&year=2023&submit=View+Data',
    
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-adult-fall&year=2022&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-egg-fall&year=2022&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=milkweed-fall&year=2022&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=milkweed&year=2022&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-adult-spring&year=2022&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-egg-spring&year=2022&submit=View+Data',

    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-adult-fall&year=2021&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=monarch-egg-fall&year=2021&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=fall&map=milkweed-fall&year=2021&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=milkweed&year=2021&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-adult-spring&year=2021&submit=View+Data',
    'https://journeynorth.org/sightings/querylist.html?season=spring&map=monarch-egg-spring&year=2021&submit=View+Data',
    # Add more URLs as needed
]

# Step 10: Loop through the URLs and scrape data for each
for url in urls:
    scrape_monarch_data(url)

# Optional: Print the current working directory to confirm where the CSV files are saved
print(f"Data saved in: {os.getcwd()}")