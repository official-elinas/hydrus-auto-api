import os
import subprocess

import deepdanbooru as dd
from deepdanbooru.commands import evaluate_image

images_fqp = []
img_dir = fr"{os.getcwd()}\images"
print(img_dir)
for img in os.listdir(img_dir):
    if '.txt' not in img:
        images_fqp.append(fr'{img_dir}\{img}')
print(images_fqp)

model_tag_list = []
model_tags = fr"{os.getcwd()}\deepdanbooru\tags-general.txt"
with open (model_tags) as tags:
    ddb_tags = tags.read()
    ddb_tags = ddb_tags.split('\n')
    model_tag_list.append(ddb_tags)

model_path = f"{os.getcwd()}\deepdanbooru\project"
model = dd.project.load_model_from_project(model_path, compile_model=False)

for img in images_fqp:
    print(f' img: {img}')
    for tag, score in evaluate_image(image_input=img, model=model, tags=model_tag_list[0], threshold=0.55):
        # print(f"({score:05.3f}) {tag}")
        # if save_txt: tag_list.append(tag)
        print(f'Tag: {tag}')
        print(f'Score: {score}')
