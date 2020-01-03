#import libraries
import urllib.request as ur
from bs4 import BeautifulSoup
import csv
import time
import re

# Creating soup from local html file
movie_html = "C:/Users/ahuja/Desktop/side_projects/buzzfeed/A-C.html"
movie_list = open(movie_html, 'r')
soup = BeautifulSoup(movie_list, 'html.parser')

#Create empty dictionary
#movie_dict = {}

movie_array = []
movie_list = []

i=0
MAX_MOVIES = 200


while i < MAX_MOVIES:

	#get info about current movie
	movie_info = soup.find_all('a')[i]

	#save movie title and link to its script separately
	movie_title = movie_info.get_text(strip=True, separator=' ')
		movie_title = re.sub('\n','',script_name)
		movie_title = re.sub('\t','',script_name)
		movie_title = re.sub('\ufffd','',script_name)

	movie_url = movie_info['href']

	#get info about doc-type
	doc_info = soup.find_all(attrs={"class" : "type"})[i]
	doc_type = doc_info.get_text()

	movie_array = [movie_title, movie_url, doc_type]

	movie_list.append(movie_array)
	#iterate
	i += 1


"""
	A-C : 355 titles
	D-J : 403 titles
	K-R : 368 titles 
	S-Z : 308 titles
	Total: 1434 titles
"""

#ADD LATER - Eliminate \n\n etc
#ADD LATER - only add HTML files to the dict

j = 0

for movie in movie_list:

	title = movie[0]
	url = movie[1]
	doc_type = movie[2]

	if (doc_type == ".pdf") or (doc_type == ".doc"):
		continue

	#get the url to follow
	try:
		script_doc = ur.urlopen(url)
	except:
		print ('url did not open for ' + title + ' ' + str(j)) 
		continue

	if doc_type == ".txt":
		#open a .txt file named as the movie title and keep ready for writing
		print (title, doc_type)
		try:
			script = script_doc.read().decode('utf-8')
		except:
			print('encoding error for ' + title + ' ' + str(j)) 
	elif doc_type == ".html":
		script_soup = BeautifulSoup(script_doc, 'html.parser')
		script = script_soup.get_text()

	if doc_type == ".txt" or doc_type == ".html":
		script_name = "%s.txt" % title
		file = open(script_name, 'w')
		try:
			file.write(script)
		except:
			print('decoding error for ' + title + ' ' + str(j)) 


	j += 1

"""
while i < MAX_MOVIES:

	#get info about current movie
	movie_info = soup.find_all('a')[i]

	#save movie title and link to its script separately
	movie_title = movie_info.get_text(strip=True, separator=' ')
	movie_url = movie_info['href']

	#add to dictionary
	movie_dict[movie_title] = movie_url
	
	#iterate
	i += 1

#Export to CSV

with open('movies.csv', 'w') as f:
    for key in movie_dict.keys():
        f.write("%s,%sn"%(key,movie_dict[key]))

"""