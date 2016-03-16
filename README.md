### Password Generator by sting8k ###

A tool to generate password from words that user provide.

---


#### Usage

By typing `python bpwd.py -h usage`, you can list all arguments

```
usage: bpwd.py [-h] [-A ADD] [-T TRANSFORM] [-m MAXITEM]
               [-l MAXLEN] -lst LISTWORD [-ext EXTENDWORD] [-o OUTPUT]

Password Generator by sting8k

optional arguments:
  -h, --help            show this help message and exit
  -A ADD, --add ADD     Add words to a wordlist file named by -lst, split by
                        [space]
  -T TRANSFORM, --transform TRANSFORM
                        Auto generate Uppercase to words in -A argument
  -m MAXITEM, --maxitem MAXITEM
                        Set Max items to combine
  -l MAXLEN, --maxlen MAXLEN
                        Set Max length of a word
  -lst LISTWORD, --listword LISTWORD
                        Wordlist to combine
  -ext EXTENDWORD, --extendword EXTENDWORD
                        An extend wordlist
  -o OUTPUT, --output OUTPUT
                        Output file
```

#### Examples

Init the first wordlist with some words

```
> python bpwd.py -A "john 1992 28 01" -lst input.txt
[*] Estimated ~1956 words in list!
[*] Generated 1956 words in 0.00113391876221
[*] 1956 words were written to output.txt

```

Then we got a file named input.txt

```
john
1992
28
01
John
```

Output.txt
```
...
john19922801
john19920128
john28199201
john28011992
john01199228
john01281992
1992john2801
1992john0128
199228john01
...
```

---

Then if you want to add more words to this input.txt:
```
> python bpwd.py -A "cena sayian" -lst input.txt
[*] Estimated ~9864100 words in list!
[*] Generated 9864100 words in 6.22505402565
[*] 9864100 words were written to output.txt

```

We got this in input.txt

```
john
1992
28
01
John
92
cena
sayian
Cena
Sayian
```

And new output.txt
```
...
92011992
199201cena
1992cena01
011992cena
01cena1992
cena199201
cena011992
199201sayian
1992sayian01
...
```

If you always want to add characters or words like `$`, `123`, `@`,... then you should go like this:

`touch ext.txt`

```
@
123
$
```

```
> python bpwd.py -ext ext.txt -lst input.txt
[*] Estimated ~16926797485 words in list!
...

```


