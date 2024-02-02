import json
import os
import re
import shutil

from down import verify_file
from json_oper import load_json, store_json

playlist_id = '3222851321'  # QQ音乐歌单ID，通过分享获取
cache_dir = './cache'
music_dir = './music'
export_dir = './export'
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))
map_info_json_path = os.path.join(cache_dir, 'map.{0}.json'.format(playlist_id))
songs_format = '{signernames} - {songaliasname}'


# songs_format = '{signernames} - {songaliasname} - {albumname}'


def check_fail(songs_info):
    for song_info in songs_info:
        if not ('download_done' in song_info.keys() \
                and song_info['download_done'] == True \
                and 'download_verify' in song_info.keys() \
                and song_info['download_verify'] == True):
            print('FAIL at', song_info['signernames'], '-', song_info['songaliasname'])
        else:
            pass
            # print('PASS at', song_info['signernames'], '-', song_info['songaliasname'])


def check_duplicate(songs_info):
    seen = {}
    for song_info in songs_info:
        val = song_info['signernames'] + ' - ' + song_info['songaliasname']
        if val is not None and val in seen:
            seen[val] = seen[val] + 1
            print(f"Duplicate {seen[val]} songs found in dictionary: {val}")
        else:
            seen[val] = 1


def sanitize_path(path):
    return re.sub(r'[\\/*?:"<>|]', "", path)


def export_files(export_dir, src_dir, songs_info, mapping_file):
    songs_info_dict = {v['strMediaMid']: v for v in songs_info}
    songs_info_id_filename_mapper = dict()

    # 生成映射字典
    for song_info in songs_info:
        filename = songs_format.format_map(song_info).replace("|", " ")
        fileext = ('.flac' if song_info['songtype'] == 'flac' else '.mp3')
        songs_info_id_filename_mapper[song_info['strMediaMid']] = sanitize_path(f'{filename}{fileext}')

    # 重命名相同歌名
    seen = {}
    for id, fn in songs_info_id_filename_mapper.items():
        val = fn
        if val is not None and val in seen:
            seen[val] = seen[val] + 1
            parts = fn.rsplit('.', 1)
            songs_info_id_filename_mapper[id] = f'{parts[0]}{seen[val]}.{parts[1]}'
        else:
            seen[val] = 1

    # 保存映射文件
    store_json(mapping_file, songs_info_id_filename_mapper)

    # 导出文件夹
    # Create destination folder if it doesn't exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    else:
        print('导出文件夹已存在，请删除后重试')
        return

    # Copy all files from source folder to destination folder
    for idx, (src_fn, export_fn) in enumerate(songs_info_id_filename_mapper.items()):
        source_path = os.path.join(src_dir, src_fn)
        destination_path = os.path.join(export_dir, export_fn)
        shutil.copy(source_path, destination_path)
        print(f"{idx + 1}: Copied {source_path} to {destination_path}")


songs_info = load_json(paylist_info_json_path)
check_fail(songs_info)
for i in songs_info:
    verify = verify_file(music_dir, i)
    if not verify:
        print('VERIFY FAILED :{0}-{1}'.format(i['signernames'], i['songname']))
check_duplicate(songs_info)
export_files(export_dir, music_dir, songs_info, map_info_json_path)
