# AI speech-to-text and text-to-speech validation

## Prerequisites
- Python
- Pip
- Virtualenv

Detailed installation instructions [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Setup

### Create virtual environment:
On macOS and Linux:
```bash
python3 -m venv venv
```

On Windows:
```bash
py -m venv venv
```

### Activate virtual environment:
On macOS and Linux:
```bash
source venv/bin/activate
```

On Windows:
```bash
.\venv\Scripts\activate
```

### Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

### Create data file
Create the file `files/data.txt` with texts on separate lines

### Run the test
```bash
python3 tests.py
```