import requests


def search(song_info):
    if 'sixyin_song_id' in song_info.keys():
        return

    song_search_kw = '{0}+{1}+{2}'.format(song_info['songname'], song_info['signernames'], song_info['albumname'])

    url = "https://api.itooi.cn/tencent/search"
    headers = {}
    params = {"type": "song",
              # "keyword": "听见下雨的声音+魏如昀+听见下雨的声音 电影原声带"}
              "keyword": song_search_kw}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    song_id = result['data']['list'][0]['id']
    song_name = result['data']['list'][0]['name']
    song_singer = str.join('|', [signer for signer in result['data']['list'][0]['singers']])
    song_album = result['data']['list'][0]['albumName']

    song_info['sixyin_song_id'] = song_id
    song_info['sixyin_song_name'] = song_name
    song_info['sixyin_song_singer'] = song_singer
    song_info['sixyin_song_album'] = song_album


def verify_key(key):
    url = "https://api.itooi.cn/unlock/" + key
    headers = {}
    params = {}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    # print(result['code'])
    # print(result['msg'])
    return True if result['code'] == 200 else False


def get_download_link(song_info, key):
    url = "https://api.itooi.cn/tencent/url"
    headers = {'Unlockcode': key}
    params = {'id': song_info['sixyin_song_id'],
              'quality': song_info['songtype'],
              'isRedirect': '0'}  # 是否直接下载

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    song_info['download_link'] = result['data'][0]

    if result['code'] == 400:
        return None
    else:
        return result['data'][0]
