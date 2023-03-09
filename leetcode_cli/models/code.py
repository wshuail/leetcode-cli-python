import sys
import os
import json
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.session import build_session
from leetcode_cli.detail import query_question_detail
from leetcode_cli.detail import parse_detail_response
from leetcode_cli.util import map_question_id_to_slug
from leetcode_cli.util import map_slug_to_question_id
from leetcode_cli.util import Config


lang = Config.lang
lang_suffix = Config.lang_suffixes[lang]

cur_dir = os.getcwd()



def code(question, session):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
        question_id = map_slug_to_question_id(title_slug)

    if os.path.exists(os.path.expanduser('~/.lc/cache/{}.{}.json'.format(question_id, title_slug))):
        with open(os.path.expanduser('~/.lc/cache/{}.{}.json'.format(question_id, title_slug)), 'r') as f:
            detail = json.loads(f.read())
    else:
        session = build_session()
        response = query_question_detail(question_id, session)
        detail = parse_detail_response(response)
    
    code_snippet = [code_snippet for code_snippet in detail['codeSnippets'] if code_snippet['langSlug'] == lang][0]['code']

    with open(os.path.join(cur_dir, '{}.{}.{}'.format(str(question_id), title_slug, lang_suffix)), 'w') as f:
        f.write(code_snippet)

    print (code_snippet)




if __name__ == '__main__':
    session = build_session()
    code(question='1', session=session)




