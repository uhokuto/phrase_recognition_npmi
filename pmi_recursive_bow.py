import re
import pandas as pd
import codecs
import pickle
import numpy as np
import MeCab
import sys
import collections
import math
import copy

class pmi:

    def __init__ (self, word_count):  
        
        
        self.word_count = word_count
        self.bigramed_record={} #bigram化したフレーズをキー、それが生成されたn_gram再帰回数のvalue   
        self.bigramed_record_filter={}
    


    def exec_pmi(self,n_gram,bow_tokens):
        print('n_gram',n_gram)
        self.unigram_dic={}
        self.bigram_dic={}
        self.bi_uni_mapping={}
        self.pmi_val={}
        tokens=[]
        for doc in bow_tokens:
            tokens+=doc
            
        prev_word=''
        for word in tokens:
            #self.word_count+=1
          
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
            
               
        bigramed_bow_tokens = copy.deepcopy(bow_tokens)
        word_list=[]
        for k,v in self.bigram_dic.items():        
            
            w1 = self.unigram_dic[self.bi_uni_mapping[k][0]]
            w2 = self.unigram_dic[self.bi_uni_mapping[k][1]]
            #print(k,v)
            #print(-np.log(v/self.word_count))
            if -np.log(v/self.word_count) ==0:
                continue
            pmi_val = np.log((v/self.word_count)/((w1/self.word_count)*(w2/self.word_count)))/(-np.log(v/self.word_count))      
            #print(pmi_val,-np.log(v/self.word_count))
            if pmi_val >  0.5:
                
                for row in range(len(bigramed_bow_tokens)):
                    idx = 0
                    while self.bi_uni_mapping[k][0] in bigramed_bow_tokens[row][idx:] :
                        
                        idx = bigramed_bow_tokens[row].index(self.bi_uni_mapping[k][0],idx)   
                        if idx == len(bigramed_bow_tokens[row])-1:
                            break
                        if bigramed_bow_tokens[row][idx+1] == self.bi_uni_mapping[k][1]:
                            bigramed_bow_tokens[row][idx] = k
                            del bigramed_bow_tokens[row][idx+1]
                            if self.bigramed_record.get(k)==None:
                                self.bigramed_record[k]=n_gram
                                print(k,self.bigramed_record[k])
                        idx += 1 

                    
        count_bigram_now = 0
        count_bigram_prev =0
        for k,v in self.bigramed_record.items():# bigramフレーズ辞書 k フレーズ　v n gram 数
            if v==n_gram:
                count_bigram_now += 1
            elif v==n_gram-1:
                count_bigram_prev += 1
            
        if count_bigram_now == count_bigram_prev:#再帰終了条件　n gramがもはや増えなければ終了
            return bigramed_bow_tokens,self.bigramed_record
        
        n_gram+=1
        ngram = copy.deepcopy(n_gram)
        return self.exec_pmi(ngram,bigramed_bow_tokens)#bigramed_bow_tokensには、ngram フレーズ化した単語列が、もとのデータセットの２次元配列の状態で入っている
        
    
