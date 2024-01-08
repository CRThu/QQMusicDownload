import os
import time

import requests
from requests.adapters import HTTPAdapter, Retry

from down import download_file
from get_list import merge_songs_info, get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link, reset_verify_failed_songs_info

playlist_id = '3222851321'  # QQ音乐歌单ID，通过分享获取
# playlist_id = '9118888178'  # QQ音乐歌单ID，通过分享获取
unlock_key = 'A222'  # 需通过flac.life官网免费获取解锁码
cache_dir = './cache'
music_dir = './music'
start_at_index = 0
paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

if not os.path.exists(music_dir):
    os.makedirs(music_dir)

session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

# 需通过flac.life官网免费获取解锁码
stat = verify_key(unlock_key)
print('key verify: ', stat)
if stat is False:
    raise Exception()

# 加载播放列表原始文件
playlist_raw = get_list(playlist_id)
store_json(paylist_raw_json_path, playlist_raw)
# playlist_raw = load_json(paylist_raw_json_path)

# 解析播放列表
songs_info = parse_list(playlist_raw)
old_songs_info = load_json(paylist_info_json_path)
merge_songs_info(songs_info, old_songs_info)
store_json(paylist_info_json_path, songs_info)
# songs_info = load_json(paylist_info_json_path)

# for song_info in songs_info:
#     print(song_info)
# print(songs_info[0])
print('歌曲数量:', len(songs_info))

# reset_verify_failed_songs_info(songs_info)
# store_json(paylist_info_json_path, songs_info)

for i, song_info in enumerate(songs_info):
    if i < start_at_index:
        print('{0}/{1}: JUMP'.format(i + 1, len(songs_info)))
        continue

    # 搜索歌曲
    print('{0}/{1}: SEARCH {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    search(song_info)

    # 获取歌曲链接
    print('{0}/{1}: GETLINK {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    get_download_link(song_info, unlock_key)
    # print(song_info)

    print('{0}/{1}: DOWNLOAD {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    download_file(song_info, music_dir)
    store_json(paylist_info_json_path, songs_info)

    print('{0}/{1}: SUCCESS {2}'.format(i + 1, len(songs_info), song_info))
