import os

src_dir = os.path.join(".", "export")
ffmpeg_dir = os.path.join(".", "ffmpeg", "bin", "ffmpeg.exe")


# ffmpeg download at https://github.com/BtbN/FFmpeg-Builds/releases
# unzip ffmpeg-master-latest-win64-gpl-shared.zip to ./ffmpeg
# ffmpeg.exe is located at ./ffmpeg/bin

def convert_flac2mp3(fn, bitrate="320k"):
    cmd = f"{ffmpeg_dir} -i \"{fn}.flac\" -b:a {bitrate} \"{fn}.mp3\""
    print(cmd)
    ret = os.system(cmd)
    # if success, return 0
    return ret


def get_flac_filenames(d):
    flac_files = [os.path.splitext(f)[0] for f in os.listdir(d) if f.endswith('.flac')]
    # print("FLAC files:", flac_files)
    return flac_files


flac_list = get_flac_filenames(src_dir)
for flac_fn in flac_list:
    convert_flac2mp3(os.path.join(src_dir, flac_fn), "320k")
