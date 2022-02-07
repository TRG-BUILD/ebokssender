""" Create data for testing file copier

"""


import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Create dummy files for testing...")
parser.add_argument("-n", "--numbers", type=int, help="Number of files")
parser.add_argument("-p", "--path", type=str, default="./data", help="Path for files")
args = parser.parse_args()

if __name__ == "__main__":
    path = Path(args.path)
    for item in range(args.numbers):
        with open(path / f"{item}.pdf", "w") as fp:
            fp.write(f"This i filenumber {item}")
        with open(path / f"{item}.txt", "w") as fp:
            fp.write(f"This i filenumber {item}")
