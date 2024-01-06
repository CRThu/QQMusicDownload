import requests


def search(song_info):
    song_search_kw = '{0}+{1}+{2}'.format(song_info[0], song_info[1], song_info[2])

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

    search_info = (song_id, song_name, song_singer, song_album)
    # print(search_info)
    return search_info


def verify_key(key):
    url = "https://api.itooi.cn/unlock/" + key
    headers = {}
    params = {}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    # print(result['code'])
    # print(result['msg'])
    return True if result['code'] == 200 else False


def get_download_link(song_info, search_info, key):
    url = "https://api.itooi.cn/tencent/url"
    headers = {'Unlockcode': key}
    params = {'id': search_info[0],
              'quality': song_info[4],
              'isRedirect': '0'}  # 是否直接下载

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if result['code'] == 400:
        return None
    else:
        return result['data'][0]
