import os
import sys
import json
import logging
logging.getLogger().setLevel(logging.INFO)
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



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


def cache_file_exist(question):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
        question_id = map_slug_to_question_id(title_slug)
    
    question_cache_file = os.path.join(os.path.expanduser('~/.lc/cache'), '{}.{}.json'.format(question_id, title_slug))

    return os.path.exists(question_cache_file)

def load_cache_file(question):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
        question_id = map_slug_to_question_id(title_slug)
    
    question_cache_file = os.path.join(os.path.expanduser('~/.lc/cache'), '{}.{}.json'.format(question_id, title_slug))

    if not cache_file_exist(question_id):
        raise ValueError ("target file {} does not exist".format(question_cache_file))

    with open(question_cache_file, 'r') as f:
        cache = json.loads(f.read())
        cache['similarQuestions'] = json.loads(cache['similarQuestions'])

    return cache

def create_config_file():
    config = {}
    config['leetcode_session'] = None
    config['name'] = None
    config['email'] = None
    config['lang'] = None
    
    config['lang_suffixes'] = {
            "python3": "py",
            "javascript": "js",
            "java": "java",
            "c": "c",
            "cpp": "cpp",
            "ruby": "rb",
            "go": "go",
            "php": "php",
            "swift": "swift",
            "kotlin": "kt",
            "rust": "rs",
            "perl": "pl",
            "haskell": "hs",
            "scala": "scala",
            "lua": "lua",
            "r": "r",
            "typescript": "ts",
            "dart": "dart",
            "clojure": "clj"
            }

    config['comment_symbol'] = {
            "python3": "#",
            "javascript": "//",
            "java": "//",
            "c": "//",
            "cpp": "//",
            "ruby": "#",
            "go": "//",
            "php": "//",
            "swift": "//",
            "kotlin": "//",
            "rust": "//",
            "perl": "#",
            "haskell": "--",
            "scala": "//",
            "lua": "--",
            "r": "#",
            "typescript": "//",
            "dart": "//",
            "clojure": ";;"
            }


    config['id_slug_cache'] = 'id_slug_cache.json'
    config['slug_id_cache'] = 'slug_id_cache.json'

    config['check_symbol'] = u'\u2705'
    config['not_check_symbol'] = u'\u274C'
    config['lock_symbol'] = u'\U0001F512'

    config_path = os.path.join(os.path.expanduser('~/.lc'), 'config.json')
    with open(config_path, 'w') as f:
        f.write(json.dumps(config))

    logging.info("Basic config {} was created. \n leetcode_session need to be updated.".format(config_path))



def update_config_field(config, field):
    field_value = config.get(field)
    input_str = "please update {}\n".format(field)
    if field_value is not None or field_value != "":
        input_str += "current {}: {}\nPress ENTER to skip if you want to remain.\n".format(field, field_value)
    new_field_value = input(input_str)
    if new_field_value == '':
        return field_value
    else:
        return new_field_value


def update_config():
    logging.info('config will be updated.')
    
    config_path = os.path.join(os.path.expanduser('~/.lc'), 'config.json')
    if not os.path.exists(config_path):
        create_config_file()

    with open(config_path, 'r') as f:
        config = json.loads(f.read())

    for i, field in enumerate(['leetcode_session', 'name', 'email', 'lang']):
        logging.info("{}/4".format(str(i+1)))
        field_value = update_config_field(config, field)
        config[field] = field_value

    with open(config_path, 'w') as f:
        f.write(json.dumps(config))

    logging.info("config {} was updated.".format(config_path))

def init(func):
    def wrapper(*args, **kwargs):
        id_slug_cache_exist = os.path.exists(os.path.join(os.path.expanduser('~/.lc'), id_slug_cache)) 
        slug_id_cache_exist = os.path.exists(os.path.join(os.path.expanduser('~/.lc'), slug_id_cache))
        if not id_slug_cache_exist or not slug_id_cache_exist:
            cache_stat_status_pairs()
        if not os.path.exists(os.path.join(os.path.expanduser('~/.lc'), 'config.json')):
            create_config_file()
        
        with open(os.path.join(os.path.expanduser('~/.lc'), 'config.json'), 'r') as f:
            config = json.loads(f.read())
        
        leetcode_session = config.get('leetcode_session')
        if leetcode_session is None or leetcode_session == "":
            update_config()
        func(*args, **kwargs)
    return wrapper

class Config(object):
    if not os.path.exists(os.path.join(os.path.expanduser('~/.lc'), 'config.json')):
        create_config_file()
    with open(os.path.join(os.path.expanduser('~/.lc'), 'config.json'), 'r') as f:
        config = json.loads(f.read())

    name = config.get('name')
    email = config.get('email')
    
    id_slug_cache = config.get('id_slug_cache')
    slug_id_cache = config.get('slug_id_cache')
    leetcode_session = config.get('leetcode_session')
    lang = config.get('lang')
    lang_suffixes = config['lang_suffixes']
    comment_symbol = config['comment_symbol']

    check_symbol = config['check_symbol']
    not_check_symbol = config['not_check_symbol']
    
    lock_symbol = config['lock_symbol']



id_slug_cache = Config.id_slug_cache
slug_id_cache = Config.slug_id_cache


if __name__ == '__main__':
    update_config()


