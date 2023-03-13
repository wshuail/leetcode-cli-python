import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.util import map_question_id_to_slug, map_slug_to_question_id
from leetcode_cli.util import Config

check_symbol = Config.check_symbol
not_check_symbol = Config.not_check_symbol
lock_symbol = Config.lock_symbol


    

def query_user_questions_status(title_slug, session):
    
    query = """
        query userQuestionStatus($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                status
            }
        }
    """

    body = {"query": query, "variables": {"titleSlug": title_slug}, "operationName": "userQuestionStatus"}
    
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body, preload_content=True, timeout=None)
    
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

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body, preload_content=True, timeout=None)
    
    response = json.loads(response.data)['data']

    return response


def parse_similar_response(response, session):

    questions = response['question']['similarQuestionList']
    questions = [[map_slug_to_question_id(q['titleSlug']), q['title'], q['difficulty'], q['isPaidOnly']] for q in questions]
    for q in questions:
        question_status = query_user_questions_status(title_slug=q[0], session=session)
        status = question_status.get('status', None)
        q.append(status)
    questions.sort(key=lambda x: int(x[0]), reverse=True)

    max_len = max([len(q[1]) for q in questions])

    output = ''
    for q in questions:
        line = ' '*10
        line += str(q[0]).ljust(8)
        line += q[2].ljust(15)
        line += check_symbol.ljust(5) if q[4] == 'ac' else not_check_symbol.ljust(5)
        line += lock_symbol.ljust(8) if q[3] else ' '*9
        line += q[1].ljust(max_len+5)
        line += '\n'
        output += line

    print (output)


def similar(question, session):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
 
    response = query_similar_questions(title_slug=title_slug, session=session)
    parse_similar_response(response, session)


if __name__ == '__main__':
    session = build_session()
    similar('two-sum', session)





