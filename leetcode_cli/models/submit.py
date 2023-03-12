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


def query_submission_details(submission_id, session):
    query = """

        query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        runtime
        runtimeDisplay
        runtimePercentile
        runtimeDistribution
        memory
        memoryDisplay
        memoryPercentile
        memoryDistribution
        code
        timestamp
        statusCode
        user {
          username
          profile {
            realName
            userAvatar
          }
        }
        lang {
          name
          verboseName
        }
        question {
          questionId
        }
        notes
        topicTags {
          tagId
          slug
          name
        }
        runtimeError
        compileError
        lastTestcase
      }
    }
    """
    
    body = {"query": query, "variables": {"submissionId": submission_id}, "operationName": "submissionDetails"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']


    return response



def submit(file, session):
    
    file_path = os.path.join(cur_dir, file)
    if not os.path.exists(file_path):
        raise ValueError ('file {} does not exist...'.format(file_path))
    file_name = os.path.basename(file_path)
    question_id, question_slug, lang_suffix = file_name.split('.')
    lang = {v: k for k, v in lang_suffixes.items()}.get(lang_suffix, None)
    if lang is None:
        raise ValueError ('Could not tell which programming language you are using, please specify by lang')
    
    with open(file, 'r') as f:
        code = f.read()
    
    request = {"lang": lang,
               "question_id": str(question_id),
               "typed_code": code
               }
    request = json.dumps(request)
    response = session.request(method='POST', url="https://leetcode.com/problems/two-sum/submit/", body=request)
    response = json.loads(response.data)
    submission_id = response['submission_id']
    time.sleep(3)
    submission_response = query_submission_details(submission_id=submission_id, session=session)
    sub_details = submission_response['submissionDetails']
    logging.info("Question Id: {}".format(question_id))
    logging.info("Question Slug: {}".format(question_slug))

    runtime = sub_details['runtimeDisplay']
    memory = sub_details['memoryDisplay']
    runtime_per = sub_details['runtimePercentile']
    memory_per = sub_details['memoryPercentile']


    if runtime == 'N/A' or memory == 'N/A' or runtime_per is None or memory_per is None:
        logging.info('Submission Failed.')
    else:
        memory_per_ceil = max(math.ceil(memory_per)//2, 1)
        runtime_per_ceil = max(math.ceil(runtime_per)//2, 1)
        print ('{} {} {}{}'.format('Runtime'.ljust(10), str(runtime).rjust(10), check_symbol*runtime_per_ceil, not_check_symbol*(50-runtime_per_ceil)))
        print ('{} {} {}{}'.format('Memory'.ljust(10), str(memory).rjust(10), check_symbol*memory_per_ceil, not_check_symbol*(50-memory_per_ceil)))
        logging.info("{} {} {} {}".format(runtime, runtime_per, memory, memory_per))
        logging.info('Submission Successed.')

    return response


