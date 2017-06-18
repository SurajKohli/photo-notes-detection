import pickle
import operator
from collections import Counter

def check_if_one_level(topic_list):
	prev = len(topic_list[0].split('.'))
	for i in range(1,len(topic_list)):
		present = topic_list[i].split(" ")
		if( prev!=present ):
			return False
	return True


def find_common_topic(topic_list):
	new_topic_list = [x[0] for x in topic_list]
	counts = Counter(new_topic_list)
	max_value = counts[max(counts, key = counts.get)]
	dupids = [x for x in new_topic_list if counts[x] == max_value]
	#keep only that in dupids
	print(max_value)
	print(new_topic_list)
	print(dupids)
	changed_list = list()
	for i in topic_list:
		if str(i[0]) in dupids:
			changed_list.append(i)
	print("Final output")
	print(changed_list)
	print("====")
	return changed_list

with open('all_datasets.p', 'rb') as handle:
	all_dataset = pickle.loads(handle.read())

with open('known_topics_dict.p','rb') as handle:
	known_topics_dict = pickle.loads(handle.read())

f = open('Result/word_list.txt','r')
lines = f.readlines()
input_dict = dict()
final_lines = list()
for line in lines:
	final_lines.append(line.strip('\n'))
for line in final_lines:
	if line in all_dataset:
		# print(line)
		# print(all_dataset[line])
		for topic in all_dataset[line]:
			if topic in input_dict:
				input_dict[topic] = input_dict[topic] + 1
			else:
				input_dict[topic] = 1

for topic in input_dict:
	print(topic, '=>' , input_dict[topic])

max_value = input_dict[max(input_dict, key = input_dict.get)]
print(max_value)

max_topics = list()
for topic in input_dict:
	if(input_dict[topic] == max_value):
		max_topics.append(str(topic))
		print(topic)

print(max_topics)
if( len(max_topics) == 1 ):
	topic = known_topics_dict[str(max_topics[0])]
	if 'Summary' in topic:
		topic_str = max_topics[0][0]
		print(topic_str)
		topic = known_topics_dict[topic_str]
else:
	common_topic = find_common_topic(max_topics)
	if( len(common_topic) == 1 ):
		topic = known_topics_dict[common_topic[0]]
		if 'Summary' in topic:
			topic_str = common_topic[0][0]
			topic = known_topics_dict[topic_str]
	else:
		topics = list()
		for i in common_topic:
			sub_topic = known_topics_dict[i]
			if 'Summary' in sub_topic:
				sub_topic = known_topics_dict[i[0]]
			topics.append(sub_topic)
		topic = " , ".join(topics)


print("========================================================================================")
print("****************************************************************************************")
print('\n')
print('\n')
print("The topic being talked about is approximately")
print('\n')
print('\n')
print('\n')
print(topic)
print('\n')
print('\n')
print("*****************************************************************************************")
print("=========================================================================================")


final_topic_list = topic.split(',')
print(final_topic_list)
with open('Result/topic_list.txt','w') as f:
	f.write("\n".join(final_topic_list))
f.close()  