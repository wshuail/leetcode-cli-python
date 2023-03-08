import sys
import os
import json
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.config import Config
from leetcode_cli.session import build_session
from leetcode_cli.util import map_question_id_to_slug


lang = Config.lang
lang_suffix = Config.lang_suffixes[lang]


def query_question_detail(question, session):
    try:
        question_id = int(question)
        title_slug = map_question_id_to_slug(question_id)
    except:
        title_slug = question

    query = """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            content
            isPaidOnly
            difficulty
            similarQuestions
            langToValidPlayground
            topicTags {
              name
              slug
              translatedName
              __typename
            }
            codeSnippets {
              lang
              langSlug
              code
              __typename
            }
            stats
            hints
            solution {
              id
              canSeeDetail
              __typename
            }
            status
            metaData
          }
        }
    """

    print (title_slug)

    body = {"query": query, "variables": {"titleSlug": title_slug}, "operationName": "getQuestionDetail"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)
    
    response = json.loads(response.data)['data']
    
    return response



def cache_question_detail(detail):
    if not os.path.exists(os.path.expanduser('~/.lc/cache')):
        os.makedirs(os.path.expanduser('~/.lc/cache'), exist_ok=True)
    
    question_id = detail['questionId']
    title_slug = detail['titleSlug']
    detail = json.dumps(detail)
    
    with open(os.path.join(os.path.expanduser('~/.lc/cache'), '{}.{}.json'.format(question_id, title_slug)), 'w') as f:
        f.write(detail)



def parse_detail_response(response):

    detail = response['question']
    print (detail)
    
    detail['content'] = BeautifulSoup(detail['content'], 'html.parser').get_text()



    """
    
    content = detail['content']
    content = BeautifulSoup(content, 'html.parser').get_text()
    print ('content: {}'.format(content))

    code_snippets = detail['codeSnippets']
    target_code_snippet = [code_snippet for code_snippet in code_snippets if code_snippet['langSlug'] == lang][0]['code']
    """

    cache_question_detail(detail)

    return detail


def detail(question, session):
    r = query_question_detail(question, session)
    detail = parse_detail_response(r)
    
    fields = ['questionId', 'questionFrontendId', 'title', 'titleSlug', 'content', 'isPaidOnly',
              'difficulty', 'similarQuestions', 'langToValidPlayground', 'topicTags', 
              'codeSnippets', 'stats', 'hints', 'solution', 'status', 'metaData']

    question_id = detail['questionId']
    title = detail['title']
    difficulty = detail['difficulty']
    topic_tags = [topic['name'] for topic in detail['topicTags']]
    content = detail['content']
    hints = detail['hints']

    print ("{}:  {}".format("Question Id".ljust(20), question_id))
    print ("{}:  {}".format("Question Title".ljust(20), title))
    print ("{}:  {}".format("Difficulty".ljust(20), difficulty))
    print ("{}:  {}".format("Topics".ljust(20), topic_tags))
    print ('\n\n')
    print (content)
    print ('\n\n')
    if hints:
        print ('Hints: ')
        for hint in hints:
            print (hint)

    return detail


if __name__ == '__main__':
    session = build_session()
    detail(question='1', session=session)




