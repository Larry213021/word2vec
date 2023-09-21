import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from boltons.iterutils import remap

identity_list = []
ICD9_list_all = {}
ICD9_list_all_2 = set()

#excel檔案位置，都使用csv為最佳
df = pd.read_csv('D:/nkust_1108_Lab\disease_data\schizophrenia\excel版/case.csv')
#輸出的檔案
filename = "Word2vec_schizophrenia_5.npy"
df = df.fillna(0)
df = df[['identity','icd9_1','icd9_2','icd9_3','icd9_4','icd9_5']]
groups = df.groupby('identity',sort = False)

#np.zeros((人數, 每個人平均得到的疾病數, 每個疾病數維度))
np_data = np.zeros((len(groups), 80, 5))
group_count = 0

for count in range(len(df)):
    # print(count,"/",len(df))
    vectorlist1 = []
    ICD9_list = []
    if (df.iloc[count].at["identity"]) not in identity_list:
        identity_list.append(df.iloc[count].at["identity"])
        grp = groups.get_group(df.iloc[count].at["identity"])
        for i in range(len(grp)):
            ICD9_list_all.setdefault(grp.iloc[i].at["icd9_1"], )
            ICD9_list_all.setdefault(grp.iloc[i].at["icd9_2"], )
            ICD9_list_all.setdefault(grp.iloc[i].at["icd9_3"], )
            ICD9_list_all.setdefault(grp.iloc[i].at["icd9_4"], )
            ICD9_list_all.setdefault(grp.iloc[i].at["icd9_5"], )
        for i in range(len(grp)):
            ICD9_list_all_2.add(grp.iloc[i].at["icd9_1"])
            ICD9_list_all_2.add(grp.iloc[i].at["icd9_2"])
            ICD9_list_all_2.add(grp.iloc[i].at["icd9_3"])
            ICD9_list_all_2.add(grp.iloc[i].at["icd9_4"])
            ICD9_list_all_2.add(grp.iloc[i].at["icd9_5"])
        group_count+=1
        print(group_count, '/', len(groups))

ICD9_list_all_2 = str(ICD9_list_all_2)
ICD9_list_all_2 = ICD9_list_all_2.replace("'", '')
ICD9_list_all_2 = ICD9_list_all_2.replace(",", '')
ICD9_list_all_2 = ICD9_list_all_2.replace("{", '')
ICD9_list_all_2 = ICD9_list_all_2.replace("}", '')
ICD9_list_all_2 = ICD9_list_all_2.replace(".", '')

fmodelw = open("icd.txt", "w")
fmodelw.write(ICD9_list_all_2)
fmodelw.close()

fmodelr = open("icd.txt")
word2veclist = open("word2vec.txt","w")

TB = fmodelr.read().splitlines()
TB = [x.split() for x in TB]
myWord2Vec1 = Word2Vec(TB, min_count=1, vector_size=5, epochs=9, sg=1)
for x in range(len(myWord2Vec1.wv.index_to_key)):
    ICD9_list_all[myWord2Vec1.wv.index_to_key[x]] = myWord2Vec1.wv.vectors[x]
    word2veclist.writelines(str(myWord2Vec1.wv.index_to_key[x])+str(":")+str(myWord2Vec1.wv.vectors[x])+str("\n"))
    print(x, '/', len(myWord2Vec1.wv.index_to_key))
# 清除字典中的None
drop_falsey = lambda path, key, value: value is not None
ICD9_list_all = remap(ICD9_list_all, visit=drop_falsey)

word2veclist.close()







group_count = 0
identity_list = []
for count in range(len(df)):
    vectorlist1 = []
    ICD9_list = []
    if (df.iloc[count].at["identity"]) not in identity_list:
        identity_list.append(df.iloc[count].at["identity"])
        grp = groups.get_group(df.iloc[count].at["identity"])
        for i in range(len(grp)):
            ICD9_list.append(grp.iloc[i].at["icd9_1"])
            ICD9_list.append(grp.iloc[i].at["icd9_2"])
            ICD9_list.append(grp.iloc[i].at["icd9_3"])
            ICD9_list.append(grp.iloc[i].at["icd9_4"])
            ICD9_list.append(grp.iloc[i].at["icd9_5"])
        ICD9_list = set(ICD9_list)
        ICD9_list = str(ICD9_list)
        ICD9_list = ICD9_list.replace("'", '')
        ICD9_list = ICD9_list.replace(",", '')
        ICD9_list = ICD9_list.replace("{", '')
        ICD9_list = ICD9_list.replace("}", '')
        ICD9_list = ICD9_list.replace(".", '')

        if len(ICD9_list) == 0:
            continue
        else:
            fmodelw = open("model.txt", "w")
            fmodelw.write(ICD9_list)
            fmodelw.close()

            fmodelr = open("model.txt")
            TB = fmodelr.read().splitlines()
            TB = [x.split() for x in TB]
            vectorlist1 = np.zeros((1, 80, 5))
            for x in range(min(len(TB[0]), 80)):
                vectorlist1[0][x] = ICD9_list_all[TB[0][x]]
            np_data[group_count] = vectorlist1
            group_count += 1

            print(group_count, '/', len(groups))
np.save(filename, np_data)