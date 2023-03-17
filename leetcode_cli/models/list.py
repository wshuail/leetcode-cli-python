import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.util import Config

check_symbol = Config.check_symbol
not_check_symbol = Config.not_check_symbol
lock_symbol = Config.lock_symbol


def query_problemset_question_list(session, level=None, limit=100):
    
    query = """
        query problemsetQuestionList(
            $categorySlug: String, 
            $limit: Int, 
            $skip: Int, 
            $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                    ) {
                        totalNum
                        questions: data {
                            questionId
                            questionFrontendId
                            title
                            titleSlug
                            acRate
                            difficulty
                            isPaidOnly
                            status
                            }
                        }
                    }
    """

    if level:
        level = level.upper()
        body = {"query": query, "variables": {"filters": {"difficulty": level}, "categorySlug": "", "skip": 0, "limit": limit}, "operationName": "problemsetQuestionList"}
    else:
        body = {"query": query, "variables": {"filters": {}, "categorySlug": "", "skip": 0, "limit": 9999}, "operationName": "problemsetQuestionList"}
    
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body, preload_content=True, timeout=None)
    
    response = json.loads(response.data)['data']

    return response


def parse_list_response(response, level, undo=False, free=False):

    questions = response['problemsetQuestionList']['questions']

    # total_num = detail['totalNum']
    
    # isPaidOnly

    if undo and free:
        questions = [[q['questionId'], q['title'], q['difficulty'], q['isPaidOnly'], q['status']] for q in questions if (q['status'] is None or q['isPaidOnly'] == False)]
    elif undo:
        questions = [[q['questionId'], q['title'], q['difficulty'], q['isPaidOnly'], q['status']] for q in questions if q['status'] is None]
    elif free:
        questions = [[q['questionId'], q['title'], q['difficulty'], q['isPaidOnly'], q['status']] for q in questions if q['isPaidOnly'] == False]
    else:
        questions = [[q['questionId'], q['title'], q['difficulty'], q['isPaidOnly'], q['status']] for q in questions]
    questions.sort(key=lambda x: int(x[0]), reverse=True)

    max_len = max([len(q[1]) for q in questions])

    output = ''
    for q in questions:
        line = ' '*10
        line += str(q[0]).ljust(8)
        if level is None:
            line += q[2].ljust(15)
        line += check_symbol.ljust(5) if q[4] == 'ac' else not_check_symbol.ljust(5)
        line += lock_symbol.ljust(8) if q[3] else ' '*9
        line += q[1].ljust(max_len+5)
        line += '\n'
        output += line

    print (output)


def list_question(session, level=None, undo=False, free=False, limit=100):
    response = query_problemset_question_list(session=session, level=level, limit=limit)
    parse_list_response(response, level=level, undo=undo, free=free)


if __name__ == '__main__':
    session = build_session()
    response = query_problemset_question_list(level='easy', session=session)
    parse_list_response(response, undo=False, free=False)





