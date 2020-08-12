from requests import get
from json import loads

# get and return return requested data
def getftxdata(url):
    return loads(get(url).text)['result']