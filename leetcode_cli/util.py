import os
import sys
import json
import logging
logging.getLogger().setLevel(logging.INFO)
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class Config(object):
    with open(os.path.join(os.path.expanduser('~/.lc'), 'config.json'), 'r') as f:
        config = json.loads(f.read())
    
    id_slug_cache = config.get('id_slug_cache')
    slug_id_cache = config.get('slug_id_cache')
    leetcode_session = config.get('leetcode_session')
    lang = config.get('lang')
    lang_suffixes = config['lang_suffixes']

    check_symbol = config['check_symbol']
    not_check_symbol = config['not_check_symbol']



id_slug_cache = Config.id_slug_cache
slug_id_cache = Config.slug_id_cache



def map_question_id_to_slug(question_id):
    with open(os.path.expanduser('~/.lc/{}'.format(id_slug_cache)), 'r') as f:
        id_slug_map = json.loads(f.read())
    title_slug = id_slug_map[str(question_id)].get('question_title_slug')

    return title_slug


def map_slug_to_question_id(title_slug):
    with open(os.path.expanduser('~/.lc/{}'.format(slug_id_cache)), 'r') as f:
        slug_id_map = json.loads(f.read())
    question_id = slug_id_map[str(title_slug)].get('question_id')

    return question_id


def cache_stat_status_pairs():
    url = 'https://leetcode.com/api/problems/all/'
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

    if not os.path.exists(os.path.expanduser('~/.lc')):
        os.makedirs(os.path.expanduser('~/.lc'), exist_ok=True)

    with open(os.path.expanduser('~/.lc/{}'.format(id_slug_cache)), 'w') as f:
        f.write(id_slug)
    
    with open(os.path.expanduser('~/.lc/{}'.format(slug_id_cache)), 'w') as f:
        f.write(slug_id)


def create_config_file():
    config = {}
    config['leetcode_session'] = ""
    config['name'] = ""
    config['email'] = ""
    config['lang'] = ""
    
    config['lang_suffixes'] = {
            'python3': 'py'
            }

    config['id_slug_cache'] = 'id_slug_cache.json'
    config['slug_id_cache'] = 'slug_id_cache.json'

    config['check_symbol'] = u'\u2705'
    config['not_check_symbol'] = u'\u274C'

    config_path = os.path.join(os.path.expanduser('~/.lc'), 'config.json')
    with open(config_path, 'w') as f:
        f.write(json.dumps(config))

    logging.info("Basic config {} was created. \n leetcode_session need to be updated.".format(config_path))



def update_config():
    config_path = os.path.join(os.path.expanduser('~/.lc'), 'config.json')
    with open(config_path, 'r') as f:
        config = json.loads(f.read())
    leetcode_session = config.get('leetcode_session')
    if leetcode_session is None or leetcode_session == "":
        logging.info("config {} need to be updated.".format(config_path))
        lc_session_input_str = """
            1/4
            Please input your leetcode session.
            Read README if you don't know how.
            """
        leetcode_session = input(lc_session_input_str)

        name = config.get('name')
        name = input('2/4 please input your name.')
        email = config.get('email')
        email = input('3/4 please input your email.')
        lang = config.get('lang')
        lang = input('4/4 please input your preferable lang.')
        
        config['leetcode_session'] = leetcode_session
        config['name'] = name
        config['email'] = email
        config['lang'] = lang
        
        with open(config_path, 'w') as f:
            f.write(json.dumps(config))

        logging.info("config {} was updated.".format(config_path))

    else:
        pass



def init(func):
    def wrapper(*args, **kwargs):
        id_slug_cache_exist = os.path.exists(os.path.join(os.path.expanduser('~/.lc'), id_slug_cache)) 
        slug_id_cache_exist = os.path.exists(os.path.join(os.path.expanduser('~/.lc'), slug_id_cache))
        if not id_slug_cache_exist or not slug_id_cache_exist:
            cache_stat_status_pairs()
        if not os.path.exists(os.path.join(os.path.expanduser('~/.lc'), 'config.json')):
            create_config_file()
        update_config()
        func(*args, **kwargs)
    return wrapper





