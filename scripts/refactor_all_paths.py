import os
import glob
import re

base_dir = '/Users/vimalkansotia/Downloads/Bioinformatics'
hardcoded_prefix = '/Users/vimalkansotia/Downloads/Bioinformatics'

py_files = glob.glob(os.path.join(base_dir, '**/*.py'), recursive=True)

print("Refactoring all python files for dynamic portable paths...")

for fpath in py_files:
    if 'refactor_all_paths.py' in fpath:
        continue
        
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
        
    if hardcoded_prefix in content:
        # Determine depth relative to root
        rel = os.path.relpath(fpath, base_dir)
        depth = len(rel.split(os.sep)) - 1
        
        if depth == 0:
            dir_calc = "os.path.dirname(os.path.abspath(__file__))"
        else:
            up_levels = ", ".join(["'..'"] * depth)
            dir_calc = f"os.path.abspath(os.path.join(os.path.dirname(__file__), {up_levels}))"
            
        # Replace occurrences of hardcoded string
        # Replace string literal '/Users/vimalkansotia/Downloads/Bioinformatics/...' or '/Users/vimalkansotia/Downloads/Bioinformatics'
        pattern = re.compile(re.escape(hardcoded_prefix) + r'(/[^"\'\s]*)?')
        
        def replacer(match):
            subpath = match.group(1)
            if subpath:
                # e.g. /data/processed/master_metadata.csv -> os.path.join(BASE_DIR, 'data/processed/master_metadata.csv')
                clean_sub = subpath.lstrip('/')
                parts = clean_sub.split('/')
                joined = ", ".join([f"'{p}'" for p in parts])
                return f"os.path.join(BASE_DIR, {joined})"
            else:
                return "BASE_DIR"

        # Check if import os is present
        new_content = content
        if "import os" not in new_content:
            new_content = "import os\n" + new_content
            
        # Add BASE_DIR definition near top after imports
        lines = new_content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith(('import ', 'from ')):
                insert_idx = i + 1
                
        base_dir_line = f"BASE_DIR = {dir_calc}"
        if "BASE_DIR =" not in new_content:
            lines.insert(insert_idx, base_dir_line)
            
        new_content = '\n'.join(lines)
        
        # Replace literal strings
        # E.g., '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/master_metadata.csv'
        # -> os.path.join(BASE_DIR, 'data', 'processed', 'master_metadata.csv')
        def replace_quoted(m):
            quote = m.group(1)
            path_str = m.group(2)
            sub = path_str[len(hardcoded_prefix):].lstrip('/')
            if not sub:
                return "BASE_DIR"
            parts = sub.split('/')
            joined = ", ".join([f"'{p}'" for p in parts])
            return f"os.path.join(BASE_DIR, {joined})"

        new_content = re.sub(r'(["\'])' + re.escape(hardcoded_prefix) + r'([^"\']*?)\1', replace_quoted, new_content)
        
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
            
        print(f"  Fixed: {rel}")

print("Path refactoring complete!")
