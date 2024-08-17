import pandas as pd
import codecs
import numpy as np
import pmi_recursive_bow
import MeCab
import re
import copy
import math

def tokenize(sentence):
        
        tokens =[]
        japanese = re.compile("[一-龥ぁ-んァ-ンー。、々a-zA-Z]+")  
        #print(sentence)
        if type(sentence) == float:
            tokens=[' ']
        else:    
            sentence_list = re.findall(japanese,sentence)
            
            sentence = ''.join(sentence_list)
            #mecab = MeCab.Tagger ('mecabrc')
            mecab = MeCab.Tagger ("mecabrc")
            #t.parseToNode('') 
            word_vector = []    
            
            #mecab.parse('')
            token=mecab.parseToNode(sentence) 
           
            while token:
                features=token.feature.split(',')
                hinsi=features[0]
                kihonkei = features[6]
                if  hinsi!= '動詞' :
                    tokens.append(token.surface)
                else:
                    tokens.append(token.surface)
                
                
                token=token.next
                
        return tokens



tsukurepo_df = pd.read_csv('../dataset/dataset_for_jtm(not -log).csv',  encoding='ms932', sep=',',skiprows=0)  
tsukurepo = tsukurepo_df['tsukurepos']
bow_unigrams=[]
w_count=0
for t in tsukurepo:
    words = tokenize(t)
    bow_unigrams.append(words)
    w_count+=len(words)
    
#bow_filter_unigrams =  copy.deepcopy(bow_unigrams)  
#max_n=5
#w_count=len(unigrams)
PMI = pmi_recursive_bow.pmi(w_count)
#threshold_n_gram = 2
n_grams_bow,n_gramed_phrases_byn = PMI.exec_pmi(1,bow_unigrams)
print(n_gramed_phrases_byn)

ph_ngram = []
for phrase,n_gram in n_gramed_phrases_byn.items():
    ph_ngram.append([n_gram+1,phrase])
phrase_df = pd.DataFrame(ph_ngram, columns=['n_gram','phrase'])

with codecs.open("../dataset/npmi_bow.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    phrase_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True) 
n_gram_bow_list = [ [' '.join(row)]  for row in n_grams_bow ] 
df=pd.DataFrame(n_gram_bow_list, columns=['phrased_sentences']) 
#n_gram_bow_filter_list = [ [' '.join(row)]  for row in n_grams_bow_filter ] 
#df2=pd.DataFrame(n_gram_bow_filter_list, columns=['phrased_filter_sentences']) 

df_r = df.reset_index()
tsukurepo_df = pd.concat([tsukurepo_df,df],axis=1)
with codecs.open("../dataset/tsukurepo_npmi_phrased.csv", "w", "ms932", "ignore") as f2: 
    #header=Trueで、見出しを書き出す
    tsukurepo_df.to_csv(f2, index=False, encoding="ms932", mode='w', header=True) 

'''
with codecs.open("n_grams.csv", "w", "ms932", "ignore") as f1: 
    #header=Trueで、見出しを書き出す
    n_grams.to_csv(f1, index=False, encoding="ms932", mode='w', header=True)
'''       
