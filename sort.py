import sys
from pathlib import Path
import os
import shutil
import re

CATEGORIES = {"audio": [".mp3", ".wav", ".flac", ".wma"],
              "video": [".mkv", ".avi", ".mov", ".mp4"],
              "images": [".jpeg", ".png", ".jpg", ".svg"],
              "archives": [".zip", ".gz", ".tar"],
              "docs": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"]
              }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(file: Path):
    new_name = file.name.translate(TRANS)
    new_name = re.sub(r"[^a-z0-9A-Z.]", "_", new_name)
    return new_name


def write_in_file(list: list, path: Path):
    ...


def get_category(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def unpack_archive(path: Path):
    ...


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
        # file_name = category + ".txt"
        # with open(target_dir.joinpath(file_name), "w") as fh:
        #     ...
    new_path = target_dir.joinpath(normalize(file))
    if not new_path.exists():
        file.replace(new_path)
        if category == "archives":
            unpack_archive(new_path)


def sort_folder(path: Path) -> None:
    for i in path.glob("**/*"):
        if i.is_file():
            category = get_category(i)
            move_file(i, category, path)


def delete_empty_folders(path: Path):
    for i in path.glob("**/*"):
        if i.is_dir() and not os.listdir(i):
            i.rmdir()


def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path entered"

    if not path.exists():
        return "Path does not exists"

    sort_folder(path)
    delete_empty_folders(path)

    return "All Ok"


if __name__ == "__main__":
    main()
