import os
import sys
import json
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.detail import detail


def query_question_today(session):

    query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                userStatus
                link
                question {
                    acRate
                    difficulty
                    freqBar
                    frontendQuestionId: questionFrontendId
                    isFavor
                    paidOnly: isPaidOnly
                    status
                    title
                    titleSlug
                    hasVideoSolution
                    hasSolution
                    topicTags {
                        name
                        id
                        slug
                    }
                }
            }
        }
    """

    body = {"query": query, "operationName": "questionOfToday"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']

    return response


def parse_today_response(response):
    r = response['activeDailyCodingChallengeQuestion']
    date = r['date']
    status = r['userStatus']  # 'NotStart',
    link = r['link']
    q = r['question']
    acrate = q['acRate']
    difficulty = q['difficulty']
    paidonly = q['paidOnly']
    title = q['title']
    title_slug = q['titleSlug']
    topic_tags = [tag['name'] for tag in q['topicTags']]

    return title_slug


def today(session):
    r = query_question_today(session)
    title_slug = parse_today_response(r)
    detail(question=title_slug, session=session)


if __name__ == '__main__':
    from session import build_session
    session = build_session()
    # response = query_question_today(session=session)
    today(session)



