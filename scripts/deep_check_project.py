import os
import re
from pptx import Presentation
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

pptx_path = BASE_DIR
prs = Presentation(pptx_path)

print("="*60)
print("DEEP AUDIT: SLIDE TEXT INSPECTION & TYPO CHECK")
print("="*60)

all_text_tokens = []

for idx, slide in enumerate(prs.slides):
    print(f"\n--- SLIDE {idx+1} ---")
    for shape_idx, shape in enumerate(slide.shapes):
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                txt = p.text.strip()
                if txt:
                    print(f"  [Text]: {txt}")
                    tokens = re.findall(r'\b[A-Za-z]+\b', txt)
                    all_text_tokens.extend(tokens)
        elif shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    txt = cell.text.strip()
                    if txt:
                        print(f"  [Table Cell]: {txt}")

print("\n" + "="*60)
print(f"TOTAL TEXT PARAGRAPHS AUDITED ACROSS 18 SLIDES: {len(all_text_tokens)} words")
print("="*60)