'''        
    def exec_pmi_filter(self,n_gram,bow_tokens,bow_filter_tokens,thres_n_phrase):
        self.unigram_dic={}
        self.bigram_dic={}
        self.bi_uni_mapping={}
        self.unigram_filter_dic={}
        self.bigram_filter_dic={}
        self.bi_uni_filter_mapping={}
        self.pmi_val={}
        tokens=[]
        filter_tokens=[]
        for doc,doc2 in zip(bow_tokens,bow_filter_tokens):
            tokens+=doc
            filter_tokens += doc2
            
        prev_word=''
        for word in tokens:
            #self.word_count+=1
          
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
            
        prev_word2=''
        for word2 in filter_tokens:
            #self.word_count+=1
          
            if word2 not in self.unigram_filter_dic and word2 !='':                
                self.unigram_filter_dic[word2]= 1
            
            elif word2 !='':                
                self.unigram_filter_dic[word2] += 1
                
            if prev_word2 !='' and word2 !='':                
                filter_bigram = prev_word2 + word2 
                
                if filter_bigram not in self.bigram_filter_dic:                    
                    self.bigram_filter_dic[filter_bigram] = 1  
                    bi = filter_bigram.replace('$','')
                    #assert self.bigram_dic.get(bi)!=None, 'bigram is not in bigram_dic {}'.format(filter_bigram)
                    self.bi_uni_filter_mapping[filter_bigram] = [prev_word2,word2]
                else:                    
                    self.bigram_filter_dic[filter_bigram] += 1                
             
            prev_word2 = word2
            
               
        bigramed_bow_tokens = copy.deepcopy(bow_tokens)
        bigramed_bow_filter_tokens = copy.deepcopy(bow_filter_tokens)
        word_list=[]
        #assert len(self.bigram_dic) == len(self.bigram_filter_dic), 'no of bigram dic unmatch {0} {1}'.format(len(self.bigram_dic),len(self.bigram_filter_dic))
        for (k,v),(kf,vf) in zip(self.bigram_dic.items(),self.bigram_filter_dic.items()):        
            
            w1 = self.unigram_dic[self.bi_uni_mapping[k][0]]
            w2 = self.unigram_dic[self.bi_uni_mapping[k][1]]
            #print(n_gram,k,v)
            #print(-np.log(v/self.word_count))
            if -np.log(v/self.word_count) ==0:
                continue
            pmi_val = np.log((v/self.word_count)/((w1/self.word_count)*(w2/self.word_count)))/(-np.log(v/self.word_count))      
            #print(pmi_val,-np.log(v/self.word_count))
            
            if pmi_val >  0.5:
                
                for row in range(len(bigramed_bow_tokens)):
                    idx = 0
                    #print(self.bi_uni_mapping[k][0])
                    while self.bi_uni_mapping[k][0] in bigramed_bow_tokens[row][idx:] :
                        #print(n_gram,self.bi_uni_mapping[k][0],bigramed_bow_tokens[row][idx:])
                        idx = bigramed_bow_tokens[row].index(self.bi_uni_mapping[k][0],idx) 
                        assert len(bigramed_bow_tokens[row][idx:]) == len(bigramed_bow_filter_tokens[row][idx:]),'{0}  {1}'.format(bigramed_bow_tokens[row][idx:],bigramed_bow_filter_tokens[row][idx:])
                        if idx == len(bigramed_bow_tokens[row])-1:                            
                            break
                            
                        if bigramed_bow_tokens[row][idx+1] == self.bi_uni_mapping[k][1]:                        
                            
                            bigramed_bow_tokens[row][idx] = k                            
                            del bigramed_bow_tokens[row][idx+1]
                            self.bigramed_record[k]=n_gram
                            
                            print(bigramed_bow_tokens[row][idx])
                            if n_gram <= thres_n_phrase:                            
                                bigramed_bow_filter_tokens[row][idx] = kf
                                #print(bigramed_bow_filter_tokens[row][idx])
                                del bigramed_bow_filter_tokens[row][idx+1]
                            elif n_gram > thres_n_phrase and :    
                                bigramed_bow_filter_tokens[row][idx] = self.bi_uni_filter_mapping[kf][0] + '$' + self.bi_uni_filter_mapping[kf][1]
                                del bigramed_bow_filter_tokens[row][idx+1]
                            print(bigramed_bow_filter_tokens[row][idx])
                            
                        idx += 1 
                        
                        
                        

                    
        count_bigram_now = 0
        count_bigram_prev =0
        for k,v in self.bigramed_record.items():
            if v==n_gram:
                count_bigram_now += 1
            elif v==n_gram-1:
                count_bigram_prev += 1
            
        if count_bigram_now == count_bigram_prev:
            return bigramed_bow_tokens,bigramed_bow_filter_tokens, self.bigramed_record
        
        n_gram+=1
        return self.exec_pmi_filter(n_gram,bigramed_bow_tokens,bigramed_bow_filter_tokens,thres_n_phrase)
'''        
        