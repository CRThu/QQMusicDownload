import json
import os
import re

from json_oper import load_json, store_json

playlist_id = '3222851321'  # QQ音乐歌单ID，通过分享获取
cache_dir = './cache'
music_dir = './test_music'
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))
map_info_json_path = os.path.join(cache_dir, 'map.{0}.json'.format(playlist_id))
songs_format = '{signernames} - {songaliasname} - {albumname}'


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


def rename_files(directory, songs_info, mapping_file):
    songs_info_dict = {v['strMediaMid']: v for v in songs_info}
    songs_info_id_filename_mapper = dict()

    for song_info in songs_info:
        filename = songs_format.format_map(song_info).replace("|", " ")
        fileext = ('.flac' if song_info['songtype'] == 'flac' else '.mp3')
        songs_info_id_filename_mapper[song_info['strMediaMid']] = sanitize_path(f'{filename}{fileext}')

    store_json(mapping_file, songs_info_id_filename_mapper)

    # TODO
    # for file in os.listdir(directory):
    #     if file in songs_info_dict.keys():
    #         rename_filename = (songs_format.format_map(songs_info_dict[file])
    #                            + ('.flac' if songs_info_dict[file]['songtype'] == 'flac' else '.mp3')) \
    #             .replace("|", " ")
    #         rename_filename = sanitize_path(rename_filename)
    #         os.rename(os.path.join(directory, file), os.path.join(directory, rename_filename))
    #         print(f'Renamed {file} -> {rename_filename}')


songs_info = load_json(paylist_info_json_path)
check_fail(songs_info)
check_duplicate(songs_info)
# rename_files(music_dir, songs_info, map_info_json_path)
