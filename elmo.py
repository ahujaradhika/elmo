from __future__ import print_function
from __future__ import print_function
import json, uuid
from ibm_watson import AssistantV2

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
        

def load_credential(authfile = None):
   if authfile == None:
       authfile = 'ibm-credentials.env'

   with open(authfile) as f:
       cred = {}
       for line in f:
           parts = line.strip('\r').strip('\n').split("=")

           if len(parts) == 2:
               cred[parts[0]] = parts[1]
       return cred;

   return None

def create_elmo(credential):
   # If service instance provides API key authentication
   return AssistantV2(
              version='2018-09-20',
              # url is optional, and defaults to the URL below. Use the correct URL for your region.
              url='https://gateway.watsonplatform.net/assistant/api',
              iam_apikey=credential['ASSISTANT_IAM_APIKEY'])

#########################
# Sessions
#########################
def create_session(assistant, ass_id):
   session = assistant.create_session(ass_id).get_result()
   print(json.dumps(session, indent=2))
   return session

#########################
# Message
#########################
def send_message(assistant, ass_id, sess_id, msg):
   message = assistant.message(
       ass_id,
       sess_id,
       input={'text': msg}, #'What\'s the weather like?'},
       context={
           'metadata': {
               'deployment': 'myDeployment'
           }
       }).get_result()
   #print(json.dumps(message, indent=2))
   return message['output']['generic'][0]['text']

def delete_session(assistant, ass_id, sess_id):
   return assistant.delete_session(ass_id, sess_id).get_result()

if __name__ == '__main__':
   credential = load_credential()

   if not credential:
       pass

   elmo = create_elmo(credential)
   ass_id = "70f87349-4762-41fb-a263-5dfc9626ad53"
   sess_id = create_session(elmo, ass_id)["session_id"]

   history = []
   dialog = "hello"
   msg = ""
   movie = "some movie"
   movie_characters = []
   NUMBER_OF_TRAITS = 28

   #CHATBOT STRUCTURES
   chatbot_dict = {} #dictionary of traits->percentiles for user conversation with chatbot
   chatbot_percentiles = []  #list of percentiles for user conversation with chatbot

   #MOVIE CHARACTER STRUCTURES
   list_of_dicts = []  #list of dictionaries of traits->percentiles (dictionary is for each character)
   list_of_percentiles = []  #list of lists of percentiles (list is for each character)
   smaller_list = [] #for parsing purposes


   while not "bye" in msg.lower() and not "see you" in msg.lower():
       msg = send_message(elmo, ass_id, sess_id, dialog)
       history.append(msg)

       if "Character" in msg or "Match character" in msg or "Search character" in msg:
          print (least_squares_matcher(chatbot_percentiles, list_of_percentiles))


        elif "Bingo! this is it" in msg:
            movie = history[-1].split("movie")[1].strip()
            movie_characters = char_names(movie)

           import json
           import requests

           headers = {'Content-Type': 'text/plain;charset=utf-8','Accept': 'application/json',}

           params = (('version', '2017-10-13'),)

           data = open('history.txt', 'rb').read()
           response = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'QoK4TRsFxHfWUW3d-_KV4DOujgALshtnrzPolJ6BY_Wk'))
           parsed = json.loads(response.text)

           #parses through chatbot dictionary traits->percentiles to generate list of percentiles 
           for i in range(len(parsed)-2):
             chatbot_dict[(parsed['personality'][i]['name'])] = parsed['personality'][i]['percentile']
 
             for j in (range(len(parsed['personality'][i]['children']))):
               chatbot_dict[(parsed['personality'][i]['children'][j]['name'])] = parsed['personality'][i]['children'][j]['percentile']

           for trait in chatbot_dict:
             chatbot_percentiles.append(chatbot_dict[trait])

             list_of_dicts = search_movie(movie)

             for item in list_of_dicts:
               for trait in item:
                 smaller_list.append(item[trait])  
               list_of_percentiles.append(smaller_list)
               smaller_list=[]



           # do the personal insights/api/v3/profile# find the best character
       dialog = input("Elmo: %s\nMe: " %(msg.strip('\r').strip('\n')))
       history.append(dialog)

       file_name = 'history'+'.txt'
       file = open(file_name,"w")
       file.write(str(history))
       file.close()

   delete_session(elmo, ass_id, sess_id)




