import nltk 
import re

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



