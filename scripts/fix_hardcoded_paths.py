import os
import glob
import re
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

base_dir = BASE_DIR
hardcoded_str = BASE_DIR

py_files = glob.glob(os.path.join(base_dir, '**/*.py'), recursive=True)

print(f"Auditing {len(py_files)} python files for hardcoded local paths...")

found_count = 0
for fpath in py_files:
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if hardcoded_str in content:
        found_count += 1
        print(f"  Found hardcoded path in: {os.path.relpath(fpath, base_dir)}")

print(f"Total files needing path fixes: {found_count}")
