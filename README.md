# FUN-PROJECT-FINE-TUNING-GPT2-TO-TEACH-PYTHON-IN-THE-STYLE-OF-ANIME
## I first trained/fine-tuned the GPT-2 in google colab using an L4 GPU, which took about 3 hours for 1 epoch.
## I then uploaded it to huggingface to use their inference api.
## The model was fine-tuned on anime scripts (see example anime scripts I uploaded) and Python data (see collab file for specific huggingface dataset).
## I then prompt engineered the GPT-2 to be Yumi, an anime girl.
## I employed a translation LLM to convert the English text generation outputs to Japanese
## I used a text-to-speech (TTS) LLM to convert the Japanese text to audio.
## The current TTS model employed is (comedically) poor but can easily be switched out for other models with inference api from hugging face.
## I have the translator disabled currently.
## You can also disable the translation model and get direct english with a few minor changes to the code.
## The model connects to the html frontend via flask (see app.py).
## You can either create a .env file with your token (HUGGINGFACEHUB_API_TOKEN = instert_your_token_here) or insert it manually (don't share it with anyone).
