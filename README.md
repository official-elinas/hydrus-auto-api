# hydrus auto Stable Diffusion api
Software - `python 3.9` and [stable-diffusion-webui by AUTOMATIC1111
](https://github.com/AUTOMATIC1111/stable-diffusion-webui) if you don't have it already

## Commands
`git clone https://github.com/official-elinas/hydrus-auto-api.git` 

Run - `pip -r install requirements.txt` in a `venv` if you choose

## Output on Auto's UI
Go to settings and check the following to create tag.txt files when you generate images. This script will not work without it!

![hydrus](repo_images/img.png)
1. Get `model-resnet_custom_v3.h5` and place it in this project at `deepdanbooru/project/model-resnet_custom_v3.h5` - you can get this from the `models` folder in auto's UI after enabling the flag `--deepdanbooru` in `webui-user.bat` or `webui-user.sh` 
1. Create a folder and place your `png/jpg/jpeg/webp` files and `txt` tag files in the same dir `/images` and run the script while outside the directory
3. After processing they will go to `/imported` if the folder has not been created already
4. You can find them in hydrus easily by using the automatically added namespace - `ai:true` in the search bar

## What is Hydrus?
> The hydrus network client is a desktop application written for Anonymous and other internet enthusiasts with large media collections. It organises your files into an internal database and browses them with tags instead of folders, a little like a booru on your desktop. Tags and files can be anonymously shared through custom servers that any user may run. Everything is free, nothing phones home, and the source code is included with the release. It is developed mostly for Windows, but builds for Linux and macOS are available (perhaps with some limitations, depending on your situation).
Source: https://hydrusnetwork.github.io/hydrus/

If you are not familiar with the application, you can read through the docs or download the latest release here: https://github.com/hydrusnetwork/hydrus/releases

Hydrus is not just a tagging solution, but supports downloading from numerous sites as well as a PTR (Public Tag Repo) that matches hashes and will automatically tag images you already have that are originals and not resized.
## Setup on Hydrus Client API
1. Get your client access key under "services"
2. "review services"
3. "client api" tab 
4. add a client
5. click "copy api access key" on the bottom right
6. add it as an OS environment variable or in your IDE or just remove that code and hardcode it here: `secret_key = {'Hydrus-Client-API-Access-Key': key}`
6. if your client api is working it should be accessible at http://127.0.0.1:45869

# TODO
- [x] Move imported files into an `imported` folder
- [x] Fix unix paths
- [x] Integrate deepdanbooru tagging as an *optional* feature (for now)
- [x] Character tags
- [ ] Tagging older images without tag.txt files
- [ ] Implement args with options
- [ ] Support exif tagging
- [x] Add additional AI detail tags
- [ ] Integrate into Auto's UI as a script - maybe
- 
# Current Limitations
* Only supports alphanumeric characters as tags, but adds the prompt as a separate namespace called `prompt:<my really good prompt here>`