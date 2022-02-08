"""

Script to copy a single file over, waiting for a new file to occur and then start with the next file.

"""
from pathlib import Path
from time import sleep, perf_counter_ns

import shutil


def main(work_dir: Path, file_list: list[Path]):
    asking: str = ""
    time_spend: list = [perf_counter_ns()]
    for file in file_list:
        print(f"Copy file {file} to {work_dir}")

        if asking != "a":
            asking = input("Go On [y/n/a]")

        if asking == "n":
            continue

        work_file = work_dir / file.name

        waiting_for_file = work_dir / f"{file.stem}.txt"

        if waiting_for_file.exists():
            print(f"Skipping {file}...")
            continue

        shutil.copy(file, work_file)

        print(f"Waiting for file: {waiting_for_file} to be computed... ")

        while not waiting_for_file.exists():
            sleep(0.3)

        print(
            f"Finished {file} in {(time_spend[-1]-perf_counter_ns())/1000000000} seconds"
        )
        time_spend.append(perf_counter_ns())
    else:
        print(f"Finished working on all {len(file_list)}.")
        print(f"Time used { (time_spend[-1]-time_spend[0])/1000000000 } seconds")
        print()
        print(time_spend)


if __name__ == "__main__":
    data_dir = Path("../test/data")

    work_dir = Path("../test/work")

    file_list: list = sorted([file for file in data_dir.glob("*.pdf")])

    main(work_dir, file_list)
