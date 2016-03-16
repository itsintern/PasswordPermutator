import itertools
import math
import argparse
import traceback
import time

from datetime import date

cur_year = date.today().year

argwtf = {}


def npr(n,r):
	return (stirling(n)/stirling(n-r) if n>20 else
		math.factorial(n)/math.factorial(n-r))

def maxitem_by_len(lstword):
	sort_lst = sorted(lstword, key=len)
	mlen = 0
	tmp = 0
	for word in lstword:
		mlen += len(word)
		if not mlen>argwtf['maxlen']:
			tmp += 1
		else:
			break
	return tmp

def counting(lstword):
	count = 0
	maxitem = argwtf['maxitem']
	if maxitem==0:
		maxitem = len(lstword)

	for i in range(1,maxitem+1):
		count+=npr(len(lstword),i)
	return count
	
def generate(lstword):
	res = []
	maxitem = argwtf['maxitem']
	if maxitem==0:
		maxitem = len(lstword)

	for i in range(1,maxitem+1):
		for x in itertools.combinations(lstword,i):
			if not (len(str(''.join(x)))<=argwtf['maxlen'] or argwtf['maxlen']==0):
				continue
			for y in itertools.permutations(x,i):
				res.append(''.join(y))

	return res

def clean_lstword(words):
	for i in range(0,len(words)):
		if words[i] == "":
			del words[i]
	return words

def chk_file(p_file):
	try:
		finput = open(p_file,"r")
		input = finput.read()
		finput.close()
		return input.split()
	except Exception, e:
		print e
		return False
		
def render_append():
	try:
		check = chk_file(argwtf['listword'])
		if check!=False:
			old_words = clean_lstword(check)
			new_words = clean_lstword(argwtf['append'].split())
			return old_words+new_word(new_words,argwtf['transform'])
		print "Cannot open file", argwtf['listword']
		return False
	except Exception, e:
		print(traceback.format_exc())
		return False
		
def yob(s):
	try:
		s = int(s)
		if s>=1900 and s<=cur_year:
			return str(s)[2:4]
		return False
	except Exception, e:
		return False

def new_word(words,transform):
	newwd = words
	if transform == 1:
		for word in newwd:
			if word.title() != word:
				newwd.append(word.title())
			y = yob(word)
			if y!=False:
				newwd.append(y)
	return newwd
	
def output(words,dtime):
	try:
		print "[*] Generated "+str(len(words))+" words in "+str(dtime)
		data = '\n'.join(words)
		foutput = open(argwtf['output'],"w")
		foutput.write(data)
		foutput.close()
		print "[*] "+str(len(words))+" words were written to "+argwtf['output']
	except Exception, e:
		print(traceback.format_exc())

parser = argparse.ArgumentParser(description='Password Generator by sting8k')
parser.add_argument('-A','--add', help='Add words to a wordlist file named by -lst, split by [space]', default="")
parser.add_argument('-a','--append', help='Append words to an existing wordlist file called by -lst, split by [space]', default="")
parser.add_argument('-T','--transform', help='Auto generate Uppercase to words in -A or -a argument', default=1)
parser.add_argument('-m','--maxitem', help='Set Max items to combine', default=0)
parser.add_argument('-l','--maxlen', help='Set Max length of a word', default=0)
parser.add_argument('-lst','--listword', help='Wordlist to combine', required=True, default="")
parser.add_argument('-ext','--extendword', help='An extend wordlist', default="0")
parser.add_argument('-o','--output', help='Output file', default="output.txt")

args = vars(parser.parse_args())
argwtf = args
argwtf['maxitem'] = int(argwtf['maxitem'])
argwtf['maxlen'] = int(argwtf['maxlen'])
argwtf['transform'] = int(argwtf['transform'])


if argwtf['add'] != "":
	rs = new_word(argwtf['add'].split(),argwtf['transform'])
	data = '\n'.join(rs)
	f= open(argwtf['listword'],"w")
	f.write(data)
	f.close()

if argwtf['append'] != "":
	rs = render_append()
	if rs!=False:
		data = '\n'.join(rs)
		f= open(argwtf['listword'],"w")
		f.write(data)
		f.close()

if chk_file(argwtf['listword']) != False:
	rs = chk_file(argwtf['listword'])
	if argwtf['extendword'] != "0":
		if chk_file(argwtf['extendword']) != False:
			rs += chk_file(argwtf['extendword'])

	if argwtf['maxlen']!=0:
		tmp = maxitem_by_len(rs)
		if tmp<argwtf['maxitem']:
			argwtf['maxitem']=tmp

	print "[*] Estimated ~"+str(counting(rs))+" words in list!"

	start = time.time()
	op = generate(rs)
	end = time.time()
	duration = end - start
	output(op,duration)
	
	

