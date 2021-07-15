import argparse
import os
import patoolib
import subtitleChecker


def check_subtitles():
    all_files_contain_english_subrips = True
    all_files_contain_subrips = True
    files_without_subs = []
    files_without_en_subs = []
    for root, dirs, files in os.walk(args.target_dir):
        for filename in files:
            file = os.path.join(root, filename)
            for file_ending in video_file_endings:
                if file.endswith(".{0}".format(file_ending)):
                    languages = subtitleChecker.get_subtitles_languages(file)
                    if not languages:
                        files_without_subs.append(file)
                        all_files_contain_subrips = False
                    elif languages == -1:
                        files_without_en_subs.append(file)
                        all_files_contain_english_subrips = False
                    else:
                        found_english = False
                        for subtitle_language in languages:
                            if subtitle_language == "english":
                                found_english = True
                                break
                        if not found_english:
                            files_without_en_subs.append(file)
    if all_files_contain_english_subrips:
        print("All files in {0} contain English subrips!".format(args.source_dir))
        return
    elif all_files_contain_subrips:
        print("All files in {0} contain subrips!".format(args.source_dir))
    else:
        if files_without_subs:
            print("\033[31mThese files do not contain any subrips:\033[m")
            for file_name in files_without_subs:
                print(file_name)
        if files_without_en_subs:
            print("\033[31mThese files do not contain english subrips:\033[m")
            for file_name in files_without_en_subs:
                print(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dir', type=str, help='path to dir to check')
    parser.add_argument('target_dir', type=str, help='path to dir for extraction')
    args = parser.parse_args()
    archive_file_endings = ["zip", "rar"]
    video_file_endings = ["mkv"]
    if not os.path.isdir(args.source_dir):
        print("source_dir does not exist")
        quit()
    if not os.path.isdir(args.target_dir):
        os.mkdir(args.target_dir)
    # extracing:
    for root, dirs, files in os.walk(args.source_dir):
        for filename in files:
            file = os.path.join(root, filename)
            for file_ending in archive_file_endings:
                if file.endswith(".{0}".format(file_ending)):
                    patoolib.extract_archive(file, outdir=args.target_dir + '\\extracts')

    check_subtitles()
