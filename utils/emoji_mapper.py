import json
from utils.helpers import tokenize, lemmatize

with open("data/emoji_dict_1200_clean_rebuild.json", encoding="utf-8") as f:
    EMOJI_DICT = json.load(f)

def get_emoji(word):
    return EMOJI_DICT.get(word.lower())

from utils.emoji_mapper import get_emoji

def map_to_emojis(original_text):
    tokens = tokenize(original_text)

    emojis = []

    for word in tokens:
        lemma = lemmatize(word)
        emoji = get_emoji(lemma)

        if emoji:
            emojis.append(emoji)
        else: emojis.append(word)

    return " ".join(emojis)