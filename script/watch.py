import logging
import re
import subprocess
import sys
from pprint import PrettyPrinter

import autopep8
import isort
from yapf.yapflib.errors import YapfError
from yapf.yapflib.yapf_api import FormatCode

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
pp = PrettyPrinter(indent=3)

python_re = re.compile(r'\.py$')
vscode_temp_file_re = re.compile(r'\.py\.[0-9a-f]+\.py$')


def is_python(path):
  return bool(re.search(python_re, path))


def get_paths_by_os(line):
  if sys.platform == 'linux':
    return line.rstrip().split(' ')
  elif sys.platform == 'darwin':
    dir = line.rstrip()
    return (dir, None)
  else:
    raise Exception('Unavailable OS.')


def updated_paths():
  for line in sys.stdin:
    print(line)
    vals = get_paths_by_os(line)
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
        autopep8ed_contents, filename=path, style_config='./pyproject.toml')
  except (SyntaxError, YapfError) as e:
    print(e)
    return False

  isorted_contents = isort.code(
      yapfed_contents, config=isort.Config(settings_path='.'))

  if contents == isorted_contents:
    return False
  put_file_contents(path, isorted_contents)
  return True


def ignore_pattern(path):
  return bool(re.search(vscode_temp_file_re, path))


if __name__ == '__main__':
  for path in updated_paths():
    if ignore_pattern(path):
      continue

    if is_python(path):
      if beautify_with_autopep8_yapf_isort(path):
        continue
    subprocess.run(['script/create-template'])
