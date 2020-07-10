"""
Collects all image URLs from a soup.io account (and all related accounts, while it's at it).
Can be interrupted and will resume from last successful URL.

Needs two dependencies:

    pip install requests beautifulsoup4

Call this file with your soup name:

    python ripsoup.py yoursoupname

The URLs are put into a text file, which you can then download with

    wget -nc -i data/yoursoupname/image_urls
"""
import os
import sys
from contextlib import suppress
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SOUP = sys.argv[-1]
if "." in SOUP:
    print(
        "Invalid soup name. Please call this script like this: python ripsoup.py mysoupname"
    )
URL_FILE = f"data/{SOUP}/last_successful_url"
IMAGE_FILE = f"data/{SOUP}/image_urls"
SOUP_FILE = f"data/{SOUP}/related_soups"


def save_image_data(images):
    with open(IMAGE_FILE, "w+") as f:
        content = "\n".join(images)
        f.write(content)


def get_src(url):
    path = Path(url)
    if path.stem.endswith("_500"):
        extension = path.suffix
        url = url[:-(len(extension) + len("_500"))] + extension
    return url


def get_page_data(url, images, soups, session):
    fail_counter = -1
    response = None
    while not response or not response.status_code == 200:
        fail_counter += 1
        with suppress(Exception):
            response = session.get(url, timeout=10000)
    if fail_counter > 1:
        print(f"{fail_counter} fails before getting {url}")

    soup = BeautifulSoup(response.content.decode(), "html.parser")

    posts = soup.select(".post")
    for post in posts:
        soups |= set(
            [
                img.attrs.get("alt")
                for img in post.select(".content .source .user_container img")
            ]
        )
        for image in post.select(".content .description img"):
            images.append(get_src(image.attrs.get("src")))
        for image in post.select(".content .imagecontainer img"):
            images.append(get_src(image.attrs.get("src")))

    next_url = soup.select(".pagination a.more")
    if next_url:
        next_url = next_url[0].attrs.get("href")
        next_url = f"https://{SOUP}.soup.io{next_url}" if next_url else None

    save_image_data(images)
    with open(URL_FILE, "w+") as f:
        f.write(next_url)

    return next_url, images, soups


def get_all_data(start_url):
    current_url = start_url
    session = requests.Session()
    related_soups = set()
    image_urls = list()
    while current_url:
        current_url, image_urls, related_soups = get_page_data(
            current_url, image_urls, related_soups, session=session,
        )
        print(".", end="")

    with open(SOUP_FILE, "w+") as f:
        f.write("\n".join(sorted(list(related_soups))))


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs(f"data/{SOUP}", exist_ok=True)
    Path(URL_FILE).touch()
    get_all_data(start_url=open(URL_FILE).read() or f"https://{SOUP}.soup.io")
