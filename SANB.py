import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split


myDict = {}
catCount = [0,0]
stopwords = set(["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

def removeStoppers(bagOfWords):
	bagOfWords = list(set(bagOfWords) - stopwords)
	bagOfWords = [w for w in bagOfWords if len(w)>2]
	return

def stemming(bagOfWords):
	# Need to stem
	return

def makeWords(sentence):
	bagOfWords = sentence.split(' ')
	removeStoppers(bagOfWords)
	stemming(bagOfWords)
	return bagOfWords

def makeDict(myDict,catCount,sentence,label):
	#need to remove stopper words and do lemmization
	bagOfWords = makeWords(sentence)
	for word in bagOfWords:
		if(word not in myDict):
			myDict[word] = [0,0]
		myDict[word][label] += 1
	catCount[label] += 1

def calcProb(w,label):
	try:
		P = (0.5 + wordVector.loc[w].iloc[label]/catCount[label])/2;
	except:
		P = 1
	return P

def Classifier(sentence,threshold):
	bagOfWords = makeWords(sentence)
	posProb,negProb = 1,1
	for w in bagOfWords:
		posProb *= calcProb(w,0)
	for w in bagOfWords:
		negProb *= calcProb(w,1)
	posProb *= catCount[0]
	negProb *= catCount[1]
	if(posProb > 2*negProb):
		return 0
	return 1

def naiveBayesian(testData,threshold=0.5):
	correct,wrong = 0,0
	for i in range(len(testData)):
		predictedClass = Classifier(testData.iloc[i,0],threshold)
		if(predictedClass == testData.iloc[i,1]):
			correct += 1
		else:
			wrong += 1
	return correct,wrong

def Analyser(corpus):
	data = open(corpus).read()
	labels, texts = [],[]
	myData = data.split("\n")
	myData = myData[:-1]
	for line in myData:
		temp = line.split(' ')
		label = ord(temp[0][-1]) - ord('0')
		#1 - neg 0 - pos
		labels.append(label%2)
		texts.append(' '.join(temp[1:]))

	DF = pd.DataFrame()
	DF['text'] = texts
	DF['label'] = labels
	DF = shuffle(DF)
	trainData,testData = train_test_split(DF,test_size = 0.25)
	for i in range(len(trainData)):
		makeDict(myDict,catCount,trainData.iloc[i,0],trainData.iloc[i,1])
	wordVector = pd.DataFrame.from_dict(myDict,orient='index')
	(correct,wrong) = naiveBayesian(testData)
	accuracy = (correct*100.0)/(correct+wrong)
	print("Correctly predicted : " + str(correct) + " among " +  str(len(testData)) + " sentences")
	print("Accuracy : " + str(accuracy))

Analyser('amazon.txt')
