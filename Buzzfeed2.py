#!/usr/bin/env python
# coding: utf-8

# In[108]:
from __future__ import print_function
import json, uuid
from ibm_watson import AssistantV2


# import urllib.request as ur
# from bs4 import BeautifulSoup
# import csv
# import time
# import re

# # Creating soup from local html file
# movie_html = "moviescript.html"
# movie_list = open(movie_html, 'r')
# soup = BeautifulSoup(movie_list, 'html.parser')

# movie_array = []
# movie_list = []

# i=0
# MAX_MOVIES = 20


# while i < MAX_MOVIES:

# 	#get info about current movie
# 	movie_info = soup.find_all('a')[i]

# 	#save movie title and link to its script separately
# 	movie_title = movie_info.get_text(strip=True, separator=' ')
# 	movie_title = re.sub('\n','',movie_title)
# 	movie_title = re.sub('\t','',movie_title)
# 	movie_title = re.sub('\ufffd','',movie_title)
# 	print(movie_title)   

# 	movie_url = movie_info['href']

# 	#get info about doc-type
# 	doc_info = soup.find_all(attrs={"class" : "type"})[i]
# 	doc_type = doc_info.get_text()

# 	movie_array = [movie_title, movie_url, doc_type]

# 	movie_list.append(movie_array)
# 	#iterate
# 	i += 1


# """
# 	A-C : 355 titles
# 	D-J : 403 titles
# 	K-R : 368 titles 
# 	S-Z : 308 titles
# 	Total: 1434 titles
# """

# #ADD LATER - Eliminate \n\n etc
# #ADD LATER - only add HTML files to the dict

# j = 0
# success_pulled = []

# for movie in movie_list:

# 	title = movie[0]
# 	url = movie[1]
# 	doc_type = movie[2]

# 	if (doc_type == ".pdf") or (doc_type == ".doc"):
# 		print ('it\'s a pdf')    
# 		continue

# 	#get the url to follow
# 	try:
# 		script_doc = ur.urlopen(url)
# 	except:
# 		print ('url did not open for ' + title + ' ' + str(j)) 
# 		continue

# 	if doc_type == ".txt":
# 		#open a .txt file named as the movie title and keep ready for writing
# 		print (title, doc_type)
# 		try:
# 			script = script_doc.read().decode('utf-8')
# 		except:
# 			print('encoding error for ' + title + ' ' + str(j)) 
# 	elif doc_type == ".html":
# 		script_soup = BeautifulSoup(script_doc, 'html.parser')
# 		script = script_soup.get_text()

# 	if doc_type == ".txt" or doc_type == ".html":
# 		script_name = "%s.txt" % title
# 		script_name = re.sub('\n','',script_name)
# 		script_name = re.sub('\t','',script_name)
# 		script_name = re.sub('\ufffd','',script_name)
# 		file = open(script_name, 'w')
# 		try:
# 			file.write(script)
# 		except:
# 			print('decoding error for ' + title + ' ' + str(j))

# 	j += 1
# 	success_pulled.append(title)
# 	print (j)


# In[109]:


# for movie in success_pulled:
#     print(str(movie))


# In[2]:


import re
script_words = {}

def read_text(movie):
    textline = []
    textname = movie+'.txt'
    lines = open(textname,'r').readlines()
    for line in lines:
        textline.append(line.strip())
    return textline

#'the-godfather'
#'the-fault-in-our-stars'
file_names = ['the-godfather','the-hangover','the-lord-of-the-rings','star-wars','ghostbusters']
for movie in file_names:
    script_words[movie] = read_text(movie)


# In[3]:


import pandas as pd
import spacy
from collections import Counter
nlp = spacy.load('en')
def named_entity_counts(document,named_entity_label):   
    ## Function that outputs a Counter object of human entities found\n",
    occurrences = [ent.string.strip() for ent in document.ents if ent.label_ == named_entity_label and ent.string.strip()]
    return Counter(occurrences)

def parse_text(movie):
    name_text = movie + '.txt'
    text2 = open(name_text).read()
    doc = nlp(text2)
    parsed_script = doc  
    entity_type = 'PERSON' 
    number_of_entities = 5
    Entities=pd.DataFrame(named_entity_counts(parsed_script,entity_type).most_common(number_of_entities),columns=["Character","Count"])
    Entities['Movie'] = movie
    return Entities

