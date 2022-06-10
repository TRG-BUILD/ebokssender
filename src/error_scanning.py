"""

Script to scanning log files in failed folder
"""
import logging
from pathlib import Path
import csv

def main(scan: Path, filename: str):

    output = []
    for idx, file in enumerate(scan.rglob('*.log')):
        if idx % 25 == 0:
            print(idx+1, file)
        with open(file, 'r') as fp:
            content = fp.read()
            content = parse_file(content)
            content['filename'] = file.name
            output.append(content)

    #print("Write output.csv")

    with open(scan / filename, 'w', newline='') as csvfile:
        fieldnames = list(output[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(output)

    print(len(output))
    print(scan / filename)

def find_content(tag:list, content: str):
    if ( place_from := content.find(tag[0]) ) == -1:
        return ""
    place_from = place_from + len(tag[0])
    place_to = content.find(tag[1], place_from)
    #print(place_from, place_to)

    return content[place_from: place_to]


def parse_file(content):
    output = {}
    output['document'] = find_content(['Dokument sendt ', '\n'], content)
    output['statuskode'] = find_content(['<StatusKode>', '</StatusKode>'], content)
    output['fullname'] = find_content(['UserFullName=', '\n'], content)
    output['CPRCVR'] = find_content(['CPRCVR=', '\n'], content)
    output['Kanal'] = find_content(['Kanal=', '\n'], content)
    return output

if __name__ == "__main__":
    scan = Path('/Volumes/ease/Udsendt/MaxiHotfolder/FailedJobs/')
    main(scan, "failed.csv")

    #scan = Path('/Volumes/ease/Udsendt/MaxiHotfolder/SuccessfulJobs/')
    #main(scan, "failed.csv")






