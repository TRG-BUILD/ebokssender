from pathlib import Path
from time import sleep

import shutil


def main(data_dir, work_dir, file_file):
    for file in file_list:
        print(f"Copy file {file} to {work_dir}")
        org_file = data_dir / f"{file}.pdf"
        work_file = work_dir / f"{file}.pdf"

        waiting_for_file = work_dir / f"{file}.txt"

        if waiting_for_file.exists():
            print(f"Skipping {org_file}...")
            continue
        shutil.copy(org_file, work_file)

        print(f"Waiting for file: {waiting_for_file} to be computed... ")

        while not waiting_for_file.exists():
            sleep(0.3)

        print(f"Finished {org_file} ")
    else:
        print(f"Finished working on all {len(file_list)}.")


if __name__ == "__main__":
    data_dir = Path("../test/data")

    work_dir = Path("../test/work")

    file_list = sorted([file.stem for file in data_dir.glob("*.pdf")])

    main(data_dir, work_dir, file_file)
