import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from halo import Halo

load_dotenv()


def get_songs_per_date(date: str):
    spinner = Halo(text='Getting songs from web', spinner='dots')
    spinner.start()
    # generate url per date
    url = os.getenv('BILLBOARD_URL') + date
    response = requests.get(url)
    # get page
    soup = BeautifulSoup(response.text, 'html.parser')
    # get all songs
    songs = soup.find_all(class_='o-chart-results-list-row-container')

    names = []

    # loop through all gotten songs
    for song in songs:
        # get infos of song
        nameObj = song.find(class_='c-title')
        name = nameObj.text.strip()
        author = nameObj.find_next('span', class_='c-label').text.strip()
        names.append({
            'name': name,
            'author': author
        })
    spinner.stop()
    return names
