import os

from get_list import get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link

playlist_id = '3222851321'
cache_path = './cache/'
paylist_raw_json_path = os.path.join(cache_path, 'playlist.{0}.raw.json'.format(playlist_id))
paylist_info_json_path = os.path.join(cache_path, 'playlist.{0}.json'.format(playlist_id))

if not os.path.exists(cache_path):
    os.makedirs(cache_path)

playlist_raw = get_list(playlist_id)
store_json(paylist_raw_json_path, playlist_raw)
# get_playlist_raw = load_json(paylist_raw_json_path)

songs_info = parse_list(playlist_raw)
store_json(paylist_info_json_path, songs_info)
# songs_info = load_json(paylist_info_json_path)


# for song_info in songs_info:
#     print(song_info)
# print(songs_info[0])

search_info = search(songs_info[0])

print(search_info)

print('key 1234: ', verify_key('1234'))
print('key 2043: ', verify_key('2043'))

link = get_download_link(songs_info[0], search_info, '2043')
print(link)
