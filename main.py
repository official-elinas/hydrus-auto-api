import fnmatch
import json
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


# Get your client access key under
# "services" -> "review services" -> "client api" tab -> add a client and click "copy api access key"
try:
    key = os.environ['SECRET_KEY']
except KeyError:
    raise Exception('Generate a hydrus api key please!')

secret_key = {'Hydrus-Client-API-Access-Key': key}
API_ADDR = 'http://127.0.0.1:45869'

# support for other filetypes too, if you're odd sorry.
file_count = int(len(fnmatch.filter(os.listdir('images'), '*.*')) / 2)
print(f'Total filecount: {file_count}')

tag_files = []
image_files = []
for file in os.listdir("images"):
    if '.txt' in file:
        tag_files.append(file)
    else:
        image_files.append(file)

model_tag_list = []
model_tags = str(Path(fr"{os.getcwd()}/deepdanbooru/tags-general.txt"))
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

        tag_struct = {
            "hash": curr_file_hash,
            "service_names_to_tags": {
                "my tags": ["ai:true", f'prompt:{image.split("-")[2].replace(".png", "")}']
            }
        }

        # split the positive tags and them
        for new_tag in tags['positive_tags']:
            all_mod_tags = new_tag.split(',')
            for single_tag in all_mod_tags:
                # TODO: this is alphanumeric ONLY - need to support more formats without fucking shit up
                new = re.sub(r'\W+', ' ', single_tag)
                tag_struct['service_names_to_tags']['my tags'].append(new.strip())

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
            tag_struct['service_names_to_tags']['my tags'].append(tag)

        req = requests.post(f'{API_ADDR}/add_tags/add_tags', headers=secret_key, json=tag_struct)
        if req.ok:
            print('Successfully tagged file.')

for image in image_files:
    print(f' Image tagged and imported: {image}')
    images = Path(f'{os.getcwd()}/images/{image}')
    tag_files = Path(f'{os.getcwd()}/images/{image.replace(".png", "")}.txt')
    shutil.move(images, Path(f"{os.getcwd()}/imported"))
    shutil.move(tag_files, Path(f"{os.getcwd()}/imported"))
