import requests


def get_list(playlist_id):
    url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_playlist_cp.fcg"
    headers = {}
    params = {"format": "json",
              "id": playlist_id}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    return result


def parse_list(data):
    arr = data['data']['cdlist'][0]['songlist']
    songs_info = []

    for i in arr:
        signer_names = str.join('|', [signer['name'] for signer in i['singer']])
        song_type = None
        file_size = 0
        if i['sizeflac'] != 0:
            song_type = 'flac'
            file_size = i['sizeflac']
        elif i['size320'] != 0:
            song_type = '320'
            file_size = i['size320']
        elif i['size128'] != 0:
            song_type = '128'
            file_size = i['size128']
        else:
            raise Exception('{0} 未找到相应解析度的音乐'.format(i['songname']))

        m = dict()
        m['songname'] = i['songorig']
        m['songaliasname'] = i['songname']
        m['signernames'] = signer_names
        m['albumname'] = i['albumname']
        m['strMediaMid'] = i['strMediaMid']
        m['songtype'] = song_type
        m['filesize'] = file_size

        songs_info.append(m)

    songs_info.sort(key=lambda x: (x['signernames'], x['albumname']))

    # for song_info in songs_info:
    #    print(song_info)

    return songs_info


def merge_songs_info(new_songs_info, old_songs_info):
    old_dicts = {v['strMediaMid']: v for v in old_songs_info}

    for n in new_songs_info:
        if n['strMediaMid'] in old_dicts:
            match_old_dict = old_dicts[n['strMediaMid']]

            if 'sixyin_song_id' in match_old_dict.keys():
                n['sixyin_song_id'] = match_old_dict['sixyin_song_id']
                n['sixyin_song_name'] = match_old_dict['sixyin_song_name']
                n['sixyin_song_singer'] = match_old_dict['sixyin_song_singer']
                n['sixyin_song_album'] = match_old_dict['sixyin_song_album']
            if 'download_link' in match_old_dict.keys():
                n['download_link'] = match_old_dict['download_link']
            if 'download_path' in match_old_dict.keys():
                n['download_path'] = match_old_dict['download_path']
                n['download_done'] = match_old_dict['download_done']
                n['download_verify'] = match_old_dict['download_verify']