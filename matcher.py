import json
import requests

headers = {
    'Content-Type': 'text/plain;charset=utf-8',
    'Accept': 'application/json',
}

params = (
    ('version', '2017-10-13'),
)

#GLOBALS
# This should be passed as a paramter: list of MOVIE CHARACTERS NOT MOVIES (Movie names just used as a placeholder)
movie_characters = ["finding-nemo", "frozen", "shrek", "star-wars"]
NUMBER_OF_TRAITS = 28


#CHANGE CODE - If this API call is already done somewhere else, no need to use request
data = open('C:/Users/ahuja/Desktop/side_projects/buzzfeed/scripts/breakfast-club.txt', 'rb').read()
response = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'QoK4TRsFxHfWUW3d-_KV4DOujgALshtnrzPolJ6BY_Wk'))
parsed = json.loads(response.text)

print(parsed)


#CHATBOT STRUCTURES
chatbot_dict = {}	#dictionary of traits->percentiles for user conversation with chatbot
chatbot_percentiles = []	#list of percentiles for user conversation with chatbot

#MOVIE CHARACTER STRUCTURES
list_of_dicts = []	#list of dictionaries of traits->percentiles (dictionary is for each character)
list_of_percentiles = []	#list of lists of percentiles (list is for each character)
smaller_list = [] #for parsing purposes

"""
NOTE: If the data is already separated out into a list of percentiles for chatbot, 
and a list of list of percentiles for movie characters, 
then you can start on line 80 (but you will still need globals)
"""

#parses through chatbot dictionary traits->percentiles to generate list of percentiles 
for i in range(len(parsed)-2):
	chatbot_dict[(parsed['personality'][i]['name'])] = parsed['personality'][i]['percentile']

	for j in (range(len(parsed['personality'][i]['children']))):
		chatbot_dict[(parsed['personality'][i]['children'][j]['name'])] = parsed['personality'][i]['children'][j]['percentile']

for trait in chatbot_dict:
	chatbot_percentiles.append(chatbot_dict[trait])

# This should be passed as a paramter: list of MOVIE CHARACTERS NOT MOVIES (Movie names just used as a placeholder)
movie_characters = ["finding-nemo", "frozen", "shrek", "star-wars"]

trait_dict = {}

for character in movie_characters:


	#CHANGE CODE - change to location of the .txt with the words said by a particular character
	#CHANGE CODE - If the API call is already done somewhere else, no need to use request
	data = open('C:/Users/ahuja/Desktop/side_projects/buzzfeed/scripts/' + character + '.txt', 'rb').read()
	response = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'QoK4TRsFxHfWUW3d-_KV4DOujgALshtnrzPolJ6BY_Wk'))
	parsed = json.loads(response.text)	

	#parses through code to generate list of dictionaries of trait->percentiles (list is for each character)
	for i in range(len(parsed)-2):
		trait_dict[(parsed['personality'][i]['name'])] = parsed['personality'][i]['percentile']

		for j in (range(len(parsed['personality'][i]['children']))):
			trait_dict[(parsed['personality'][i]['children'][j]['name'])] = parsed['personality'][i]['children'][j]['percentile']

	list_of_dicts.append(trait_dict)

"""
parses through to generate a list of a list of percentiles
(inner list is the percentile for each trait)
(outer list is the list of list of percentiles for each trait)
"""
for item in list_of_dicts:
	for trait in item:
		smaller_list.append(item[trait])	
	list_of_percentiles.append(smaller_list)
	smaller_list=[]


#IF PERCENTILES ALREADY SEPARATED OUT, START HERE

# Least Squares Matching
def least_squares_matcher(chatbot_percentiles, list_of_percentiles):

	least_squares = []
	i = 0
	j = 0

	while j < len(list_of_percentiles):

		cur_least_square = 0

		while i < NUMBER_OF_TRAITS: 
			diff = chatbot_percentiles[i] - list_of_percentiles[j][i]
			square = diff * diff

			cur_least_square += square
			i += 1

		least_squares.append(cur_least_square)
		j += 1

	least_square_index = (least_squares.index(min(least_squares)))

	return (movie_characters[least_square_index])

print (least_squares_matcher(chatbot_percentiles, list_of_percentiles))

