import nltk, gensim
import os
nltk.download('stopwords')

s = []
stop = set(nltk.corpus.stopwords.words('english'))
dir = "documents"
for f in os.listdir(dir):
    with open(os.path.join(dir, f)) as rf:
        for line in rf:
            s.append([x.lower() for x in line.strip().split(" ") if x not in stop])
#model = gensim.models.Word2Vec()
model = gensim.models.Word2Vec(sentences=s, window=7, min_count=5, workers=4, sg=1)
#model.build_vocab(s)


with open("wvs.txt", "w+") as wf:
    for ct, word in enumerate(model.wv.index2word):
        wf.write("{}\t{}\n".format(word, " ".join([str(s) for s in model.wv[word]])))
