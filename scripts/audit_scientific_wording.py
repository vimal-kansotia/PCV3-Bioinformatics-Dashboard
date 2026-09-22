import os
import glob
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

search_dir = BASE_DIR
strong_words = ['concordant', 'corroborate', 'cause', 'caused', 'origin', 'transmission', 'molecular clock', 'evolutionary rate']

found_issues = []

for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith(('.md', '.py', '.txt', '.csv')):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
                for word in strong_words:
                    if word in content.lower():
                        found_issues.append((f, word))

print(f"Found {len(found_issues)} occurrences of potential wording issues:")
for fname, word in found_issues[:20]:
    print(f"  File: {fname} | Word: '{word}'")
