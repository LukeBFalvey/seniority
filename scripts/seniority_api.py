from bottle import get, run
import pandas as pd
import csv
from seniority_lib import SeniorityResolver, stem_and_join
import os

title_scores = {}
resolver = SeniorityResolver()

def _load_scores():
    title_scores = {}
    with open('data/seniority_scores.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            title_scores[row[0]] = row[1]
            
    return title_scores

@get('/')
def hello():
    return "Hello World!"

def resolve_title(title):
    title = resolver.lower_job_title(title)
    title = resolver.resolve_abbreviations(title)
    title = resolver.correct_spelling(title)
    return title

@get('/seniority/<title>')
def seniority(title):
    title = resolve_title(title)
    title = stem_and_join(title)
    
    print('Title is : ' + title)
    
    if title in title_scores:
        return title_scores[title]
    else:
        return 'Not Implemented'

    
if __name__ == '__main__':
    global title_scores
    title_scores = _load_scores()
    run(host='localhost', port=8080, debug=True)
    