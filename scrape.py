import requests
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess
import os
from urllib.parse import urljoin




# scrape the download links from the website
# write in links.txt
def get_video_links(adds):
    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "soups"
    output_path.mkdir(parents=True, exist_ok=True)

    download_links = []
    for add in adds:
        
        response = requests.get(add)
        soup = BeautifulSoup(response.content, 'html.parser')

        # download link
        ### https://archive.org/download/moomin-season-3/%5BMoomin%20Master%5D%20Moomin%20season%203/MOOMIN%2028%20The%20Floating%20Theatre.mp4
        # url fetched
        ### <a href="MOOMIN%2014%20Our%20Neighbor%20is%20a%20Tough%20Teacher.mp4">MOOMIN 14 Our Neighbor is a Tough Teacher.mp4</a>
        for link in soup.find_all('a'):
            # print(link)
            href = link.get('href')
            if href and '.mp4' in href:
                href = urljoin(add, href) ### join the base url with the href
                download_links.append(href)
    
    with open(output_path / "links.txt", "w") as f:
        for link in download_links:
            f.write(link + "\n")

def download_videos():
    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "videos"
    output_path.mkdir(parents=True, exist_ok=True)

    with open( base_dir/ "soups/links.txt", "r") as f:
        links = f.readlines()

    for link in links:
        ## MOOMIN%2001%20Spring%20in%20Moomin%20Valley
        link = link.strip()
        file_name = link.split("/")[-1]
        file_name = file_name.replace("%20", "_")
        path = output_path / file_name

        if os.path.exists(path):
            print(f"{file_name} already downloaded.")
            continue

        print(f"Start downloading {file_name}...")
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"----------------- downloaded.")


if __name__ == "__main__":

    adds = ['https://archive.org/download/moomin-season-1/%5BMoomin%20Master%5D%20Moomin%20season%201/',
        'https://archive.org/download/moomin-season-2/%5BMoomin%20Master%5D%20Moomin%20Season%202/',
        'https://archive.org/download/moomin-season-3/%5BMoomin%20Master%5D%20Moomin%20season%203/']

    # get_video_links(adds)
    download_videos()



