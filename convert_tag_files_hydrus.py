import os
from pathlib import Path

original_tags_dir = Path(fr"{os.getcwd()}/tag_files")

if not os.path.exists(f"{os.getcwd()}/new_tag_files"):
    os.mkdir(f"{os.getcwd()}/new_tag_files")

for file in os.listdir(original_tags_dir):
    with open(f"{original_tags_dir}/{file}", 'rb') as f:
        lines = f.readlines()
        found_tags = []
        # don't add multiple creator tags (if there are) to the beginning of the file due to weight
        creator_found = False
        characters_idx = 1
        for line in lines:
            tag = line.strip().decode('utf-8')
            if '_' in tag:
                tag = tag.replace('_', ' ')
            # ignore these tags
            if 'tagme' in tag:
                continue
            # only add one creator tag due to frequent dupes from Hydrus
            elif 'creator:' in tag and not creator_found:
                # found_tags.append(tag)
                found_tags.insert(0, tag.split(':')[1]) # remove the namespace add the artist to idx 0
                creator_found = True
            # dupe tags can happen with underscores so don't add dupe tags
            elif ('character:' in tag) and (tag != 'character:original') and tag.split(':')[1] not in found_tags:
                # insert characters to list after artist and increment
                found_tags.insert(characters_idx, tag.split(':')[1])
                characters_idx += 1
            # get namespaced hydrus clothing tags and remove the namespace
            elif 'clothing:' in tag:
                found_tags.append(tag.split(':')[1])
            # get rid of remaining namespaced tags except creator/character and only numeric tags
            elif ':' not in tag and not tag.isnumeric() and tag.isascii():  # and not tag.isnumeric()
                found_tags.append(tag)
        unique_tags = (list(dict.fromkeys(found_tags)))
        with open(f"{os.getcwd()}/new_tag_files_commas/{file.split('.')[0]}.txt", 'w', encoding='utf-8') as new_tag_file:  # split('.'[0])}.txt
            print(f'Updating tags for file: {file.split(".")[0]}.txt')
            new_tag_file.write((', '.join(t for t in unique_tags)))
