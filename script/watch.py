import logging
import re
import subprocess
import sys
from pprint import PrettyPrinter

import autopep8
from isort import SortImports
from yapf.yapflib.yapf_api import FormatCode

log = logging.getLogger(__name__)
pp = PrettyPrinter(indent=3)

python_re = re.compile(r'\.py$')


def is_python(path):
  return bool(re.search(python_re, path))


def updated_paths():
  for line in sys.stdin:
    print(line)
    vals = line.rstrip().split(' ')
    if len(vals) == 3:
      dir, _, file = vals
      yield dir + file
    elif len(vals) == 2:
      file, _ = vals
      yield file
    else:
      print('Unknown notification format:')
      print(line)


def get_file_contents(path):
  with open(path, 'r', encoding='utf8') as f:
    return f.read()


def put_file_contents(path, contents):
  with open(path, 'w', encoding='utf8') as f:
    f.write(contents)


def beautify_with_autopep8_yapf_isort(path):
  contents = get_file_contents(path)

  autopep8ed_contents = autopep8.fix_code(contents, apply_config=True)
  try:
    yapfed_contents, _ = FormatCode(
        autopep8ed_contents, filename=path, style_config='setup.cfg')
  except SyntaxError as e:
    print(e)
    return False
  isorted_contents = SortImports(file_contents=yapfed_contents).output

  if contents == isorted_contents:
    return False
  put_file_contents(path, isorted_contents)
  return True


if __name__ == '__main__':
  for path in updated_paths():
    if is_python(path):
      if beautify_with_autopep8_yapf_isort(path):
        continue
    subprocess.run(['script/create-template'])
