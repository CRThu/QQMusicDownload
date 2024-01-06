import os

import requests

from down import extract_filename, download_file, verify_file
from get_list import get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link

playlist_id = '9118888178'
cache_dir = './cache'
music_dir = './music'
paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

if not os.path.exists(music_dir):
    os.makedirs(music_dir)

playlist_raw = get_list(playlist_id)
store_json(paylist_raw_json_path, playlist_raw)
# get_playlist_raw = load_json(paylist_raw_json_path)

songs_info = parse_list(playlist_raw)
store_json(paylist_info_json_path, songs_info)
# songs_info = load_json(paylist_info_json_path)


# for song_info in songs_info:
#     print(song_info)
print(songs_info[0])

search_info = search(songs_info[0])

print(search_info)

# 需通过flac.life官网免费获取解锁码
print('key 1234: ', verify_key('1234'))
print('key 2043: ', verify_key('2043'))

link = get_download_link(songs_info[0], search_info, '2043')
print(link)

# (filename, filesize) = download_file(link, music_dir)
# print(filename, filesize)

stat = verify_file(songs_info[0], music_dir)
print(stat)
