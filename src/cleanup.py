import sys
import os
import re

INPUT_DIR = os.path.join('..', 'converted')


def cleanup(filename):
    in_path = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(in_path):
        raise FileNotFoundError(
            'The requisite file is not found in the "converted" directory.')
    with open(in_path, 'r', encoding='utf-8') as inp:
        lines = inp.readlines()

    # Remove TOC
    lo = hi = None
    for i, line in enumerate(lines):
        if line.startswith(r'\protect\hyperlink'):
            if lo is None:
                lo = i
            hi = i
    lines = lines[:lo] + ['\\tableofcontents\n'] + lines[(hi+2):]

    lines = list(filter(lambda line: not line.startswith(r'\hypertarget{'),
                        lines))
    txt = ''.join(lines)

    # Remove closing braces left from hypertargets
    txt = re.sub(r'label{(\S+)}}', 'label{\g<1>}', txt)

    # Remove section numbers from bibliography and recommended reading
    txt = re.sub(r'section{Основная[ \n]+литература}',
                 r'section*{Основная литература}', txt)
    txt = re.sub(r'section{Библиография}', r'section*{Библиография}', txt)

    # Normalise italics
    txt = txt.replace('\\emph{', '\\textit{')

    # Normalise dashes
    txt = txt.replace(' -- ', ' --- ')

    new_filename = filename.replace('.tex', '_cleaned.tex')
    with open(os.path.join(INPUT_DIR, new_filename), 'w', encoding='utf-8') as out:
        out.write(txt)
    return new_filename


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python cleanup.py FILE')
        print('FILE is assumed to be located in the "converted" directory.')
    filename = sys.argv[1]
    try:
        cleanup(filename)
    except Exception as e:
        print(f'An error has occurred: {e}')
        sys.exit(1)
