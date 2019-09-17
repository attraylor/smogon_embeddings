import json
import re
import os
from bs4 import BeautifulSoup
import argparse
#posts_on_page = []
parser = argparse.ArgumentParser()
parser.add_argument("--dir", default='')
args = parser.parse_args()
start_dir = 'scraped_content'
end_dir = 'parsed_text'
subdir = args.dir
complete_start = os.path.join(start_dir, subdir)
complete_end = os.path.join(end_dir, subdir)
if not os.path.exists(complete_end):
	os.makedirs(complete_end)

for f in os.listdir(complete_start):
	print(f)
	if ".json" in f:
		posts_on_page = []
		with open(os.path.join(complete_start, f)) as rf:
			for line in rf:
				posts_on_page.append(json.loads(line.strip()))
		filename = re.sub("\.json", ".txt", f)
		with open(os.path.join(complete_end, filename), "w+") as wf:
			for post in posts_on_page:
				if "title" in post.keys():
					title = re.sub(" \| Smogon Forums", "", post["title"])
					wf.write(title)
					wf.write("\n")
				else:
					soup = BeautifulSoup(post["post"])
					for div in soup.find_all("blockquote"):
						div.decompose()
					decomposed = soup.get_text()
					wf.write(decomposed)
					wf.write("\n")
