#!/usr/bin/python
# -*- coding: UTF-8 -*-

from emoji import UNICODE_EMOJI as emojis, emojize, demojize
from fuzzywuzzy import process
import nltk
import random
import re
import sys
import unicodedata

stemmer = nltk.PorterStemmer()

emoji_names = list(map(demojize, emojis))
pos_to_filter = ["PRP", "TO", "CC"]
flags_to_filter = ["1f1e", "1f1f", "1f3f"]

copypasta = sys.argv[1]
word_list = copypasta.split()

def add_emoji(word):
    if nltk.pos_tag([word])[0][1] in pos_to_filter:
        return word

    stem = stemmer.stem(word)
    (match_name, match_value) = process.extractOne(stem, emoji_names)
    if match_value < 75:
        return word
    
    emoji_name = match_name
    emoji = emojize(emoji_name)
    if any(flag in emoji.encode('unicode-escape').decode('ASCII') for flag in flags_to_filter) and match_value != 100:
        return word

    return word + " " + random.randint(1, 3) * emoji

emojipasta = " ".join(map(add_emoji, word_list))

print(emojipasta)