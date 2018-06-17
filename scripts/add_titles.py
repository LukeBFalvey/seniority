from seniority_lib import *
import sys

if __name__ == '__main__':
    title = sys.argv[1]
    
    titles = load_pickle(TITLE_PATH)
    if title in titles:
        print('{} already in set'.format(title))
    else:
        titles.add(title)
        save_pickle(titles, TITLE_PATH)
        print('Added title: {}'.format(title))
    
    
    