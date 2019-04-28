#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Haoxian Hu, hhu28@fordham.edu

# estimated time: 20 min
# start time: 23:15 04/26/2018
# end time: 23:45 04/26/2018
# time used: 30 min

def nGrams():
    path_file = input('Please enter the path of the json file including ".json":\n')
    path_output = input('\nPlease enter the output path of the Excel file:\n')
    print('\nGenerating N-grams models..')
    
    import time
	import pandas as pd
    import nltk
    from nltk import sent_tokenize, word_tokenize, pos_tag, FreqDist
    from nltk.corpus import stopwords
    from nltk.util import ngrams
	
    #record the start time
    start = time.process_time()
    
    #read headlines and short_descriptions
    df = pd.read_json('{}'.format(path_file), lines=True)
    headline = df['headline']                              
    desc = df['short_description']
    
    #combine headline and short_descriptions
    raw1 = headline.append(desc)
    
    #replace '\u' with ' ' in the text
    raw2 = list(raw1.replace('u',' '))
    
    #change list into string
    str1 = "".join(raw2)
    tokens = nltk.word_tokenize(str1)
    
    #change all tokens into lower case  
    words1 = [w.lower() for w in tokens]                 
    
    #only keep text words, no numbers 
    words2 = [w for w in words1 if w.isalpha()]
    
    #remove stopwords such as "and", "or", making the result more meaningful
    stopwords = stopwords.words('english')
    words_nostopwords = [w for w in words2 if w not in stopwords]
    
    #reduce different tenses of the same word (e.g. 'ate', 'eaten' → 'eat') 
    porter = nltk.PorterStemmer()                         
    stem1 = [porter.stem(w) for w in words_nostopwords]
    wnl = nltk.WordNetLemmatizer()                        
    lemmatization = [wnl.lemmatize(w) for w in stem1]
    
    #Get the 1-gram frequency distribution in a decending order
    freq_word = FreqDist(lemmatization)                  
    sorted_freq_word = sorted(freq_word.items(),key = lambda k: k[1], reverse = True) 
    
    #name the two columns as 'word','frequency'
    sorted_freq_word = pd.DataFrame(sorted_freq_word)
    sorted_freq_word.columns = ['word','frequency']
    print('\nThe word frequency model is ready.')
    
    #Get the bigram frequency distribution in a decending order
    bigrams=list(ngrams(lemmatization,2))
    freq_bigrams = FreqDist(bigrams)                     
    sorted_freq_bigrams = sorted(freq_bigrams.items(),key = lambda k: k[1], reverse = True)
    
    #name the two columns as 'bigram','frequency'
    sorted_freq_bigrams = pd.DataFrame(sorted_freq_bigrams)
    sorted_freq_bigrams.columns = ['bigram','frequency']
    print('\nThe bigram model is ready.')
    
    print('\nGenerating Excel file..')
    #output two models into an Excel file

    with pd.ExcelWriter('{}\\N_grams_results.xlsx'.format(path_output)) as writer: 
        sorted_freq_word.to_excel(writer, index=False, sheet_name='word_frequency')
        sorted_freq_bigrams.to_excel(writer, index=False, sheet_name='bigrams')
    
    #record the end time
    end = time.process_time()
    
    print("\nN-grams models are ready.\n\nTime used in total:",round(end-start, 0),'s')
    
nGrams()

