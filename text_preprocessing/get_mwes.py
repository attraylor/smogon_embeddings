import os
import json
mwes = []
mwe_file = "text_preprocessing/mwes.txt"
files = ["../metagrok/dex/BattleAbilities.json", "../metagrok/dex/BattlePokedex.json", \
	"../metagrok/dex/BattleItems.json", "../metagrok/dex/BattleMovedex.json"]
for file in files:
	with open(file) as rf:
		json_f = json.load(rf)
	for entity in json_f:
		if "name" in json_f[entity].keys():
			name = json_f[entity]["name"]
		else:
			name = json_f[entity]["species"]
		if " " in name:
			mwes.append(name)
		elif "-" in name:
			mwes.append(" - ".join(name.split("-")))

with open(mwe_file, "w+") as wf:
	for mwe in mwes:
		print(mwe)
		wf.write("{}\n".format(mwe))
