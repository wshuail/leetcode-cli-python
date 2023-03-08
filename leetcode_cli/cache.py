import os
import sys
import json
import logging
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.config import Config

id_slug_cache = Config.id_slug_cache
slug_id_cache = Config.slug_id_cache


url = 'https://leetcode.com/api/problems/all/'

def cache_stat_status_pairs():
    sess = requests.Session()
    res = sess.get(url)

    s = res.json()

    id_slug_map = {}
    slug_id_map = {}
    d = {}
    for pair in s['stat_status_pairs']:
        stat = pair['stat']
        question_id = stat.get('question_id')
        frontend_question_id = stat.get('frontend_question_id')
        question_title = stat.get('question__title')
        question_title_slug = stat.get('question__title_slug')
        total_acs = stat.get('total_acs')
        total_submitted = stat.get('total_submitted')
        id_slug_map[question_id] = {'question_title': question_title,
                                    'question_title_slug': question_title_slug,
                                    'total_acs': total_acs,
                                    'total_submitted': total_submitted}
        
        slug_id_map[question_title_slug] = {'question_title': question_title,
                                            'question_id': question_id,
                                            'total_acs': total_acs,
                                            'total_submitted': total_submitted}

    id_slug = json.dumps(id_slug_map)
    slug_id = json.dumps(slug_id_map)

    if not os.path.exists(os.path.expanduser('~/.lc/cache')):
        os.makedirs(os.path.expanduser('~/.lc/cache'), exist_ok=True)

    with open(os.path.expanduser('~/.lc/cache/{}'.format(id_slug_cache)), 'w') as f:
        f.write(id_slug)
    
    with open(os.path.expanduser('~/.lc/cache/{}'.format(slug_id_cache)), 'w') as f:
        f.write(slug_id)


if __name__ == '__main__':
    cache_stat_status_pairs()

    print ('cached.')
