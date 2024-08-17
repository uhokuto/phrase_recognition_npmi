import re
import pandas as pd
import codecs
import pickle
import numpy as np
import MeCab
import sys
import collections
import math

class pmi:

    def __init__ (self, max_n_gram):
        
        
        
        self.max_n_gram=max_n_gram
        self.bigramed_record={} #bigram化したフレーズをキー、それが生成されたn_gram再帰回数のvalue

    
    


    def exec_pmi(self,n_gram,tokens):
        self.unigram_dic={}
        self.bigram_dic={}
        self.bi_uni_mapping={}
        self.pmi_val={}
        self.word_count=0
        prev_word=''
        for word in tokens:
            self.word_count+=1
          
            if word not in self.unigram_dic and word !='':
                self.unigram_dic[word] = 1
            
            elif word !='':
                self.unigram_dic[word] += 1
                
            if prev_word !='' and word !='':
                bigram = prev_word + word    
                
                if bigram not in self.bigram_dic:
                    self.bigram_dic[bigram] = 1
                    self.bi_uni_mapping[bigram] = [prev_word,word]
                    
                else:
                    self.bigram_dic[bigram] += 1
            
                
            prev_word = word                
            
               
        bigramed_tokens = tokens
        word_list=[]
        for k,v in self.bigram_dic.items():        
            
            w1 = self.unigram_dic[self.bi_uni_mapping[k][0]]
            w2 = self.unigram_dic[self.bi_uni_mapping[k][1]]
            print(k,v,self.word_count)
            print(-np.log(v/self.word_count))
            if -np.log(v/self.word_count)==0:
                continue
            pmi_val = np.log((v/self.word_count)/((w1/self.word_count)*(w2/self.word_count)))/(-np.log(v/self.word_count))      
            print(pmi_val)
            if pmi_val >  0.5:
                idx = 0
                while self.bi_uni_mapping[k][0] in bigramed_tokens[idx:] :
                    
                    idx = bigramed_tokens.index(self.bi_uni_mapping[k][0],idx)   
                    if idx == len(bigramed_tokens)-1:
                        continue
                    if bigramed_tokens[idx+1] == self.bi_uni_mapping[k][1]:
                        bigramed_tokens[idx] = k
                        del bigramed_tokens[idx+1]
                        self.bigramed_record[k]=n_gram
                   
                    idx += 1   
                    
            
        if n_gram >=self.max_n_gram:
            return bigramed_tokens,self.bigramed_record
        
        n_gram+=1
        return self.exec_pmi(n_gram,bigramed_tokens)
            

