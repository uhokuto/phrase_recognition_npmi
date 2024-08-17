import pandas as pd
import codecs
import numpy as np
import pmi_recursive
import MeCab
import re


def tokenize(sentence):
        
        
        japanese = re.compile("[一-龥ぁ-んァ-ンー。、々a-zA-Z]+")  
        sentence_list = re.findall(japanese,sentence)
        sentence = ''.join(sentence_list)
        #mecab = MeCab.Tagger ('mecabrc')
        mecab = MeCab.Tagger ("mecabrc")
        #t.parseToNode('') 
        word_vector = []    
        
        #mecab.parse('')
        token=mecab.parseToNode(sentence) 
        tokens =[]
        while token:
            features=token.feature.split(',')
            hinsi=features[0]
            kihonkei = features[6]
            if  hinsi!= '動詞' :
                tokens.append(token.surface)
            else:
                tokens.append(kihonkei)
            
            
            token=token.next
                
        return tokens



tsukurepo_df = pd.read_csv('tsukurepo_df.csv',  encoding='ms932', sep=',',skiprows=0)  
tsukurepo = tsukurepo_df['tsukurepo']
unigrams=[]
for t in tsukurepo:
    unigrams+=tokenize(t)
print(unigrams)
max_n=5
PMI = pmi_recursive.pmi(max_n)
n_grams,n_gramed_phrases_byn = PMI.exec_pmi(1,unigrams)
print(n_gramed_phrases_byn)

ph_ngram = []
for phrase,n_gram in n_gramed_phrases_byn.items():
    ph_ngram.append([n_gram+1,phrase])
phrase_df = pd.DataFrame(ph_ngram, columns=['n_gram','phrase'])

with codecs.open("npmi.csv", "w", "ms932", "ignore") as f: 
    #header=Trueで、見出しを書き出す
    phrase_df.to_csv(f, index=False, encoding="ms932", mode='w', header=True) 


'''
with codecs.open("n_grams.csv", "w", "ms932", "ignore") as f1: 
    #header=Trueで、見出しを書き出す
    n_grams.to_csv(f1, index=False, encoding="ms932", mode='w', header=True)
'''       
