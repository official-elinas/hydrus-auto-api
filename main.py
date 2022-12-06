import argparse
import fnmatch
import pathlib
import re
import os
import shutil
import json
import os
import subprocess

import requests as requests
import deepdanbooru as dd
from deepdanbooru.commands import evaluate_image
from pathlib import Path


# parser = argparse.ArgumentParser()
# parser.add_argument('-in', '--input-dir', type=str, required=True, help='Input directory to all of your images')
# parser.add_argument('-out', '--output-dir', type=str, required=True, help='Output directory to save your images')
# parser.add_argument('-db-th', '--ddb-threshold', type=int, required=False, const=0.55, help='Tag sensitivity
# threshold for DeepDanbooru tags - default is 0.55 - lower is less sensitive')
# args = parser.parse_args()

# Get your client access key under
# "services" -> "review services" -> "client api" tab -> add a client and click "copy api access key"
try:
    key = os.environ['SECRET_KEY']
except KeyError:
    raise Exception('Generate a hydrus api key please!')

secret_key = {'Hydrus-Client-API-Access-Key': key}
API_ADDR = 'http://127.0.0.1:45869'

# if you didn't create the imported directory it will be created
if not os.path.exists(Path(f'{os.getcwd()}/imported')):
    print('path does not exist')
    os.makedirs(f'{os.getcwd()}/imported')

file_count = int(len(fnmatch.filter(os.listdir('images'), '*.*')) / 2)
print(f'Total filecount: {file_count}')

filetypes = ['png', 'jpg', 'jpeg', 'webp']
tag_files = []
image_files = []
for file in os.listdir("images"):
    if '.txt' in file:
        tag_files.append(file)
    else:
        image_files.append(file)

model_tag_list = []
# TODO - changed from tags-general.txt
model_tags = str(Path(fr"{os.getcwd()}/deepdanbooru/tags_all.txt"))
with open(model_tags) as tags:
    ddb_tags = tags.read()
    ddb_tags = ddb_tags.split('\n')
    model_tag_list.append(ddb_tags)

model = dd.project.load_model_from_project(str(Path(f"{os.getcwd()}/deepdanbooru/project")), compile_model=False)

