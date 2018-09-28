from PIL import Image
import pytesseract
import re
import collections
import glob
import Levenshtein
import csv
import os
import sys


class TesseractReader(object):
    def parse(self, filepath):
        img = Image.open(filepath)
        return pytesseract.image_to_string(img, lang='deu')


def detect_headers(filepaths, reader):
    possible_headers = []

    for filepath in filepaths:
        text = reader.parse(filepath)

        for line in map(str.strip, text.splitlines()):
            # require either a number at line end or a dot
            if not re.match(r'.+(\d+|\.)$', line):
                possible_headers.append(line)

    return collections.Counter(possible_headers)


def match_headers(possible_headers, available_headers):
    matches = []

    for possible in possible_headers:
        qualities = []
        for check in available_headers:
            dist = Levenshtein.distance(check, possible)
            qualities.append((dist, check))

        best_match = sorted(qualities)[0]
        matches.append((possible, best_match[1], best_match[0]))

    ok_headers = {}
    for m in matches:
        if m[2] <= 2:
            ok_headers[m[0]] = m[1]

    return ok_headers


def read_toc(filepath, headers, reader):
    text = reader.parse(filepath)

    recipes = collections.defaultdict(list)
    cur_header = None
    for line in map(str.strip, text.splitlines()):
        if line in headers:
            cur_header = headers[line]
        else:
            m = re.match(r'(.+?)[\.\s]*(\d+|\.)$', line)
            if m:
                recipes[cur_header].append((m.group(1), m.group(2)))

    return recipes


if __name__ == '__main__':
    directory = sys.argv[1]
    
    legal_headers = [
        'Mit Fleisch', 'Vegetarisch', 'Vegan',
        'Mit Fisch', 'Süßes'
    ]
    files = glob.glob(os.path.join(directory, '*.jpg'))

    reader = TesseractReader()
    headers = detect_headers(files, reader)
    matched_headers = match_headers(headers, legal_headers)

    with open('out.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Ausgabe', 'Kategorie', 'Rezept', 'Seite'])

        for filepath in files:
            date = os.path.splitext(os.path.basename(filepath))[0]
            recipesdict = read_toc(filepath, matched_headers, reader)

            for category, recipes in recipesdict.items():
                for recipe in recipes:
                    writer.writerow([date, category, recipe[0], recipe[1]])
