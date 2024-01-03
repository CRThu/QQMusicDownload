from get_list import get_list
from sixyin import search

songs_info = get_list()

# for song_info in songs_info:
#     print(song_info)
print(songs_info[0])

search_info = search(songs_info[0])

print(search_info)
