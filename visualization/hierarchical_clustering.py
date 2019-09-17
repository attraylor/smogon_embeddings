from sklearn.manifold import TSNE
from sklearn.decomposition import PCA #Grab PCA functions
import matplotlib.pyplot as plt

import utils


from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

words, words_to_wvs, vecs = utils.get_words_and_vectors("wvs.txt")


edited_ou_list = "Alakazam,Azumarill,Blacephalon,Celesteela,Chansey,Charizard,Clefable,Diancie,Excadrill,Ferrothorn,Garchomp,Gliscor,Greninja,Gyarados,Hawlucha,Heatran,Jirachi,Kartana,Keldeo,Kommo,Kyurem,Landorus,Lopunny,Magearna,Magnezone,Mawile,Medicham,Mew,Pelipper,Rotom,Scizor,Serperior,Skarmory,Swampert,Tangrowth,Bulu,Fini,Koko,Lele,Tornadus,Toxapex,Tyranitar,Victini,Volcarona,Zapdos"
ou_words = [x.lower() for x in edited_ou_list.split(",")]

l = linkage([words_to_wvs[word] for word in ou_words], method='complete', metric='seuclidean')

# calculate full dendrogram
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.ylabel('word')
plt.xlabel('distance')

dendrogram(
    l,
    leaf_rotation=0.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    orientation='left',
    leaf_label_func=lambda v: ou_words[v])
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
