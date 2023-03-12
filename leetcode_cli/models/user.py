import os
import sys
import json
from datetime import datetime
from datetime import date

# import july

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from leetcode_cli.models.session import build_session


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
    submissionCalendar = json.loads(cal_data['submissionCalendar'])
    print (submissionCalendar.__class__)
    dates, data = [], []
    for k, v in submissionCalendar.items():
        dates.append(datetime.fromtimestamp(int(k)).date())
        data.append(v)
    if dates[-1] != date.today():
        dates.append(date.today())
        data.append(0)
    
    # july.heatmap(dates, data, title='Leetcode Activity', cmap="github")

    return response


def query_username(session):
    global_data = query_global_data(session=session)
    username = global_data['userStatus']['username']
    return username
    


if __name__ == '__main__':
    session = build_session()
    response = query_global_data(session=session)
    username = response['userStatus']['username']
    query_user_calendar(username, session, year=2020)



