import json
import logging
import os
import sys

logging.getLogger().setLevel(logging.INFO)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.models.detail import query_question_detail, parse_detail_response
from leetcode_cli.util import map_question_id_to_slug, map_slug_to_question_id
from leetcode_cli.util import cache_file_exist
from leetcode_cli.util import load_cache_file
from leetcode_cli.util import Config

check_symbol = Config.check_symbol
not_check_symbol = Config.not_check_symbol
lock_symbol = Config.lock_symbol


def query_user_questions_status(question, session):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question

    query = """
        query userQuestionStatus($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                status
            }
        }
    """

    body = {"query": query, "variables": {"titleSlug": title_slug}, "operationName": "userQuestionStatus"}

    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body, preload_content=True,
                               timeout=None)

    response = json.loads(response.data)['data']

    return response


def query_similar_questions(title_slug, session):
    query = """
    query SimilarQuestions($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            similarQuestionList {
                difficulty
                titleSlug
                title
                translatedTitle
                isPaidOnly
                }
            }
        }
    """

    body = {"query": query, "variables": {"titleSlug": title_slug}, "operationName": "SimilarQuestions"}

    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body, preload_content=True,
                               timeout=None)

    response = json.loads(response.data)['data']

    return response


def parse_similar_response(response, title_slug, session):
    question_id = map_slug_to_question_id(title_slug)

    questions = response['question']['similarQuestionList']
    for q in questions:
        q['question_id'] = map_slug_to_question_id(q['titleSlug'])

        question_status = query_user_questions_status(question=q['titleSlug'], session=session)
        status = question_status.get('question').get('status', None)
        q['status'] = status

    question_cache_file = os.path.join(os.path.expanduser('~/.lc/cache'), '{}.{}.json'.format(question_id, title_slug))

    if os.path.exists(question_cache_file):
        with open(question_cache_file, 'r+') as f:
            cache = json.loads(f.read())
            cache['similar_questions'] = questions
            f.write(json.dumps(cache, indent=4))
            logging.info('similar questions cached.')

    return questions


def format_similar_questions(questions):
    questions = [[q['question_id'], q['title'], q['difficulty'], q['isPaidOnly'], q['status']] for q in questions]
    
    questions.sort(key=lambda x: int(x[0]), reverse=True)

    max_len = max([len(q[1]) for q in questions])

    output = ''
    for q in questions:
        line = ' ' * 10
        line += str(q[0]).ljust(8)
        line += q[2].ljust(15)
        line += check_symbol.ljust(5) if q[4] == 'ac' else not_check_symbol.ljust(5)
        line += lock_symbol.ljust(8) if q[3] else ' ' * 9
        line += q[1].ljust(max_len + 5)
        line += '\n'
        output += line

    print(output)


def similar(question, session):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
        question_id = map_slug_to_question_id(title_slug)


    questions = None
    if not cache_file_exist(question=question_id):
        r = query_question_detail(question=question_id, session=session)
        detail = parse_detail_response(r)

    cache = load_cache_file(question=question_id)
    questions = cache.get('similarQuestions')
    for q in questions:
        title_slug = q.get('titleSlug')
        q['question_id'] = map_slug_to_question_id(title_slug)
        if not cache_file_exist(question=title_slug):
            r = query_question_detail(question=title_slug, session=session)
            detail = parse_detail_response(r)
        else:
            detail = load_cache_file(title_slug)
        q['status'] = detail.get('status')
        q['isPaidOnly'] = detail.get('isPaidOnly')

    format_similar_questions(questions)


if __name__ == '__main__':
    session = build_session()
    similar('two-sum', session)
