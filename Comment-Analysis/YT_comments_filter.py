import nltk 
import re

def append_if_english(list, percent):
    words = set(nltk.corpus.words.words())
    list_new = []
    for line in list:
        content = line.split("\t")
        id = content[0]
        author = content[1]
        comment = content[2]

        #tokenize comment
        tokens_com = nltk.wordpunct_tokenize(comment)

        #delete if no english words
        english = 0
        non_english = len(tokens_com)
        my_exceptions = ["el", "mi", "de", "viva", "sin", "y", "es", "las", "ne", "l", "la", "se", "lo", "hasta", "fin", "no"]
        for token in tokens_com:
            if token.lower() in words and token.lower() not in my_exceptions:
                english += 1
            elif token.lower() in words and len(tokens_com) == 1:
                english += 100
            elif token == " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                non_english -= 1

        if non_english == 0:
            non_english = 0.1
        perc_en = english/non_english
        if perc_en > percent:
            list_new.append(line)
            
    return list_new

def english_true(comment, percent):
    result = False
    words = set(nltk.corpus.words.words())
    
    #tokenize comment
    tokens_com = nltk.wordpunct_tokenize(comment)
    
    #delete if no english words
    english = 0
    non_english = len(tokens_com)
    my_exceptions = ["el", "mi", "de", "viva", "sin", "y", "es", "las", "ne", "l", "la", "se", "lo", "hasta", "fin", "no"]
    
    for token in tokens_com:
        if token.lower() in words and token.lower() not in my_exceptions:
            english += 1
        elif token.lower() in words and len(tokens_com) == 1:
            english += 100
        elif token == " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
            non_english -= 1

    if non_english == 0:
        non_english = 0.1
    perc_en = english/non_english
    if perc_en > percent:
        result = True
    else:
        result = False
    
            
    return result

def load_tsv_list_id_name(filename, id_name):
    list = ["old_id\tauthor\tcomment\tid_name"]
    with open(filename, 'r') as content:
        for i, line in enumerate(content.readlines()):

            if i == 0:
                continue #skip first line

            try:
                line = line.strip()
                line = line + "\t" + id_name

                #test if all columns have values
                content = line.split("\t")
                id = content[0]
                author = content[1]
                comment = content[2]
                list.append(line)
            except IndexError:
                continue
            except Exception as e:
                print(e)
    return list

def load_tsv_list(filename):
    list = []
    with open(filename, 'r') as content:
        for i, line in enumerate(content.readlines()):

            try:
                line = line.strip()
                
                #test if all columns have values
                content = line.split("\t")
                id = content[0]
                author = content[1]
                comment = content[2]
                
                list.append(line)
            except IndexError:
                continue
            except Exception as e:
                print(e)
    return list

def comments_inone_string(lst):
    doc = ""
    for line in lst:
        content = line.split("\t")
        comments = content[2]
        doc = doc + comments
    print(len(doc))
    return doc


def remove_emojis_string(text):
    regrex_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return regrex_pattern.sub(r'',text)

def emojies_re_pattern():
    regrex_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return regrex_pattern



