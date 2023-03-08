import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.session import build_session


def query_global_data(session):

    query = """

    query globalData {
        userStatus {
        userId
        isSignedIn
        isMockUser
        isPremium
        isVerified
        username
        avatar
        isAdmin
        isSuperuser
        permissions
        isTranslator
        activeSessionId
        checkedInToday
        notificationStatus {
            lastModified
            numUnread
            }
        }
    }
    """

    body = {"query": query, "operationName": "globalData"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']

    return response


def query_user_calendar(username, session, year=None):
    
    if year is None:
        year = datetime.now().year

    query = """
        query userProfileCalendar($username: String!, $year: Int) {
            matchedUser(username: $username) {
                userCalendar(year: $year) {
                    activeYears
                    streak
                    totalActiveDays
                    dccBadges {
                        timestamp
                        badge {
                            name
                            icon
                        }
                    }
                    submissionCalendar
                }
            }
        }
    """
    body = {"query": query, "variables": {"username": username, "year": year}, "operationName": "userProfileCalendar"}
    body = json.dumps(body)

    response = session.request(method='POST', url="https://leetcode.com/graphql", body=body)

    response = json.loads(response.data)['data']
    print (response)

    cal_data = response['matchedUser']['userCalendar']
    print (cal_data)

    return response


def query_username(session):
    global_data = query_global_data(session=session)
    username = global_data['userStatus']['username']
    return username
    


if __name__ == '__main__':
    session = build_session()
    response = query_global_data(session=session)
    username = response['userStatus']['username']
    query_user_calendar(username, session)



