import itertools
import math
import argparse
import traceback
import time
import os
from datetime import date

class password_generator:
	def __init__(self, inputWords, maxinputwords, maxlen):
		self.inputWords = inputWords
		self.maxinputwords = maxinputwords
		self.maxlen = maxlen

		if maxinputwords==0:
			self.maxinputwords = len(self.inputWords)
		if maxlen!=0:
			tmp = self.__maxinputWords_by_len()
			if tmp < maxinputwords:
				self.maxinputwords = tmp

	def npr(self, n, r):
		return (stirling(n)/stirling(n-r) if n > 20 else
			math.factorial(n)/math.factorial(n-r))

	@staticmethod
	def yob_filter(s):
		try:
			s = int(s)
			if s>=1900 and s<=date.today().year:
				return str(s)[2:4]
			return False
		except Exception, e:
			return False

	@staticmethod
	def clear_emptyword(words):
		for i in range(0,len(words)):
			if words[i] == "":
				del words[i]
		return words

	def output_counter(self):
		count = 0
		for i in range(1, self.maxinputwords+1):
			count += self.npr(len(self.inputWords),i)
		return count
	
	def output_generator(self):
		res = []
		for i in range(1, self.maxinputwords+1):
			for x in itertools.combinations(self.inputWords,i):
				if not (len(str(''.join(x))) <= self.maxlen or self.maxlen == 0):
					continue
				for y in itertools.permutations(x,i):
					res.append(''.join(y))
		return res

	@staticmethod
	def newword_filter(words, transform):
		tmp = words
		for word in tmp:
			if transform == 1:
				if word.title() != word:
					words.append(word.title())
			y = password_generator.yob_filter(word)
			if y!=False:
				words.append(y)
		print words
		return password_generator.clear_emptyword(words)

	def __maxinputWords_by_len(self):
		sorted_inputWords = sorted(self.inputWords, key=len)
		wlen = 0
		count = 0
		for word in sorted_inputWords:
			wlen += len(word)
			if not wlen > self.maxlen:
				count += 1
			else:
				break
		return count


def write_file(p_file, data):
	try:
		foutput = open(p_file ,"w")
		foutput.write(data)
		foutput.close()
	except Exception, e:
		print e
		return False

def read_file(p_file):
	try:
		finput = open(p_file,"r")
		input = finput.read()
		finput.close()
		return input.split()
	except Exception, e:
		print e
		return False
	
def output(p_file, words, dtime):
	try:
		print "[*] Generated "+str(len(words))+" words in "+str(dtime)
		data = '\n'.join(words)
		write_file(p_file, data)
		print "[*] "+str(len(words))+" words were written to " + p_file
	except Exception, e:
		print(traceback.format_exc())

def main():
	global args

	parser = argparse.ArgumentParser(description='Password Generator by sting8k')
	parser.add_argument('-A','--add', help='Add words to a wordlist file named by -lst, split by [space]', default="")
	parser.add_argument('-T','--transform', help='Auto generate Uppercase to words in -A or -a argument', default=1)
	parser.add_argument('-m','--maxinputwords', help='Set Max input words to combine', default=0)
	parser.add_argument('-l','--maxlen', help='Set Max length of a word', default=0)
	parser.add_argument('-lst','--listword', help='Wordlist to combine', required=True, default="")
	parser.add_argument('-ext','--extendword', help='An extend wordlist', default="0")
	parser.add_argument('-o','--output', help='Output file', default="output.txt")
	args = vars(parser.parse_args())

	args['maxinputwords'] = int(args['maxinputwords'])
	args['maxlen'] = int(args['maxlen'])
	args['transform'] = int(args['transform'])

	inputWords = []

	if args['listword'] != "":
		if args['add'] != "":
			inputWords = password_generator.newword_filter(args['add'].split(), args['transform'])
		if os.path.isfile(args['listword']):
			inp = read_file(args['listword'])
			if inp!= False:
				old_words = password_generator.clear_emptyword(inp)
				inputWords = old_words + inputWords
			else:
				print "Cannot read file", args['listword']
			
		data = '\n'.join(inputWords)
		write_file(args['listword'], data)
			
	if args['extendword'] != "0":
		ext = read_file(args['extendword'])
		if ext != False:
			inputWords += ext

	PG = password_generator(inputWords, args['maxinputwords'], args['maxlen'])

	print "[*] Estimated ~"+str(PG.output_counter())+" words in list!"
	start = time.time()
	op = PG.output_generator()
	end = time.time()
	duration = end - start
	output(args['output'], op, duration)
	
if __name__ == "__main__":
	main()
