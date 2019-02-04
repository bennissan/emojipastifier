#!/usr/bin/python
# -*- coding: UTF-8 -*-

from emoji import UNICODE_EMOJI as emojis, emojize, demojize
from fuzzywuzzy import process as fuzzy_match
import nltk
import random
import re
import sys

stemmer = nltk.PorterStemmer()

emoji_names = list(map(demojize, emojis))
# Repetitive parts of speech to ignore when emojifying: personal pronouns, coordinating conjunctions, and the word "to".
pos_to_filter = ["PRP", "CC", "TO"]
# Flags (actual physical flags!) to ignore when emojifying unless matched exactly: countries and national subdivisions.
flags_to_filter = ["1f1e", "1f1f", "1f3f"]

copypasta_file = sys.argv[1]
with open(copypasta_file, "r") as f:
    copypasta = f.read()
word_list = copypasta.split()

def add_emoji(word):
    if nltk.pos_tag([word])[0][1] in pos_to_filter:
        return word

    stem = stemmer.stem(word)
    (match_name, match_value) = fuzzy_match.extractOne(stem, emoji_names)
    # Arbitrary match accuracy threshold: high enough to remain accurate, but low enough to catch funny homophones.
    if match_value < 75:
        return word
    
    emoji_name = match_name
    emoji = emojize(emoji_name)
    # Checks if emoji is a flag and ignores unless matched exactly; there are too many flag emojis!
    if any(flag in emoji.encode("unicode-escape").decode("ASCII") for flag in flags_to_filter) and match_value != 100:
        return word

    # Repeat emoji between one and three times for that classic emojipasta flair.
    return word + " " + random.randint(1, 3) * emoji

emojipasta = " ".join(map(add_emoji, word_list))

print(emojipasta)