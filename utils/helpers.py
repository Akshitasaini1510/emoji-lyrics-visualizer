import re
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
def tokenize(text):
    # keeps words only, removes punctuation
    return re.findall(r"\b\w+\b", text.lower())

# building lemmatizer
# download once (safe to keep here)
nltk.download("wordnet")
nltk.download("omw-1.4")

lemmatizer = WordNetLemmatizer()

def tokenize(text):
    return re.findall(r"[a-zA-Z']+", text.lower())


def get_wordnet_pos(word):
    try:
        tag = nltk.pos_tag([word])[0][1][0].upper()
    except:
        return wordnet.NOUN

    if tag == "J":
        return wordnet.ADJ
    elif tag == "V":
        return wordnet.VERB
    elif tag == "N":
        return wordnet.NOUN
    elif tag == "R":
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatize(word):
    pos = get_wordnet_pos(word)
    return lemmatizer.lemmatize(word, pos)
