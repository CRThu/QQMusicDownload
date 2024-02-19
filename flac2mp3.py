import os

src_dir = os.path.join(".", "export")
ffmpeg_dir = os.path.join(".", "ffmpeg", "bin", "ffmpeg.exe")


# ffmpeg download at https://github.com/BtbN/FFmpeg-Builds/releases
# unzip ffmpeg-master-latest-win64-gpl-shared.zip to ./ffmpeg
# ffmpeg.exe is located at ./ffmpeg/bin

def convert_flac2mp3(i, fn, bitrate="320k"):
    print(f"{i + 1}: Convert {fn}.flac to {fn}.mp3")
    cmd = f"{ffmpeg_dir} -i \"{fn}.flac\" -b:a {bitrate} \"{fn}.mp3\""
    print(f'Command: {cmd}')
    ret = os.system(cmd)
    # if success, return 0
    if ret == 0:
        # Check if file exists
        # Check if file size is not 0
        if os.path.exists(f'{fn}.mp3') and os.path.getsize(f'{fn}.mp3') > 0:
            print(f"Deleted file: {fn}.flac")
            os.remove(f'{fn}.flac')
    return ret


def get_flac_filenames(d):
    flac_files = [os.path.splitext(f)[0] for f in os.listdir(d) if f.endswith('.flac')]
    # print("FLAC files:", flac_files)
    return flac_files


flac_list = get_flac_filenames(src_dir)

for idx, flac_fn in enumerate(flac_list):
    status = convert_flac2mp3(idx, os.path.join(src_dir, flac_fn), "192k")
    if status != 0:
        break
