import json
import os
import re

from json_oper import load_json, store_json

playlist_id = '3222851321'  # QQ音乐歌单ID，通过分享获取
cache_dir = './cache'
music_dir = './test_music'
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))
map_info_json_path = os.path.join(cache_dir, 'map.{0}.json'.format(playlist_id))
songs_format = '{signernames} - {songname} - {albumname}'


def sanitize_path(path):
    return re.sub(r'[\\/*?:"<>|]', "", path)


def rename_files(directory, playlist_file, mapping_file):
    songs_info = load_json(playlist_file)
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


rename_files(music_dir, paylist_info_json_path, map_info_json_path)
