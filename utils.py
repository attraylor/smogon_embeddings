

def get_words_and_vectors(filename= "wvs.txt"):
    words = []
    words_to_wvs = {}
    vecs = []
    with open(filename) as rf:
        for line in rf:
            split_line = line.strip().split("\t")
            if len(split_line) == 2:
                word = split_line[0]
                #print(word)
                vec = [float(i) for i in split_line[1].split(" ")]
                words.append(word)
                vecs.append(vec)
                words_to_wvs[word] = vec
    return words, words_to_wvs, vecs
