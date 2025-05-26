from sphinx.util import requests

keyword='python'
url='https://www.huibo.com/cq/jobs/all/?key='+keyword

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'}
response = requests.get(url, headers=header)
if response:
    data = response.content