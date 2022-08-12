
"""

Script to copy a single file over, waiting for a new file to occur and then start with the next file.

"""
from pathlib import Path
from time import sleep, perf_counter_ns

import shutil


def main(work_dir: Path, file_list: list[Path]):
    asking: str = ""
    time_spend: list = [perf_counter_ns()]
    print("Files to process:")
    print("-"*40)
    print("\n".join([file.name for file in file_list]))
    print()
    print("Proces:")
    print("-"*40)
    for idx, file in enumerate(file_list):

        print(f"[{idx+1}/{len(file_list)}] Copy file {file} to {work_dir}")

        if asking != "a":
            asking = input("Go On [y/n/a]")

        if asking == "n":
            continue

        work_file = work_dir / file.name

        waiting_for_file = f"{file.stem}*.log"
        print(list(work_dir.glob(waiting_for_file)))
        if any(waiting_for_file[:-5] in s.stem for s in list(work_dir.glob(waiting_for_file))):
            print(f"Skipping {file}...")
            continue

        shutil.copy(file, work_file)

        print(f"Waiting for file: {waiting_for_file} to be computed... ")

        while not any(waiting_for_file[:-5] in s.stem for s in list(work_dir.glob(waiting_for_file))):
            sleep(0.3)

        print(
            f"Finished {file} in {(time_spend[-1]-perf_counter_ns())/1000000000} seconds"
        )
        time_spend.append(perf_counter_ns())
    else:
        print(f"Finished working on all {len(file_list)}.")
        print(f"Time used { (time_spend[-1]-time_spend[0])/1000000000 } seconds")
        print()
        while True:
            close = input('Press Y to exit.')
            if close.upper() == 'Y':
                exit('Leaving Ebokssender')


def read_input(ask: str) -> Path:
    """
    Typical directories is:
    \\\\civil.aau.dk\\Fileshares\\ease\\Udsendelse
    "c:\\Strålfors Files\\MaxiHotfolder\"
    """

    while True:
        read = input(f"{ask} > ")
        directory = Path(read)
        if directory.exists():
            return directory
        else:
            print("Directory dosent exists")


if __name__ == "__main__":
    print(read_input.__doc__)

    data_dir = read_input("Path for pdf's to send")

    working_directory = read_input("Working directory (Maxihotfolder)")

    list_of_files: list = sorted([file for file in data_dir.glob("*.pdf")])

    main(working_directory, list_of_files)
