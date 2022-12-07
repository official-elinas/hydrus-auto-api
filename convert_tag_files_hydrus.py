# Converts Hydrus multi line tag files to single line comma separated ones for training
# (dreambooth, native - not used for importing)

import os
from pathlib import Path

original_tags_dir = Path(fr"{os.getcwd()}/tag_files")

if not os.path.exists(f"{os.getcwd()}/new_tag_files"):
    os.mkdir(f"{os.getcwd()}/new_tag_files")

for file in os.listdir(original_tags_dir):
    curr_file_tags = []
    with open(f"{original_tags_dir}/{file}", 'rb') as f:
        lines = f.readlines()
        found_tags = []
        # no duplicate tags
        unique_tags = set()
        for line in lines:
            tag = line.strip().decode('utf-8').replace('_', '')
            found_tags.append(tag)
        for tag in found_tags:
            if tag not in unique_tags:
                unique_tags.add(tag)

        with open(f"{os.getcwd()}/new_tag_files/{file}", 'w', encoding='utf-8') as new_tag_file:
            print(f'Updating tags for file: {file}')
            # sort tags alphabetically and separate with commas
            new_tag_file.write((', '.join(sorted(unique_tags))))
