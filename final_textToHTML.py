import urllib.parse 
import urllib.request as ur
import json as m_json
from bs4 import BeautifulSoup
import wikipedia
import html2text
import os

def apiGoogle(advanced_query):
	query = urllib.parse.urlencode ( { 'q' : advanced_query } )
	conn = ur.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query )
	response = conn.read()
	# remember to close connection
	conn.close()
	str_response = response.decode('utf-8')
	json = m_json.loads ( str_response )
	results = json [ 'responseData' ] [ 'results' ]	
	return results

def get_results_from_tutorials(advanced_query):
	google_results = apiGoogle(advanced_query)
	if google_results:
		url = google_results[0]['url']
		print(url)
		html = ur.urlopen(url)
		soup = BeautifulSoup(html,'lxml')
		#get images
		if (getImages(soup)):
			print("Images are there")
		else:
			pass			
		content_soup = BeautifulSoup(html.read(),'lxml')
		html.close()	
		w_html = open("tutorial_text.html","w")
		w_html.write(str(soup))
		w_html.close()
		r_html = open("tutorial_text.html").read()
		open("tutorial_normalized_text.txt","w").write(html2text.html2text(r_html))
		return True
	else:
		return False

def normalizeTextFile():
	f = open('tutorial_normalized_text.txt','r')
	lines = f.readlines()

	result=''
	pattern = ['    *' , ' *' , '[__' , '[' , '* * *' , 'Advertisements' , '#  [' , '"tutorialspoint" )' , '  * [' , '  *     *' , '  * Learn Web Services' , '  * Web Services Resources' , '  * Selected Reading' , '©' , 'go']
	for line in lines:
		# print(line)
		if line[0]=='!' or line[0]=='_':
			pass
		elif( line.startswith(tuple(pattern))):
			pass
		elif( '.jpg' in line ):
			pass
		else:
			result = result + line

	g = open('final_tutorial_normalized_text.txt','w').write(result)

def getImages(soup):
	data = soup.find('div',class_="col-md-7 middle-col")
	img = data.find('img')
	if img is not None:
		src = img["src"]
		final_src="http://www.tutorialspoint.com" + src
		img = ur.urlopen(final_src)
		with open(str(input_query) + '.jpg','wb') as localFile:
			localFile.write(img.read())
		return True
	else:
		return False		


def main():
	scraping_websites= 'site:www.tutorialspoint.com'
	advanced_query =  scraping_websites + ' ' + input_query
	print(advanced_query)

	results_tutorials = get_results_from_tutorials(advanced_query)
	# results_tutorials = get_html_tutorials(advanced_query)
	if (results_tutorials):
		normalizeTextFile()
		pass
	else:
		print('TUTORIALS POINT FAILED')	

	os.system('rst2html.py -q final_tutorial_normalized_text.txt > final.html')	
	f=open('final.html','r')
	soup = BeautifulSoup(f.read(),'lxml')
	try:
		for tag in soup.find('div',class_='system-messages section'):
			tag.replaceWith('')
	except:
		pass
	try:
		for tag in soup.find_all('div',class_='system-message'):
			tag.replaceWith('')
	except:
		pass
if __name__ == "__main__":
	input_query = input( 'Query: ' )
	main()
# end if	