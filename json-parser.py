import json
import requests

headers = {
    'Content-Type': 'text/plain;charset=utf-8',
    'Accept': 'application/json',
}

params = (
    ('version', '2017-10-13'),
)

data = open('C:/Users/ahuja/Desktop/side_projects/buzzfeed/hitler.txt', 'rb').read()
response = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'QoK4TRsFxHfWUW3d-_KV4DOujgALshtnrzPolJ6BY_Wk'))
parsed = json.loads(response.text)

trait_dict = {}

print (range(len(parsed)))
print (parsed['personality'][0]['name'])

for i in range(len(parsed)-2):
	print ()
	trait_dict[(parsed['personality'][i]['name'])] = parsed['personality'][i]['percentile']

	for j in (range(len(parsed['personality'][i]['children']))):
		trait_dict[(parsed['personality'][i]['children'][j]['name'])] = parsed['personality'][i]['children'][j]['percentile']
