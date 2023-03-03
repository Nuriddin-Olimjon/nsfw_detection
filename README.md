# nsfw_detection API for validating "Not safe for work" images.
The library categorizes image probabilities in the following 5 classes:

- Drawing - safe for work drawings (including anime)
- Hentai - hentai and pornographic drawings
- Neutral - safe for work neutral images
- Porn - pornographic images, sexual acts
- Sexy - sexually explicit images, not pornography

# How to run
- Tested python version is 3.10.6

- Create your environment and activate it -> ```python3 -m venv venv && . ./venv/bin/activate```
- Install dependencies -> ```pip install -r requirements.txt```
- Run -> ```python3 main.py```

# Credits
- Thanks to https://github.com/GantMan/nsfw_model/ for their model.
