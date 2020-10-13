import requests

data = requests.get(url= 'https://tinbds.com/du-an/ho-chi-minh/quan-1')

print(data.content)