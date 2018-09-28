# chefkoch-magazin-ocr

This is a project to scan my editions of the German magazine *Chefkoch
Magazin*, so that I can create a table of contents.

Since, imho, the collection of recipes (even without the actual
recipes) is a so called *Sammelwerk* and thus protected according to German
copyright law, this project **does not contain the actual table of contents**.


## Requirements

First, you need to install *tesseract* and its German data for OCR. In
Archlinux, the packages are called `tesseract` and `tesseract-data-deu`. In
other distributions the name might be similar.

You need to install the requirements, ideally into a virtual environment:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Usage

Scan the table of contents page of your Chefkoch magazines. Use the date of
the magazine as filename and put them all in one folder.

Once you've done this, run the script (set the folder `chefkoch-scans` to
the folder with your scanned table of contents):

```bash
python chefkoch.py chefkoch-scans
```

This will write a file `out.csv` containing all recipes.
