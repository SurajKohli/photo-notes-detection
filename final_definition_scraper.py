import urllib.parse 
import urllib.request as ur
import json as m_json
from bs4 import BeautifulSoup
import wikipedia
import sys
## added after google search API change
import requests

def getContent(start):
	nextNode = start
	# print(nextNode)
	text = ""
	i = 0
	while True:
		i = i+1
		# print("----- " + str(i) +" -----")
		nextNode = nextNode.next
		# try:
		tag_name = nextNode.name
		# except AttributeError:
			# print("error")
			# tag_name = ""
		# print(tag_name)
		# print(nextNode)
		if( tag_name == "p"):
			try:
				text += nextNode.text
				# print(text)
			except:
				# For places where nextNode.string does not work
				text += str(nextNode)
				# print(text)
		elif(tag_name == "h2"):
			# print("REACHED")
			break
		else:
			pass
	return text	

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

def get_results_from_w3c(advanced_query):
	#changed google search API	
	google_results,size = apiGoogle(advanced_query)
	if google_results:
		i = 0
		while ( i != size ):
			#changed google search API
			url = google_results[i]['link']
			i = i + 1		
			html = ur.urlopen(url)
			soup = BeautifulSoup(html,'lxml')
			html.close()
			try:
				startAtDefinition = soup.find(text='Definition and Usage')
			except:
				continue
			#### Check if startAtDefinition in None
			if startAtDefinition is None:
				print("DEFINITION AND USAGE NOT FOUND");
				continue
			else:
				targetText = getContent(startAtDefinition)
				return (True,targetText)
	else:
		print('W3SCHOOLS FAILED')
		return (False,None)

	return (False,None)

def get_results_from_webopedia(advanced_query):
	google_results,size = apiGoogle(advanced_query)
	if google_results:
		#changed google search API		
		url = google_results[0]['link']
		html = ur.urlopen(url)
		soup = BeautifulSoup(html,'lxml')
		html.close()	
		startSpan = soup.find('span',class_='byline')
		targetText2 = getContent(startSpan)
		if targetText2 is '':
			print('WEBOPEDIA FAILED')
			return (False,None)
		else:
			return (True,targetText2)
	else:
		print('WEBOPEDIA FAILED')		
		return (False,None)

def get_results_from_wikipedia(advanced_query):
	wiki_list=wikipedia.search(advanced_query)
	wiki_page=wikipedia.page(wiki_list[0])
	f = open('wiki.txt','w')
	f.write(wiki_page.content)
	f.close()
	f = open('wiki.txt','r')
	lines = f.readlines()
	result = ''
	for line in lines:
		if((line[0] == "=") and (line[1] == "=")):
			break
		else:
			result = result + line

	return result

def write_to_output_file(results):
	#changed google search API
	#SKD Result directory	
	f = open('Result/scraped_definition_results.txt','a')
	f.write("Topic:" + str(sys.argv[1]) )
	f.write('\n===\n')
	f.write("Result:"+ results)
	f.write('\n===\n')
	f.close()
	
def main():
	#####
	# Start scraping Websites
	#####
	input_query = sys.argv[1]
	#advanced query includes google's site option
	scraping_websites= ['site:w3schools.com','site:webopedia.com','site:wikipedia.com']
	advanced_query =  scraping_websites[0] + ' ' + input_query
	print(advanced_query)
	#function which will scrape and get result from w3c

	# results_w3c( got results boolean, result string)
	results_w3c = get_results_from_w3c(advanced_query)
	if ( results_w3c[0] ):
		write_to_output_file( results_w3c[1] )
	else:
		# searching webopedia NOW
		advanced_query =  scraping_websites[1] + ' ' + input_query
		results_webopedia = get_results_from_webopedia(advanced_query)
		if ( results_webopedia[0] ):
			write_to_output_file( results_webopedia[1] )
		else:
			# searching wikipedia NOW
			results_wikipedia = get_results_from_wikipedia(input_query)
			write_to_output_file(results_wikipedia)



if __name__ == "__main__":
	# googleCustomSearchKEY = 'AIzaSyAJQhdm0WxZLvVUZSSOlbSxeFT8Hk-TPJE'
	# googleCX = '002807431072145729011:tpfqp_wap68'
	googleCustomSearchKEY = 'AIzaSyBouXo-OoUMQ_W0IyTnV3OdC8swQqSIBns'
	googleCX = '011137880050561842421:lmcvarrvifo'	
	main()
# end if