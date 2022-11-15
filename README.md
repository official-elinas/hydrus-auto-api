# Output on Auto's UI
1. Go to settings and check the following to create tag.txt files when you generate images. This script will not work without it!

![hydrus](repo_images/img.png)
2. Get `model-resnet_custom_v3.h5` and place it in `deepdanbooru/project/model-resnet_custom_v3.h5` - you can get this from the `models` folder in auto's UI or download it online
3. Create a folder and place your `PNG` files and `TXT` tag files in the same dir `/images` and run the script while outside the directory
3. After processing they will go to `/imported` if the folder has not been created already
4. You can find them in hydrus easily by using the automatically added namespace - `ai:true` in the search bar

# Setup on Hydrus Client API
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
- [ ] Character tags
- [ ] Implement args with options
- [ ] Add additional AI detail tags
- [ ] Support exif tagging
- [ ] Integrate into Auto's UI as a script - maybe

# Current Limitations
* Only supports alphanumeric characters as tags, but adds the prompt as a separate namespace called `prompt:<my really good prompt here>`