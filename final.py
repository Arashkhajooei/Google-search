from googlesearch import search
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import os


class KeywordScraper:
    def __init__(self):
        self.keyword = None
        self.num_results = None
        self.batch_size = None
        self.save_path = None
        self.results = []

    def get_user_input(self):
        try:
            self.keyword = input("Enter the keyword: ")
            self.num_results = int(
                input("Enter the number of results to scrape: "))
            self.batch_size = int(input("Enter the batch size: "))
            self.save_path = input(r"Enter the path: ")
        except ValueError:
            print("Invalid input. Please enter valid values.")
            self.get_user_input()

    def search_keywords(self):
        remaining_results = self.num_results
        start_index = 0  # Start index for each batch
        while remaining_results > 0:
            batch_num = min(self.batch_size, remaining_results)
            results = list(search(self.keyword, tld="co.in",
                           num=start_index + batch_num, start=start_index, pause=1))
            self.results.extend(results[start_index:])

            start_index += batch_num
            remaining_results -= batch_num

    def scrape_keyword_occurrences(self):
        data = []

        count = 0
        for url in self.results:
            if count >= self.num_results:
                break

            try:
                print("Requesting URL:", url)
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text()
                    occurrences = text.lower().count(self.keyword.lower())
                else:
                    occurrences = 0

                data.append([url, occurrences])
                time.sleep(1)
                count += 1
            except requests.exceptions.RequestException as e:
                print(f"Error occurred for URL: {url} - {e}")
                continue  # Skip to the next iteration if there is an error

        df = pd.DataFrame(data, columns=['URL', 'Occurrences'])
        return df

    def write_to_csv(self, df):
        # df.to_csv(self.save_path, index=False)
        df.to_csv(os.path.join(self.save_path, r'out.csv'), index=False)

    def run_scraper(self):
        self.get_user_input()
        self.search_keywords()
        df = self.scrape_keyword_occurrences()
        self.write_to_csv(df)


scraper = KeywordScraper()
scraper.run_scraper()
