import sys
import os
import json
import re
import logging
logging.getLogger().setLevel(logging.INFO)
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.models.detail import query_question_detail
from leetcode_cli.models.detail import parse_detail_response
from leetcode_cli.util import map_question_id_to_slug
from leetcode_cli.util import map_slug_to_question_id
from leetcode_cli.util import Config


cur_dir = os.getcwd()


def code(question, session, lang=None):
    
    global_lang = Config.lang
    name = Config.name
    email = Config.email

    if lang is None and global_lang is not None:
        lang = global_lang
    if lang is None and global_lang is None:
        raise ValueError("Either update config or pass argument for lang")
    lang_suffix = Config.lang_suffixes[lang]
    comment_symbol = Config.comment_symbol[lang]

    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
        question_id = map_slug_to_question_id(title_slug)
    
    if os.path.exists(os.path.join(cur_dir, '{}.{}.{}'.format(str(question_id), title_slug, lang_suffix))):
        logging.info("target file {}.{}.{} exist...".format(str(question_id), title_slug, lang_suffix))
        return 0

    if os.path.exists(os.path.expanduser('~/.lc/cache/{}.{}.json'.format(question_id, title_slug))):
        with open(os.path.expanduser('~/.lc/cache/{}.{}.json'.format(question_id, title_slug)), 'r') as f:
            detail = json.loads(f.read())
    else:
        session = build_session()
        response = query_question_detail(question_id, session)
        detail = parse_detail_response(response)

    content = detail['content']
    content = '\n'.join(['{}  '.format(comment_symbol) + line for line in content.splitlines()])
    
    hints = detail.get('hints')

    code_snippet = [code_snippet for code_snippet in detail['codeSnippets'] if code_snippet['langSlug'] == lang][0]['code']

    with open(os.path.join(cur_dir, '{}.{}.{}'.format(str(question_id), title_slug, lang_suffix)), 'w') as f:
        if name:
            f.write('{}  Name: {}'.format(comment_symbol, name))
            f.write('\n')
        if email:
            f.write('{}  Email: {}'.format(comment_symbol, email))
            f.write('\n')
        f.write('{}  Date: {}'.format(comment_symbol, datetime.now().strftime('%Y-%m-%d')))
        f.write('\n')
        f.write('\n\n\n')
        f.write(content)
        f.write('\n\n\n')
        if hints:
            f.write('#  Hints:\n')
            for i, hint in enumerate(hints):
                f.write('#  {}: {}\n'.format(i, hint))
            f.write('\n\n')
        if lang == 'python3':
            if re.search(r":\s*List\b", code_snippet):
                f.write("from typing import List")
                f.write('\n\n\n')
        f.write(code_snippet)




if __name__ == '__main__':
    session = build_session()
    code(question='1', session=session)




