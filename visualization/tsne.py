from sklearn.manifold import TSNE
from sklearn.decomposition import PCA #Grab PCA functions
import matplotlib.pyplot as plt

words = []
words_to_wvs = {}
vecs = []
with open("wvs_mwes.txt") as rf:
	for line in rf:
		split_line = line.strip().split("\t")
		if len(split_line) == 2:
			word = split_line[0]
			#print(word)
			vec = [float(i) for i in split_line[1].split(" ")]
			words.append(word)
			vecs.append(vec)
			words_to_wvs[word] = vec


edited_ou_list = "Alakazam_-_Mega,Alakazam,Azumarill,Blacephalon,Celesteela,Chansey,Charizard_-_Mega_-_X,Charizard_-_Mega_-_Y,Charizard,Clefable,Diancie,Diancie_-_Mega,Excadrill,Ferrothorn,Garchomp,Garchomp_-_Mega,Gliscor,Greninja,Greninja_-_Ash,Gyarados,Gyarados_-_Mega,Hawlucha,Heatran,Jirachi,Kartana,Keldeo,Kommo_-_O,Kyurem_-_Black,Landorus_-_Therian,Lopunny_-_Mega,Lopunny,Magearna,Magnezone,Mawile,Mawile_-_Mega,Medicham_-_Mega,Medicham,Mew,Pelipper,Rotom_-_Wash,Scizor,Scizor_-_Mega,Serperior,Skarmory,Swampert,Swampert_-_Mega,Tangrowth,Tapu_Bulu,Tapu_Fini,Tapu_Koko,Tapu_Lele,Tornadus_-_Therian,Toxapex,Tyranitar,Tyranitar_-_Mega,Victini,Volcarona,Zapdos"

ou_words = []
for x in edited_ou_list.split(","):
	try:
		a = words_to_wvs[x.lower()]
		ou_words.append(x.lower())
	except KeyError:
		print("not found", x)
#ou_words = [x.lower() for x in edited_ou_list.split(",")]

pca = PCA(n_components=2)
result = pca.fit_transform([words_to_wvs[word] for word in ou_words])

#result = TSNE(n_components=2).fit_transform([words_to_wvs[word] for word in ou_words])
fig, ax = plt.subplots()
ax.plot(result[:, 0], result[:, 1], 'o')
ax.set_title('OU words')
ax.set_yticklabels([]) #Hide ticks
ax.set_xticklabels([]) #Hide ticks
for i, word in enumerate(ou_words):
	plt.annotate(word.replace("_-_", "-"), xy=(result[i, 0], result[i, 1]))
plt.show()

"""Alakazam-Mega
Azumarill
Blacephalon
Celesteela
Chansey
Charizard-Mega-X
Charizard-Mega-Y
Clefable
Diancie-Mega
Excadrill
Ferrothorn
Garchomp
Garchomp-Mega
Gliscor
Greninja
Greninja-Ash
Gyarados-Mega
Hawlucha
Heatran
Jirachi
Kartana
Keldeo
Kommo-o
Kyurem-Black
Landorus-Therian
Lopunny-Mega
Magearna
Magnezone
Mawile-Mega
Medicham-Mega
Mew
Pelipper
Rotom-Wash
Scizor-Mega
Serperior
Skarmory
Swampert-Mega
Tangrowth
Tapu Bulu
Tapu Fini
Tapu Koko
Tapu Lele
Tornadus
Toxapex
Tyranitar
Victini
Volcarona
Zapdos"""
