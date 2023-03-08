import os
import sys
import json
import requests
from urllib3 import PoolManager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from leetcode_cli.config import Config



def get_csrf_cookie(session_id: str) -> str:
    response = requests.get(
        "https://leetcode.com/",
        cookies={
            "LEETCODE_SESSION": session_id,
        },
    )

    return response.cookies["csrftoken"]




def build_session():
    with open(os.path.expanduser('~/.lc/config.json'), 'r') as f:
        config = json.loads(f.read())
    leetcode_session = config['leetcode_session']
    # leetcode_session = Config.leetcode_session
    csrftoken = get_csrf_cookie(session_id=leetcode_session)
    # csrftoken = Config.csrftoken

    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Swagger-Codegen/1.0.0/python',
            'Referer': 'https://leetcode.com',
            'Cookie': "csrftoken={}; LEETCODE_SESSION={}".format(csrftoken, leetcode_session),
            'x-csrftoken': csrftoken
            }
    # print (headers)
    
    # session = PoolManager(headers=headers, num_pools=4, maxsize=20, cert_reqs=2, ca_certs='/usr/local/anaconda3/lib/python3.9/site-packages/certifi/cacert.pem')
    session = PoolManager(headers=headers)
    # session = PoolManager()

    return session




