import pandas as pd
import json
import pickle
import nltk
import enchant
import re
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


os.chdir('/mnt/c/Users/lukef/Desktop/title_seniority/')

ABBREVIATION_PATH = os.path.abspath('data/abbreviations.json')
TITLE_PATH = os.path.abspath('data/titles.json')
JDB_RESUME_TILES = os.path.abspath('raw/jdb_resume_titles.csv')
JSMY_TITLES = os.path.abspath('raw/jsmy_titles.csv')

ps = PorterStemmer()

def save_json(data, path):
    with open(path, 'w') as fp:
        json.dump(data, fp)

def load_json(path):
    with open(path, 'r') as fp:
        data = json.load(fp)
    return data

def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)
        
def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def stem_and_join(title):
    return '_'.join(ps.stem(word) for word in title.split())

    
    
class SeniorityResolver(object):
    'An object that resolves abbreviations in job titles and extracts indicators of seniority'
    
    def __init__(self):
        self.abbreviations = load_json(ABBREVIATION_PATH)
        self.seniority_titles = load_pickle(TITLE_PATH)
        self.spell_checker = enchant.Dict('en_US')
        self.memory = {}
    
    @staticmethod
    def _lst_to_str(lst):
        if not lst or lst is None:
            return None
        else:
            return ' '.join(lst)
    
    @staticmethod
    def _join_one_letter_words(words):
        return ''.join([(word if len(word) == 1 else  ' ' + word + ' ')for word in words]).split()
    
    @staticmethod
    def lower_job_title(job_title):
        if isinstance(job_title, str):
            return job_title.lower()
        else:
            return None
        
    @staticmethod
    def _generate_shrinking_title(title):
        title = ' ' + title
        for space in range(title.count(' ')):
            title = title.split(' ', 1)[1]
            yield title
    
    def resolve_abbreviations(self, job_title):
        words = job_title.split()
        words = self._join_one_letter_words(words)
        return self._lst_to_str([(self.abbreviations[word] if word in self.abbreviations else word) for word in words])
    
    def correct_spelling(self, job_title):
        words = job_title.split()
        for i, word in enumerate(words):
            if self.spell_checker.check(word):
                continue
            elif word in self.memory:
                words[i] = self.memory[word]
            else:
                suggested_words = self.spell_checker.suggest(word)
                if suggested_words:
                    words[i] = suggested_words[0]
                    self.memory[word] = suggested_words[0]
                else:
                    words[i] = ''
        return self._lst_to_str(words)

    def get_seniority_title(self, job_title):
        seniority_in_title = []
        for j_title in self._generate_shrinking_title(job_title):
            for title in self.seniority_titles:
                if title == j_title[:len(title)]:
                    seniority_in_title.append(title)

        return seniority_in_title

