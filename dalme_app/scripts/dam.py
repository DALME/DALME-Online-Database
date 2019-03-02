import requests
import hashlib
from urllib.parse import urlencode

def rs_api_query(endpoint, user, key, **kwargs):
    sign = hashlib.sha256(key.encode('utf-8'))
    paramDict = kwargs
    paramDict['user'] = user
    paramstr = urlencode(paramDict)
    sign.update(paramstr.encode('utf-8'))
    R = requests.get(endpoint + paramstr + "&sign=" + sign.hexdigest())
    return R
