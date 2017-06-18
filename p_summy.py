#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in

file = "Result/final_tutorial_normalized_text.txt" #name of the plain-text file
parser = PlaintextParser.from_file(file, Tokenizer("english"))
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, 20) #Summarize the document with 5 sentences

# for sentence in summary:
#     print(sentence)

with open('Result/summary_extensive.html','w') as f:
	f.write('<!DOCTYPE html><html><head><title>EXTENSIVE NOTES</title></head><body style="background-color:#FFCC99"><div style="color:blue;font-size:150%;background-color:#FF9966">')
	for sentence in summary:
		f.write(str(sentence))
		f.write('<br>')
	f.write('</div></body></html>')

definition_file = "Result/scraped_definition_results.txt"
f = open(definition_file,'r')
defintions = f.readlines()
topic = ''
result = ''
topic_definiton = dict()
for definition in defintions:
	# print(definition)
	if '===' in definition:
		continue
	if definition.startswith('Topic:'):
		topic = definition[6:]
		print(topic)
	if definition.startswith('Result:'):
		result = definition[7:]
		# print(topic)
		# print(result)
		topic_definiton[topic] = result
		# topic = ''
		# result = ''
	else:
		result = result + definition
		topic_definiton[topic] = result

with open('Result/summary_short.hmtl','w') as f:
	f.write('<!DOCTYPE html><html><head><title>SHORT NOTES</title></head><body style="background-color:#FFCC99"><table cellspacing="15" cellpadding="10" border="3" style="color:blue;width:100%;font-size:150%;background-color:#FF9966">')
	for topic in topic_definiton:
		if topic == '':
			continue
		else:
			f.write('<tr><td>'+str(topic)+'</td><td>'+str(topic_definiton[topic])+'</td></tr>')
	f.write('</table></body></html>')
