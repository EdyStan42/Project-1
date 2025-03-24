import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

SAVE_FOLDER = 'DownloadedLogos2'


# Ensure directory exists
def create_directory(directory):
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.mkdir(directory)
    else:
        print(f"Directory already exists: {directory}")



def extract_base_domain(domain):
    return domain.split('.')[0]



def download_images_from_domains(parquet_file):

    try:
        df = pd.read_parquet(parquet_file)
    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        return

    if "domain" not in df.columns:
        print("The Parquet file must contain a 'domain' column.")
        return


    create_directory(SAVE_FOLDER)

    for domain in df["domain"]:

        base_domain = extract_base_domain(domain)


        search_query = f"{base_domain} logo"
        searchurl = GOOGLE_IMAGE + 'q=' + search_query.replace(" ", "+")
        print(f"Searching for: {search_query}")

        try:

            response = requests.get(searchurl, headers=usr_agent)
            response.raise_for_status()
            html = response.text


            soup = BeautifulSoup(html, 'html.parser')
            print(f"Parsing results for {base_domain}...")


            image_links = []
            for link in soup.find_all('img'):
                image_url = link.get('data-src') or link.get('src')
                if image_url and image_url.startswith("http"):
                    image_links.append(image_url)


            if image_links:
                try:
                    image_response = requests.get(image_links[0])
                    image_response.raise_for_status()
                    image_path = os.path.join(SAVE_FOLDER, f"{domain}.jpg")
                    with open(image_path, 'wb') as file:
                        file.write(image_response.content)
                    print(f"Image saved for {base_domain}: {image_path}")
                except Exception as e:
                    print(f"Failed to download image for {base_domain}: {e}")
            else:
                print(f"No images found for {base_domain}.")

        except Exception as e:
            print(f"Error searching for {base_domain}: {e}")



if __name__ == '__main__':
    parquet_file = r"D:\Veridio\logos.snappy.parquet" # Replace with your Parquet file path
    download_images_from_domains(parquet_file)