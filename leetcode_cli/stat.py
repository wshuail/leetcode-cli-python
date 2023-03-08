import os
import sys
import json
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.session import build_session
from leetcode_cli.config import Config
from leetcode_cli.user import query_username

check_symbol = Config.check_symbol
not_check_symbol = Config.not_check_symbol



def query_stat(username, session):

    query = """
        query userProblemsSolved($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        problemsSolvedBeatsStats {
          difficulty
          percentage
        }
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
        
    """

    body = {"query": query, "variables": {"username": username}, "operationName": "userProblemsSolved"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']

    return response


def parse_stat_response(response):
    # qc for Question Count
    overall_qc = {}
    for level_qc in response['allQuestionsCount']:
        overall_qc[level_qc['difficulty']] = level_qc['count']
        
    ac_qc = {}
    for level_qc in response['matchedUser']['submitStatsGlobal']['acSubmissionNum']:
        ac_qc[level_qc['difficulty']] = level_qc['count']

    all_rate = ac_qc['All']/overall_qc['All']
    e_rate = ac_qc['Easy']/overall_qc['Easy']
    m_rate = ac_qc['Medium']/overall_qc['Medium']
    h_rate = ac_qc['Hard']/overall_qc['Hard']

    all_rate = math.ceil(all_rate*5)
    e_rate = math.ceil(e_rate*5)
    m_rate = math.ceil(m_rate*5)
    h_rate = math.ceil(h_rate*5)

    print ('{} {}/{} {}{}'.format('Overall'.ljust(10), str(ac_qc['All']).rjust(5), str(overall_qc['All']).ljust(5), check_symbol*all_rate, not_check_symbol*(50-all_rate)))
    print ('{} {}/{} {}{}'.format('Easy'.ljust(10), str(ac_qc['Easy']).rjust(5), str(overall_qc['Easy']).ljust(5), check_symbol*e_rate, not_check_symbol*(50-e_rate)))
    print ('{} {}/{} {}{}'.format('Medium'.ljust(10), str(ac_qc['Medium']).rjust(5), str(overall_qc['Medium']).ljust(5), check_symbol*m_rate, not_check_symbol*(50-m_rate)))
    print ('{} {}/{} {}{}'.format('Hard'.ljust(10), str(ac_qc['Hard']).rjust(5), str(overall_qc['Hard']).ljust(5), check_symbol*h_rate, not_check_symbol*(50-h_rate)))


def stat(session):
    username = query_username(session=session)
    response = query_stat(username=username, session=session)
    parse_stat_response(response)



if __name__ == '__main__':
    session = build_session()
    stat(session)



