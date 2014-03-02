# -*- coding: utf-8 -*-


from pattern.vector import Document, Model, TFIDF, SVM, kfoldcv,REGRESSION,RADIAL,CLASSIFICATION
from pattern.db import csv 
from sys import argv
import jieba
import json

# extraversion, agreeable, conscientiousness, neuroticism, openness
category = ['ext', 'agr', 'con', 'neu', 'ope'] 

# open the corpus file
data = csv('./csv/corpus.csv')

# create the document.vector
data_doc = {}
for cate in category:
    data_doc[cate] = []
for text, ext, agr, con, neu, ope in data:
    data_doc['ext'].append(Document(' '.join(jieba.cut(text)), type = int(ext)==1))
    data_doc['agr'].append(Document(' '.join(jieba.cut(text)), type = int(agr)==1))
    data_doc['con'].append(Document(' '.join(jieba.cut(text)), type = int(con)==1))
    data_doc['neu'].append(Document(' '.join(jieba.cut(text)), type = int(neu)==1))
    data_doc['ope'].append(Document(' '.join(jieba.cut(text)), type = int(ope)==1))

# create the TFIDF model
m = {}
for cate in category:
    m[cate] = Model(documents = data_doc[cate], weight=TFIDF)



#Accuracy, precision, recall, F1 score
#for cate in category:
#    print cate, kfoldcv(SVM, data_doc[cate], folds=10, k=100)

key = csv('./csv/keywords.csv')
keywords = {}
for cate in category:
    keywords[cate] = ['','']
keywords['ext'][1] = key[0][0].split()
keywords['ext'][0] = key[1][0].split()
keywords['agr'][1] = key[2][0].split()
keywords['agr'][0] = key[3][0].split()
keywords['con'][1] = key[4][0].split()
keywords['con'][0] = key[5][0].split()
keywords['neu'][1] = key[6][0].split()
keywords['neu'][0] = key[7][0].split()
keywords['ope'][1] = key[8][0].split()
keywords['ope'][0] = key[9][0].split()


# adding weights with keywords
new_data = {}
for cate in category:
    new_data[cate] = []
for cate in category:
    for n in range(len(data_doc[cate])):
        new_dict = {}
        for w in data_doc[cate][n].features:
            if w in keywords[cate][1] and data_doc[cate][n].type == True:
                new_dict[w] = data_doc[cate][n].vector[w] * 2 # double the weight
            elif w in keywords[cate][0] and data_doc[cate][n].type == False:
                new_dict[w] = data_doc[cate][n].vector[w] * 2 # double the weight
            else:
                new_dict[w] = data_doc[cate][n].vector[w]
        new_data[cate].append(Document(new_dict, type = data_doc[cate][n].type ))

svm = {}
for cate in category:
    svm[cate] = SVM(train = new_data[cate],type=CLASSIFICATION)#,kernel=RADIAL)
    #svm[cate] = NB(train = new_data[cate], method=MULTINOMIAL, alpha=0.0001)
# the weight of 愛 is doubled, since it is in the ext list
#for d,w in new_data['ext'][22].keywords(top=10):
#    print d,w


# read the subject data
#data_raw = open('/Users/ignacio/Documents/subject.txt').read().decode('utf-8')
#data_raw = '''真爛，不想可惜'''
#for n in range(20):
#    data_raw = data[n][0]
try:
    with open("./subjects/users.u%s.feed.json"%argv[1]) as f:
        fcontent=f.readlines()
        data_raw=' '.join(filter(None, [ s.get('description')  for s in [json.loads(jst) for jst in fcontent]]))
        #print data_raw
        #data_raw=argv[1]
        data_sub = ' '.join(jieba.cut(data_raw))
        #print data_sub
        f1=svm['ext'].classify(Document(data_sub))  
        f2=svm['agr'].classify(Document(data_sub))  
        f3=svm['con'].classify(Document(data_sub))  
        f4=svm['neu'].classify(Document(data_sub))  
        f5=svm['ope'].classify(Document(data_sub))
        print '{"EXT":%f,"AGR":%f,"CON":%f,"NEO":%f,"OPE":%f}'%(f1,f2,f3,f4,f5)
        #print f1,f2,f3,f4,f5
        #x1,x2,x3,x4,x5= int(svm['ext'].classify(Document(data_sub))) , int(svm['agr'].classify(Document(data_sub))) , int(svm['con'].classify(Document(data_sub))) , int(svm['neu'].classify(Document(data_sub))) , int(svm['ope'].classify(Document(data_sub)))
       # print 'Your personality is:'
       # print '  Extraversion:     ', int(svm['ext'].classify(Document(data_sub)))
       # print '  Agreeable:        ', int(svm['agr'].classify(Document(data_sub)))
       # print '  Conscientiousness:', int(svm['con'].classify(Document(data_sub)))
       # print '  Neuroticism:      ', int(svm['neu'].classify(Document(data_sub)))
       # print '  Openness:         ', int(svm['ope'].classify(Document(data_sub)))
except IOError:
    print '{"EXT":%f,"AGR":%f,"CON":%f,"NEO":%f,"OPE":%f}'%(0,0,0,0,0)
