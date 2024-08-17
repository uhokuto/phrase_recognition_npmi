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

    def __init__ (self, ):
        self.bigram_dic={}
        self.unigram_dic={}
        self.bi_uni_mapping={}
        self.pmi_val = {}
        self.word_count=0
        
        

    def calc_pmi(self,sentence):
        
        
        japanese = re.compile("[一-龥ぁ-んァ-ンー。、々a-zA-Z]+")  
        sentence_list = re.findall(japanese,sentence)
        sentence = ''.join(sentence_list)
        #mecab = MeCab.Tagger ('mecabrc')
        mecab = MeCab.Tagger ("mecabrc")
        #t.parseToNode('') 
        word_vector = []    
        
        #mecab.parse('')
        token=mecab.parseToNode(sentence)   
        
        prev_word=''
        while token:
            self.word_count+=1
            features=token.feature.split(',')
            hinsi=features[0]
            
            kihonkei = features[6]
            
            if  hinsi!= '動詞' :
                word = token.surface
            else:
                word = kihonkei
            
            if word not in  self.unigram_dic:
                self.unigram_dic[word] = 1
            else:
                self.unigram_dic[word] += 1
                
            if prev_word !='':
                bigram = prev_word + word    
                
                if bigram not in self.bigram_dic:
                    self.bigram_dic[bigram] = 1
                    self.bi_uni_mapping[bigram] = [prev_word,word]
                    
                else:
                    self.bigram_dic[bigram] += 1
            
                
            prev_word = word                
            token = token.next
        
        
        for k,v in self.bigram_dic.items():
        
            if v>3:
                w1 = self.unigram_dic[self.bi_uni_mapping[k][0]]
                w2 = self.unigram_dic[self.bi_uni_mapping[k][1]]
                pmi_val = np.log((v/self.word_count)/((w1/self.word_count)*(w2/self.word_count)))/(-np.log(v/self.word_count))
          
                self.pmi_val[k] = pmi_val