result = pd.DataFrame()
for file in file_names:
    df = parse_text(file)
    result = result.append(df,ignore_index = True)


# In[4]:


def dict_names (Character):
    name_dict = {}
    for character in Character:
        character = character.upper()
        if (character in name_dict.keys()):
            continue
        if len(character.split()) >=2:
            full_name = character.split()
            name_dict[full_name[0]] = character
        else:
            name_dict[character] = ''
    return name_dict

dictionary_names = dict_names (result['Character'])
print (dictionary_names)
print (result)
        


# In[5]:


name_movie = result.set_index('Character').to_dict()['Movie']
name_movie2 = {}
for name in dictionary_names.keys():
    for n in name_movie.keys():
        if name in n.upper():
            name_movie2[name] = name_movie[n]   
print (name_movie2)


# In[11]:


# def people_says (textlist,names):
#     sublist = []
#     words_list = []
#     for character in names:
#         for i in range(len(textlist)):
#             if (textlist[i].strip() == character):
#                 j = i + 1
#                 while (textlist[j]!= ''):
#                     j += 1
#                 sublist.append(textlist[i:j])
#         words_list.append(sublist)
#     for character in dictionary_names.values():
#         if character != '':
#             for i in range(len(textlist)):
#                 if (textlist[i].strip() == character):
#                     j = i + 1
#                     while (textlist[j]!= ''):
#                         j += 1
#                     sublist.append(textlist[i:j])
#         words_list.append(sublist)
#     return words_list


# #what_people_say = []
# #{'MICHAEL': 'the-godfather', 'KAY': 'the-godfather', 'SONNY': 'the-godfather', 'MIKE': 'the-godfather', 'VICK': 'the-hangover', 'ALAN': 'the-hangover', 'DOUG': 'the-hangover', 'PATRICK': '10 Things I Hate About You', 'KAT': '10 Things I Hate About You', 'JOEY': '10 Things I Hate About You', 'CAMERON': '10 Things I Hate About You', 'GANDALF': 'the-lord-of-the-rings', 'SAM': 'the-lord-of-the-rings', 'BOROMIR': 'the-lord-of-the-rings', 'ARAGORN': 'the-lord-of-the-rings', 'FRODO': 'the-lord-of-the-rings', 'LUKE': 'star-wars', 'CHEWIE': 'star-wars', 'LEIA': 'star-wars', 'VADER': 'star-wars', 'LANDO': 'star-wars', 'FIONA': 'shrek', 'FARQUAAD': 'shrek', 'DULOC': 'shrek', 'LORD': 'shrek', 'SHREK': 'shrek', 'VENKMAN': 'ghostbusters', 'SPENGLER': 'ghostbusters', 'STANTZ': 'ghostbusters', 'DANA': 'ghostbusters'}
# #'VENKMAN': '', 'SPENGLER': '', 'STANTZ': '', 'DANA': ''}
# def char_names (movie):
#     n = []
#     for nn in name_movie2:
#         if name_movie2[nn] == movie:
#             n.append(nn)
#     return n

# what_people_say = []
# for movie in file_names:
#     what_people_say.append(people_says(script_words[movie],char_names(movie)))
    

    


# In[7]:


def people_says (textlist,character):
    sublist = []
    words_list = []
    for i in range(len(textlist)):
        if (textlist[i].strip() == character):
            j = i + 1
            while (textlist[j]!= ''):
                j += 1
            sublist.append(textlist[i+1:j])
    words_list.append(sublist)
#     for character in dictionary_names.values():
#         if character != '':
#             for i in range(len(textlist)):
#                 if (textlist[i].strip() == character):
#                     j = i + 1
#                     while (textlist[j]!= ''):
#                         j += 1
#                     sublist.append(textlist[i:j])
#         words_list.append(sublist)
    return words_list
def char_names (movie):
    n = []
    for name in name_movie2:
        if name_movie2[name] == movie:
            n.append(name)
    return n

for movie in file_names:
    for name in char_names(movie):
        file_name = name+'.txt'
        file = open(file_name,"w")
        file.write(str(people_says(script_words[movie],name)))
file.close()


# In[339]:


#compile people's words in characters

