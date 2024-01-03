import json


def get_list():
    with open('list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

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

        songs_info.append((i['songname'],
                           signer_names,
                           i['albumname'],
                           i['strMediaMid'],
                           song_type,
                           file_size))

    songs_info.sort(key=lambda x: (x[1], x[2]))

    # for song_info in songs_info:
    #    print(song_info)

    return songs_info
