import subprocess
import re
from os.path import exists

ffmpeg_path = "C:\\Program Files\\ffmpeg-20200227-9b22254-win64-static\\bin\\ffmpeg.exe"
acceptable_sub_formats = ["subrip"]

language_codes = {"eng": "english"}


def merge_found_languages(list_a: list, list_b: list):
    for code in language_codes:
        if code in list_a:
            list_a.remove(code)
            list_a.append(language_codes[code])
        if code in list_b:
            list_b.remove(code)
            list_b.append(language_codes[code])
    for element in list_a:
        if element in list_b:
            continue
        else:
            list_b.append(element)
    return list_b


# This method returns all subtitle languages present in the file at file_path. If none exist, the list is empty
def get_subtitles_languages(file_path):
    if not exists(file_path):
        raise ValueError("There is no file at ", file_path)
    completed_process = subprocess.run([ffmpeg_path, "-i", file_path], capture_output=True)
    out = str(completed_process.stderr)
    # this pattern finds the subtitle language as group(1)
    pattern_a = r"Subtitle: subrip\\r\\n\s*Metadata:\\r\\n\s*title\s*: ([^\\]+)\\"
    pattern_b = r"Stream #\d:\d\(([^\)]+)\): Subtitle: subrip"
    found_a = re.findall(pattern_a, out)
    found_b = re.findall(pattern_b, out)
    found_any_subrips = re.search("Subtitle: subrip", out)
    if found_a or found_b:
        return merge_found_languages(found_a, found_b)
    elif found_any_subrips:
        return -1
    else:
        return None
