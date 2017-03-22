import nltk

properties = {}
items = {}
def init():
	file = open('properties.txt','r')
	for line in file.readlines():
		line = line.strip().split('?')
		properties[line[0]] = line[1]
	file.close()
	with open('items.txt','r') as file:
		for line in file.readlines():
			line = line.strip().split('?')
			items[line[1]] = line[0]

def parseQP(query):
	init()
	ppt = ''
	wordArr = query
	for p in properties:
		try:
			if p in query:
				ppt = p
				wordArr = ' '.join(query.split(p))
				break
		except:
			continue
	wordArr = wordArr.split(' ')
	enStopWord = nltk.corpus.stopwords.words('english')
	enStopWord+= [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*']
	for word in wordArr:
		if word.lower() in enStopWord:
			wordArr.remove(word)
	wordArr = ' '.join(wordArr)
	for i in items:
		try:
			if i in wordArr:
				itt = items[i]
				break
		except:
			continue
	return [itt],ppt

	# wordArr = nltk.tokenize.word_tokenize(wordArr)

	# for i in range(len(wordArr)):
	# 	if wordArr[i].capitalize()==wordArr[i]:
	# 		j = i+1
	# 		while(j<len(wordArr) and wordArr[j].capitalize()== wordArr[j]):
	# 			j += 1
	# 		tmpWord = ' '.join(wordArr[i:j-1])
	# 		wordArr[i] = tmpWord
	# 		for k in range(i+1,j-1):
	# 			wordArr.pop(k)
	# 		i = j
	# 		break

	# print wordArr
	# outArr = []
	# enStopWord = nltk.corpus.stopwords.words('english')
	# enStopWord+= [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*']
	# for word in wordArr:
	# 	if not word in enStopWord:
	# 		outArr.append(word)
	# # wordArr = nltk.word_tokenize(' '.join(wordArr))
	# # nltk.pos_tag(wordArr)
	# return outArr[0],ppt

if __name__ == '__main__':
	print parseQP('What is the population of China')