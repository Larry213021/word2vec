import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from boltons.iterutils import remap
import string

identity_list = []
ICD10_list_all = {}
ICD10_list_all_2 = set()

df = pd.read_csv('D:/nkust_1108_Lab\mimic_data\schizophrenia/test.csv')#mimic，csv檔案位置
name = "Word2vecschizophreniaCase_5.npy" #檔案名稱
disease_count = 20 #每個人平均疾病數量
vector = 8 #每個疾病的向量
df = df.fillna(0)
df = df[['subject_id','icd_code']]
groups = df.groupby('subject_id',sort = False)
np_data = np.zeros((len(groups), disease_count, vector))
group_count = 0

for count in range(len(df)):
    # print(count,"/",len(df))
    vectorlist1 = []
    ICD10_list = []
    if (df.iloc[count].at["subject_id"]) not in identity_list:
        identity_list.append(df.iloc[count].at["subject_id"])
        grp = groups.get_group(df.iloc[count].at["subject_id"])
        for i in range(len(grp)):
            if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                ICD10_list_all.setdefault(grp.iloc[i].at["icd_code"], )
        for i in range(len(grp)):
            if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                ICD10_list_all_2.add(grp.iloc[i].at["icd_code"])
        group_count+=1
        print(group_count, '/', len(groups))

ICD10_list_all_2 = str(ICD10_list_all_2)
ICD10_list_all_2 = ICD10_list_all_2.replace("'", '')
ICD10_list_all_2 = ICD10_list_all_2.replace(",", '')
ICD10_list_all_2 = ICD10_list_all_2.replace("{", '')
ICD10_list_all_2 = ICD10_list_all_2.replace("}", '')
ICD10_list_all_2 = ICD10_list_all_2.replace(".", '')

fmodelw = open("icd.txt", "w")
fmodelw.write(ICD10_list_all_2)
fmodelw.close()

fmodelr = open("icd.txt")
word2veclist = open("word2vec.txt","w")

TB = fmodelr.read().splitlines()
TB = [x.split() for x in TB]
myWord2Vec1 = Word2Vec(TB, min_count=1, vector_size=vector, epochs=9, sg=1)
for x in range(len(myWord2Vec1.wv.index_to_key)):
    ICD10_list_all[myWord2Vec1.wv.index_to_key[x]] = myWord2Vec1.wv.vectors[x]
    word2veclist.writelines(str(myWord2Vec1.wv.index_to_key[x])+str(":")+str(myWord2Vec1.wv.vectors[x])+str("\n"))
    print(x, '/', len(myWord2Vec1.wv.index_to_key))
# 清除字典中的None
drop_falsey = lambda path, key, value: value is not None
ICD10_list_all = remap(ICD10_list_all, visit=drop_falsey)

word2veclist.close()



group_count = 0
identity_list = []
for count in range(len(df)):
    vectorlist1 = []
    ICD10_list = []
    if (df.iloc[count].at["subject_id"]) not in identity_list:
        identity_list.append(df.iloc[count].at["subject_id"])
        grp = groups.get_group(df.iloc[count].at["subject_id"])
        for i in range(len(grp)):
            if grp.iloc[i].at["icd_code"][0] in string.ascii_letters:
                ICD10_list.append(grp.iloc[i].at["icd_code"])
        ICD10_list = set(ICD10_list)
        ICD10_list = str(ICD10_list)
        ICD10_list = ICD10_list.replace("'", '')
        ICD10_list = ICD10_list.replace(",", '')
        ICD10_list = ICD10_list.replace("{", '')
        ICD10_list = ICD10_list.replace("}", '')
        ICD10_list = ICD10_list.replace(".", '')
        ICD10_list = ICD10_list.replace("set()", '')

        if len(ICD10_list) == 0:
            group_count += 1
            print(group_count, '/', len(groups))
            continue
        else:
            fmodelw = open("model.txt", "w")
            fmodelw.write(ICD10_list)
            fmodelw.close()

            fmodelr = open("model.txt")
            TB = fmodelr.read().splitlines()
            TB = [x.split() for x in TB]
            vectorlist1 = np.zeros((1, disease_count, vector))
            for x in range(min(len(TB[0]), disease_count)):
                vectorlist1[0][x] = ICD10_list_all[TB[0][x]]
            np_data[group_count] = vectorlist1
            group_count += 1

            print(group_count, '/', len(groups))
np.save(name, np_data)