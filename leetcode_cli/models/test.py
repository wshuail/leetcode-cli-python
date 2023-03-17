import os
import sys
import json
import time
import math
import logging
logging.getLogger().setLevel(level=logging.INFO)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session
from leetcode_cli.util import map_question_id_to_slug
from leetcode_cli.util import Config
lang_suffixes = Config.lang_suffixes
check_symbol = Config.check_symbol
not_check_symbol = Config.not_check_symbol


cur_dir = os.getcwd()


def query_console_panel_config(question, session):

    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question
    
    query = """
    query consolePanelConfig($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            questionTitle
            enableDebugger
            enableRunCode
            enableSubmit
            enableTestMode
            exampleTestcaseList
            metaData
            }
        }   
    """

    body = {"query": query, "variables": {"titleSlug": title_slug}, "operationName": "consolePanelConfig"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']
    # print (title_slug, response)

    return response


def test(file, session):

    file_path = os.path.join(cur_dir, file)
    if not os.path.exists(file_path):
        raise ValueError ('file {} does not exist...'.format(file_path))
    file_name = os.path.basename(file_path)
    question_id = file_name.split('.')[0]
    lang_suffix = file_name.split('.')[-1]
    lang = {v: k for k, v in lang_suffixes.items()}.get(lang_suffix, None)
    if lang is None:
        raise ValueError ('Could not tell which programming language you are using, please specify by lang')
    
    title_slug = map_question_id_to_slug(question_id)
    
    with open(file, 'r') as f:
        code = f.read()
    
    response = query_console_panel_config(question_id, session)
    
    # only test one avoid error "429 Rate limit exceeded"
    test_cases = response['question']['exampleTestcaseList']
    test_case = test_cases[0]
    
    logging.info('Testing case {}'.format(repr(test_case)))

    request = {"lang": lang,
               "question_id": str(question_id),
               "typed_code": code,
               "data_input": test_case,
               'judge_type': 'large',
               'test_mode': False
               }
    request = json.dumps(request)

    response = session.request(method='POST', url="https://leetcode.com/problems/{}/interpret_solution/".format(title_slug), body=request)
    response = json.loads(response.data)
    interpret_id = response['interpret_id']
    time.sleep(5)
    r = session.request(method='GET', url="https://leetcode.com/submissions/detail/{}/check/".format(interpret_id))
    r = json.loads(r.data)
    print (r)
    run_success = r.get('run_success')
    if run_success:
        code_answer = r.get('code_answer')
        logging.info('Test Case: {}, Answer: {}'.format(test_case, code_answer))
        logging.info("Test Passed.")
    else:
        status_msg = r.get('status_msg')
        compile_error = r.get('compile_error')
        logging.info('Status Msg: {}'.format(status_msg))
        logging.info('Compile Error: {}'.format(compile_error))
        logging.info("Test Failed.")
    logging.info('\n')




if __name__ == '__main__':
    pass