for image in image_files:
    # file_path = {"path": fr"{os.getcwd()}\images\{image}"}
    tmp_path_img = Path(f"{os.getcwd()}/images/{image}")
    file_path = {"path": f'{tmp_path_img}'}
    req = requests.post(f'{API_ADDR}/add_files/add_file', headers=secret_key, json=file_path)
    json_resp = req.json()
    print(req.text)

    curr_file_hash = ''
    for tag_file in tag_files:

        tags = {
            "positive_tags": [],
            "negative_tags": [],
            "ai_tags": []
        }

        if image.split('-')[0] == tag_file.split('-')[0]:
            file_count -= 1
            print(f'Files left: {file_count}')
            # get the hash to add tags later
            curr_file_hash = json_resp['hash']
            with open(Path(f"{os.getcwd()}/images/{tag_file}")) as f:
                # just for progress ref
                print(f'Processing file: {tag_file.replace(".txt", "")}')
                lines = f.readlines()
                curr_pos = False
                curr_neg = False
                curr_ai = False
                for line in lines:
                    if len(tags['positive_tags']) < 1 and not curr_pos:
                        tags['positive_tags'].append(line)
                        tags['positive_tags'][-1] = str(tags['positive_tags'][-1]).replace('\n', '')
                        curr_pos = True
                    elif len(tags['negative_tags']) < 1 and not curr_neg:
                        tags['negative_tags'].append(line)
                        tags['negative_tags'][-1] = str(tags['negative_tags'][-1]).replace('\n', '')
                        curr_neg = True
                    elif len(tags['ai_tags']) < 1 and not curr_ai:
                        tags['ai_tags'].append(line)
                        tags['ai_tags'][-1] = str(tags['ai_tags'][-1]).replace('\n', '')
                        curr_ai = True
        else:
            # no hits? continue...
            continue

        file_ext = ''
        current_file_type_ext = image.split("-")[2].split(".")[-1]
        for filetype in filetypes:
            if filetype == current_file_type_ext:
                # validation
                file_ext = current_file_type_ext
                print(f'Found valid filetype for image: {current_file_type_ext}')

        if file_ext == '':
            print(f'Invalid extension for image: {current_file_type_ext} - moving to next image')
            continue

        tag_struct = {
            "hash": curr_file_hash,
            "service_names_to_tags": {
                "my tags": ["ai:true", f"prompt:{str(tags['positive_tags'][0])}"]
            }
        }

        # split the positive tags and them
        positive_tags = str(tags['positive_tags'][0])
        new_tag_str = positive_tags.replace(')', '').replace('(', '')
        tmp_pos_tag_arr = new_tag_str.split(',')
        new_pos_tag_arr = []
        for tag in tmp_pos_tag_arr:
            if '_' in tag:
                tag = tag.strip().split()
                for underscore_tag in tag:
                    underscore_tag = underscore_tag.replace('_', ' ')
                    new_pos_tag_arr.append(underscore_tag)
            else:
                new_pos_tag_arr.append(tag)
        for modified_tag in new_pos_tag_arr:
            tag_struct['service_names_to_tags']['my tags'].append(modified_tag.strip())

        if "Negative prompt:" in tags['negative_tags'][0]:
            neg_tags = tags['negative_tags'][0].replace('Negative prompt:', '')
            tag_struct['service_names_to_tags']['my tags'].append(f'negative_tags:{neg_tags.strip()}')
        else:
            tag_struct['service_names_to_tags']['my tags'].append(f"negative_tags:{tags['negative_tags'][0].strip()}")

        tmp_ai_tags = ''.join(tags['ai_tags']).split(',')
        for tmp_ai in tmp_ai_tags:
            to_add = (tmp_ai.replace(" ", ""))
            tag_struct['service_names_to_tags']['my tags'].append(to_add)

        for tag, score in evaluate_image(image_input=str(Path(f"{os.getcwd()}/images/{image}")), model=model,
                                         tags=model_tag_list[0],
                                         threshold=0.55):
            # print(f'Tag: {tag}')
            # print(f'Score: {score}')
            underscore_replaced_tag = tag.replace('_', ' ')
            # DO not add dupe tags
            if underscore_replaced_tag not in tag_struct['service_names_to_tags']['my tags']:
                tag_struct['service_names_to_tags']['my tags'].append(underscore_replaced_tag)

        # print(json.dumps(tag_struct, indent=4))
        # print(f"Num tags: {len(tag_struct['service_names_to_tags']['my tags'])}")

        req = requests.post(f'{API_ADDR}/add_tags/add_tags', headers=secret_key, json=tag_struct)
        if req.ok:
            # TODO: add error handling for moving
            print('Successfully tagged file.')
            image_file = Path(f'{os.getcwd()}/images/{image}')
            # use the image file name as a base to move the tag file
            tag_file = Path(f'{os.getcwd()}/images/{image.replace(f".{current_file_type_ext}", "")}.txt')
            shutil.move(image_file, Path(f"{os.getcwd()}/imported"))
            shutil.move(tag_file, Path(f"{os.getcwd()}/imported"))
            print(f'Image and tag moved and imported: {image}')

for image in image_files:
    print(f'Image moved and imported: {image}')
    images = Path(f'{os.getcwd()}/images/{image}')
    tag_files = Path(f'{os.getcwd()}/images/{image.replace(".png", "")}.txt')

    if not os.path.exists(Path(f'{os.getcwd()}/imported')):
        print('path does not exist')
        os.makedirs(f'{os.getcwd()}/imported')
    shutil.move(images, Path(f"{os.getcwd()}/imported"))
    shutil.move(tag_files, Path(f"{os.getcwd()}/imported"))
