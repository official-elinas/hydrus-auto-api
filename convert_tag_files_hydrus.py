# Converts Hydrus multi line tag files to single line comma separated ones for training
# (dreambooth, native - not used for importing)

import os
from pathlib import Path

original_tags_dir = Path(fr"{os.getcwd()}/tag_files")

if not os.path.exists(f"{os.getcwd()}/new_tag_files"):
    os.mkdir(f"{os.getcwd()}/new_tag_files")

for file in os.listdir(original_tags_dir):
    with open(f"{original_tags_dir}/{file}", 'rb') as f:
        lines = f.readlines()
        found_tags = []
        for line in lines:
            tag = line.strip().decode('utf-8')
            if '_' in tag:
                tag = tag.replace('_', ' ')
            if ':' not in tag and tag.isascii():  # and not tag.isnumeric()
                found_tags.append(tag)
        unique_tags = (list(dict.fromkeys(found_tags)))
        with open(f"{os.getcwd()}/new_tag_files/{file}", 'w', encoding='utf-8') as new_tag_file:
            print(f'Updating tags for file: {file}')
            new_tag_file.write((' '.join(t for t in unique_tags)))
