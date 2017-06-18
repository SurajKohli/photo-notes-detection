import urllib.parse 
import urllib.request as ur
import json as m_json
from bs4 import BeautifulSoup
import wikipedia
import html2text
import sys
import os
## added after google search API change
import requests

def apiGoogle(advanced_query):
	query = { 'q' : advanced_query }
	data = requests.get( 'https://www.googleapis.com/customsearch/v1?key=' + googleCustomSearchKEY + '&cx=' + googleCX, params=query)
	print(data.url)
	json = data.json()
	#changed google search API
	#check if json contains 'items' as key or not
	size=0
	if 'items' in json:
		results = json['items']
		size = len(results)
		if( size > 4 ):
			size = 4
	else:
		results = []
	return results,size

def get_results_from_tutorials(advanced_query):
	#changed google search API	
	google_results,size = apiGoogle(advanced_query)	
	if google_results:
		url = google_results[0]['link']
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

	#SKD Result directory
	f = open('Result/final_tutorial_normalized_text.txt','a')
	f.write("Topic ==== " + str(sys.argv[1]))
	f.write("\n\n")
	f.write(result)
	f.write("========================================")
	f.write("\n\n")

def getImages(soup):
	data = soup.find('div',class_="col-md-7 middle-col")
	if data is not None:
		imgs = data.find_all('img')
		count = 1
		if imgs is not None:
			for img in imgs:
				if img is not None:
					src = img["src"]
					final_src="http://www.tutorialspoint.com" + src
					img = ur.urlopen(final_src)
					#SKD Result directory					
					with open('Result/tutorialspoint_' + str(count) + '.jpg','wb') as localFile:
						localFile.write(img.read())
					count = count + 1

		else:
			return False
	else:
		return False
	
	return True
				

def main():
	scraping_websites= 'site:www.tutorialspoint.com'
	advanced_query =  scraping_websites + ' ' + input_query
	print(advanced_query)

	results_tutorials = get_results_from_tutorials(advanced_query)
	if (results_tutorials):
		normalizeTextFile()
	else:
		print('TUTORIALS POINT FAILED')

	#SKD Result directory
	os.system('rst2html -q Result/final_tutorial_normalized_text.txt > Result/final_extensive_notes.html')	

	#SKD Result directory
	os.system('rst2html -q Result/scraped_definition_results.txt > Result/final_short_notes.html')

	os.system('python3 p_summy.py')




if __name__ == "__main__":
	input_query = sys.argv[1]
	# googleCustomSearchKEY = 'AIzaSyAJQhdm0WxZLvVUZSSOlbSxeFT8Hk-TPJE'
	# googleCX = '002807431072145729011:tpfqp_wap68'	
	googleCustomSearchKEY = 'AIzaSyBouXo-OoUMQ_W0IyTnV3OdC8swQqSIBns'
	googleCX = '011137880050561842421:lmcvarrvifo'	
	main()
# end if	