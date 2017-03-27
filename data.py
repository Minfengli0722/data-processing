# data-processing
#read datas from excel to separate words and remove stopwords.
import pandas
from pandas import DataFrame, Series
import xlrd, os, re
from nltk.tokenize import WordPunctTokenizer
import nltk
import time

#Separating words and removing stopwords
def removeStopwords(origin, **kwargs):
    stopwords = kwargs["stopwords"]
    spliter = kwargs["spliter"]
    for index in origin.index:
        text = "".join(origin[index])
        words = set(spliter.tokenize(text))
        lasttext = ""
        for word in words:
            if word not in stopwords:
                 lasttext += "%s "%word
        origin.set_value(index, lasttext)
    return origin

#Deleting punctuation and converting upper to lower
def merge(series):
    text = "".join(series.astype("str")).lower()
    text = re.sub(r"[^a-z\s]", ' ', text)
    return text

def dataPreprocess(filename):
    if not os.path.exists(filename):
        print "File %s is not exists"%filename      
        exit(-1)
    print "Begin reading excel"
    
    data = pandas.read_excel(filename,parse_cols = 1)
    print "Finished reading excel"
    
    stopwords = set(nltk.corpus.stopwords.words("english"))
    spliter = WordPunctTokenizer()
    df = data.groupby('Label').aggregate(merge).apply(removeStopwords, stopwords=stopwords, spliter=spliter).reset_index()
    df.to_excel("pandas.xlsx")

if __name__ == "__main__":
    time1 = time.clock()
    dataPreprocess("customer_train.xls")
    time2 = time.clock()
    print "Read: %f s"%(time2 - time1)
    pass
