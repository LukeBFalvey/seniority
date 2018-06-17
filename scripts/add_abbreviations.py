from seniority_lib import *
import sys

if __name__ == '__main__':
    acronym = sys.argv[1]
    acronym_resolved = sys.argv[2]
    
    abbreviations = load_json(ABBREVIATION_PATH)
    abbreviations[acronym] = acronym_resolved
    save_json(abbreviations, ABBREVIATION_PATH)
    print('Added abbreviations: {}: {} to abbreviations dict'.format(acronym, acronym_resolved))
    
    
    