# if ll[0] in people_say_dict.keys():
#     value = ''.join(ll[1:len(ll)])
#     people_say_dict[ll[0]].append(value)
#         else:
#             value = ''.join(ll[1:len(ll)]) 
#             people_say_dict[ll[0]] = ll[1:len(ll)]
# print (people_say_dict['MIKE'])
        
# people_say_dict = {}
# for l in per_movie:
#         for ll in l:
#                 if ll[0] in people_say_dict.keys():
#                     value = ''.join(ll[1:len(ll)])
#                     people_say_dict[ll[0]].append(value)
#                 else:
#                     value = ''.join(ll[1:len(ll)])                   
#                     people_say_dict[ll[0]] = ll[1:len(ll)]
# print (people_say_dict.keys())


# In[323]:


# key_list = list(people_say_dict.keys()) 
# for key in key_list:
#     file_name = key+'.txt'
#     file = open(file_name,"w")
#     file.write(str(people_say_dict[key]))  
# file.close()


# In[8]:


import json
import requests

headers = {
    'Content-Type': 'text/plain;charset=utf-8',
    'Accept': 'application/json',
}

params = (
    ('version', '2017-10-13'),
)

def json_parser(text_name):
    data = open(text_name, 'rb').read()
    response = requests.post('https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'QoK4TRsFxHfWUW3d-_KV4DOujgALshtnrzPolJ6BY_Wk'))
    parsed = json.loads(response.text)

    trait_dict = {}

    for i in range(len(parsed)-2):
        trait_dict[(parsed['personality'][i]['name'])] = parsed['personality'][i]['percentile']

        for j in (range(len(parsed['personality'][i]['children']))):
            trait_dict[(parsed['personality'][i]['children'][j]['name'])] = parsed['personality'][i]['children'][j]['percentile']
    return trait_dict


# In[11]:


personality = []
#if re-run the function again, need to un-comment these below
#dictionary_names.pop('MIKE')
#dictionary_names.pop('CHEWIE')
for name in dictionary_names.keys():
    txtname = name + '.txt'
    print (name)
    personality.append(json_parser(txtname))


# In[12]:


from cloudant import cloudant_iam

# Authenticate using an IAM API key
ACCOUNT_NAME = '9f18399f-0e0a-4464-9cae-afcc09328dbe-bluemix'
API_KEY = 'j7H-txptJqOJ9G1PQ01hIHZYcs2oieznEkt6qWvGQBio'
DB_NAME = 'elmo_characters'

def put_character(db, **kargs):
    db.create_document(kargs)

def get_character(db, c_id):
    return db[c_id]

def get_character_id(movie, character):
   return ":".join([movie.lower(), character.lower()])

if __name__ == "__main__":

    with cloudant_iam(ACCOUNT_NAME, API_KEY, connect=True) as client:
        db = None
        dblist = client.all_dbs()
    
        if not DB_NAME in dblist:
            db = client.create_database(DB_NAME)
        else:
            db = client[DB_NAME] 
        
        for name in dictionary_names.keys():
            
            txtname = name + '.txt'
            c_id = get_character_id(name_movie2[name], name)
            put_character(db, _id=c_id, movie = name_movie2[name],character=name, personality=json_parser(txtname))

print(db)


# In[65]:


# #for testing and choosing scripts
# def read_text(movie):
#     textline = []
#     textname = movie+'.txt'
#     lines = open(textname,'r').readlines()
#     for line in lines:
#         textline.append(line.strip())
#     return textline

# read_text('frozen')


# In[20]:




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

def delete_session(assistant, ass_id, sess_id):
    return assistant.delete_session(ass_id, sess_id).get_result()

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

if __name__ == '__main__':
    credential = load_credential()

    if not credential:
        pass

    elmo = create_elmo(credential)
    ass_id = "70f87349-4762-41fb-a263-5dfc9626ad53"
    sess_id = create_session(elmo, ass_id)["session_id"]

    dialog = "hello"
    msg = ""
    while not "bye" in msg.lower() and not "see you" in msg.lower():
        msg = send_message(elmo, ass_id, sess_id, dialog)
        dialog = input("Elmo: %s\nMe: " %(msg.strip('\r').strip('\n')))

    delete_session(elmo, ass_id, sess_id)


# In[16]:




