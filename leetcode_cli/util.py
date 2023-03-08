import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.config import Config


id_slug_cache = Config.id_slug_cache
slug_id_cache = Config.slug_id_cache


def map_question_id_to_slug(question_id):
    with open(os.path.expanduser('~/.lc/cache/{}'.format(id_slug_cache)), 'r') as f:
        id_slug_map = json.loads(f.read())
    title_slug = id_slug_map[str(question_id)].get('question_title_slug')

    return title_slug


def map_slug_to_question_id(title_slug):
    with open(os.path.expanduser('~/.lc/cache/{}'.format(slug_id_cache)), 'r') as f:
        slug_id_map = json.loads(f.read())
    question_id = slug_id_map[str(title_slug)].get('question_id')

    return question_id

