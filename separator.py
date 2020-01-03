import re
from bs4 import BeautifulSoup

movie = ["breakfast-club", "the-hangover", "the-godfather", "the-lord-of-the-rings"]

def convert(movie):

	movie_html = "C:/Users/ahuja/Desktop/side_projects/buzzfeed/" + movie + ".html"
	movie_list = open(movie_html, 'r')
	soup = BeautifulSoup(movie_list, 'html.parser')

	script = soup.get_text()	

	movie_name = "%s.txt" % movie

	file = open(movie, 'w')
	file.write(script)


def read_text(movie):
	textline = []
	textname = movie+'.txt'
	lines = open(textname, 'r').readlines()
	for line in lines:
 		textline.append(line.strip())

	return textline

print(read_text("the-lord-of-the-rings"))


"""
MOVIE LIST

- Ghostbusters
-

"""