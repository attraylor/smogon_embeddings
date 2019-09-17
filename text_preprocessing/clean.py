# Construction 2
from spacy.lang.en import English
from nltk.tokenize import MWETokenizer
import sys
import os
nlp = English()
# Create a Tokenizer with the default settings for English
# including punctuation rules and exceptions
tokenizer = nlp.Defaults.create_tokenizer(nlp)
mwe_tokenizer = MWETokenizer()
with open("text_preprocessing/mwes.txt") as rf:
	for mwe in rf:
		mwe_tokenizer.add_mwe(mwe.strip().split(" "))
new_dir = "tokenized_text"
if not os.path.exists(new_dir):
	os.makedirs(new_dir)
dirs = ["parsed_text", "parsed_text/contributions-corrections", "parsed_text/smogon-metagames"]
for dir in dirs:
	for f in os.listdir(dir):
		if ".txt" in f:
			print(f)
			with open(os.path.join(dir, f)) as rf:
				s = rf.read()
			remove_punctuation = str.maketrans("", "", "\'!\"#$%&\'()*+,:;<=>?[\\]^`{|}~_’")
			s = s.translate(remove_punctuation)
			tokens = tokenizer(s)
			tokens = [token.text for token in tokens if not token.is_space]
			tokens = mwe_tokenizer.tokenize(tokens)
			with open(os.path.join(new_dir, f), 'w+') as wf:
				for token in tokens:
					if token in ".!?":
						wf.write("\n")
					else:
						wf.write(token)
						wf.write(" ")
				wf.flush()
				wf.close()
