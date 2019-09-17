from annoy import AnnoyIndex
words = []
words_to_wvs = {}
import numpy as np
with open("wvs.txt") as rf:
    for line in rf:
        split_line = line.strip().split("\t")
        if len(split_line) == 2:
            word = split_line[0]
            #print(word)
            vec = [float(i) for i in split_line[1].split(" ")]
            words.append(word)
            words_to_wvs[word] = vec
w1 = "pikachu"
w2 = 'kanto'
w3 = "sinnoh"
w4 = "pachirisu"
words.append("vec({}) - vec({}) + vec({}) =".format(w1,w2,w3))
words_to_wvs["vec({}) - vec({}) + vec({}) =".format(w1,w2,w3)] = list(np.asarray(words_to_wvs[w1]) - np.asarray(words_to_wvs[w2]) + np.asarray(words_to_wvs[w3]))
t = AnnoyIndex(100, 'angular')  # Length of item vector that will be indexed
for ct,i in enumerate(words):
    t.add_item(ct, words_to_wvs[i])
t.build(100) # 10 trees

wwca = [w1,w2,w3,w4, "vec({}) - vec({}) + vec({}) =".format(w1,w2,w3)]
for word in wwca:
    print("10 NEAREST NEIGHBORS OF {}".format(word))
    nearest_neighbors = t.get_nns_by_item(words.index(word), 10)
    for nn in nearest_neighbors:
        print(words[nn])
