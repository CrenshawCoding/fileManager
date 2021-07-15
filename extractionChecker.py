import patoolib
import os

archive_file_endings = ["zip", "rar"]


def extract_archive_in_dir(source_dir, target_dir="./extraction"):
    for filename in os.listdir(source_dir):
        file = os.path.join(source_dir, filename)
        # checking if it is a file
        if os.path.isfile(file):
            for file_ending in archive_file_endings:
                if file.endswith(".{0}".format(file_ending)):
                    patoolib.extract_archive(file, outdir=target_dir)


patoolib.extract_archive()
