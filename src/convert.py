import sys
import os
from subprocess import run


INPUT_DIR = os.path.join('..', 'uploads')
RESULT_DIR = os.path.join('..', 'converted')


def convert_file(filename):
    if not filename.endswith('docx'):
        raise ValueError(
            f'Wrong file type: {filename.split["."][-1]};' +
            'only .docx files are supported.')
    in_path = os.path.join(INPUT_DIR, filename)
    new_filename = filename.replace('.docx', '.tex')
    out_path = os.path.join(RESULT_DIR, new_filename)
    if not os.path.exists(in_path):
        raise FileNotFoundError(
            'The requisite file is not found in the "uploads" directory.')
    run(['pandoc', '-t', 'latex', '-o', out_path, in_path])
    return new_filename


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python convert.py FILE')
        print('FILE is assumed to be located in the "uploads" directory.')
    filename = sys.argv[1]
    try:
        convert_file(filename)
    except Exception as e:
        print(f'An error has occurred: {e}')
        sys.exit(1)
