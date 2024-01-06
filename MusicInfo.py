class MusicInfo:
    def __init__(self):
        # FROM QQ MUSIC INTERFACE
        self.song_name = None
        self.signer_names = None
        self.album_name = None
        self.qq_music_str_media_mid = None
        self.song_type = None
        self.file_size = None
        # FROM SIXYIN INTERFACE
        self.sixyin_song_id = None
        self.sixyin_song_name = None
        self.sixyin_song_singer = None
        self.sixyin_song_album = None
        # DOWNLOAD LINK
        self.download_link = None
        self.download_filename = None
        self.download_done = False
        self.download_verify = False
