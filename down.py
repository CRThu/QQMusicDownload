import os

import requests


def extract_filename(url):
    return os.path.basename(url.split('?')[0])


def download_file(link, download_dir):
    filename = extract_filename(link)
    r = requests.get(link)
    song_path = os.path.join(download_dir, filename)
    with open(song_path, 'wb') as f:
        f.write(r.content)
        f.close()
    return filename, len(r.content)


def verify_file(songs_info, download_dir):
    song_path = os.path.join(download_dir, 'F000' + songs_info[3] + '.flac')
    if not os.path.exists(song_path):
        return False
    size = os.path.getsize(song_path)
    if size != songs_info[5]:
        return False
    else:
        return True
