import pickle

with open('all_datasets.p', 'rb') as handle:
	all_dataset = pickle.loads(handle.read())

with open('known_topics_dict.p','rb') as handle:
	known_topics_dict = pickle.loads(handle.read())

f = open('input.txt','r')
lines = f.readlines()
input_dict = dict()
final_lines = list()
for line in lines:
	final_lines.append(line.strip('\n'))

for line in final_lines:
	if line in all_dataset:
		# print(line)
		# print(all_dataset[line])
		print(line, "====" , all_dataset[line])
		for topic in all_dataset[line]:
			if topic in input_dict:
				input_dict[topic] = input_dict[topic] + 1
			else:
				input_dict[topic] = 1
