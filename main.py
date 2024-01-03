from get_list import get_list,parse_list
from sixyin import search

get_list_json = get_list('[playlist_id]')
songs_info = parse_list(get_list_json)

# for song_info in songs_info:
#     print(song_info)
print(songs_info[0])

search_info = search(songs_info[0])

print(search_info)
