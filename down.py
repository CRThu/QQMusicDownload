import os

import requests

download_proxies = {
    'http': '',
    'https': '',
}


def extract_filename(url):
    return os.path.basename(url.split('?')[0])


def download_file(songs_info, download_dir):
    if 'download_link' not in songs_info.keys():
        songs_info['download_done'] = False
        return False

    # 若文件存在且校验通过则跳过下载
    if verify_file(download_dir, songs_info):
        print('存在歌曲，已跳过下载')
        return True

    filename = songs_info['strMediaMid']
    r = requests.get(songs_info['download_link'], proxies=download_proxies)
    song_path = os.path.join(download_dir, filename)
    with open(song_path, 'wb') as f:
        f.write(r.content)
        f.close()

    songs_info['download_path'] = filename
    songs_info['download_done'] = True

    verify = verify_file(download_dir, songs_info)
    songs_info['download_verify'] = verify
    return verify


def verify_file(down_dir, songs_info):
    if 'download_path' not in songs_info.keys():
        return False
    song_path = os.path.join(down_dir, songs_info['download_path'])
    if not os.path.exists(song_path):
        return False
    size = os.path.getsize(song_path)
    if size != songs_info['filesize']:
        return False
    else:
        return True
