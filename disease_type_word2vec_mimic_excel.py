import pandas as pd
from gensim.models import Word2Vec
import numpy as np
from boltons.iterutils import remap

identity_list = []
ICD_list_all = {}
ICD_list_all_2 = set()

df = pd.read_csv('D:/nkust_1108_Lab\mimic資料集\Psychosis/Psychosis.csv')#mimic，csv檔案位置
name = "Word2vecPsychosis_8.npy" #檔案名稱
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
    ICD_list = []
    if (df.iloc[count].at["subject_id"]) not in identity_list:
        identity_list.append(df.iloc[count].at["subject_id"])
        grp = groups.get_group(df.iloc[count].at["subject_id"])
        print(len(grp)) # 計算目前此 subject_id 的長度
        print(grp) # 看此 subject_id 他配到的疾病代碼是哪些

        for i in range(len(grp)):
            ICD_list_all.setdefault(grp.iloc[i].at["icd_code"], )
        for i in range(len(grp)):
            ICD_list_all_2.add(grp.iloc[i].at["icd_code"])
        group_count+=1
        print(group_count, '/', len(groups))

print(ICD_list_all)
ICD_list_all_2 = str(ICD_list_all_2)
ICD_list_all_2 = ICD_list_all_2.replace("'", '')
ICD_list_all_2 = ICD_list_all_2.replace(",", '')
ICD_list_all_2 = ICD_list_all_2.replace("{", '')
ICD_list_all_2 = ICD_list_all_2.replace("}", '')
ICD_list_all_2 = ICD_list_all_2.replace(".", '')

fmodelw = open("icd.txt", "w")
fmodelw.write(ICD_list_all_2)
fmodelw.close()

fmodelr = open("icd.txt")
word2veclist = open("word2vec.txt","w")

TB = fmodelr.read().splitlines()
TB = [x.split() for x in TB]
myWord2Vec1 = Word2Vec(TB, min_count=1, vector_size=vector, epochs=9, sg=1)
for x in range(len(myWord2Vec1.wv.index_to_key)):
    ICD_list_all[myWord2Vec1.wv.index_to_key[x]] = myWord2Vec1.wv.vectors[x]
    word2veclist.writelines(str(myWord2Vec1.wv.index_to_key[x])+str(":")+str(myWord2Vec1.wv.vectors[x])+str("\n"))
    print(x, '/', len(myWord2Vec1.wv.index_to_key))
# 清除字典中的None
drop_falsey = lambda path, key, value: value is not None
ICD_list_all = remap(ICD_list_all, visit=drop_falsey)

word2veclist.close()







group_count = 0
identity_list = []
for count in range(len(df)):
    vectorlist1 = []
    ICD_list = []
    if (df.iloc[count].at["subject_id"]) not in identity_list:
        identity_list.append(df.iloc[count].at["subject_id"])
        grp = groups.get_group(df.iloc[count].at["subject_id"])
        for i in range(len(grp)):
            ICD_list.append(grp.iloc[i].at["icd_code"])
        ICD_list = set(ICD_list)
        ICD_list = str(ICD_list)
        ICD_list = ICD_list.replace("'", '')
        ICD_list = ICD_list.replace(",", '')
        ICD_list = ICD_list.replace("{", '')
        ICD_list = ICD_list.replace("}", '')
        ICD_list = ICD_list.replace(".", '')

        if len(ICD_list) == 0:
            continue
        else:
            fmodelw = open("model.txt", "w")
            fmodelw.write(ICD_list)
            fmodelw.close()

            fmodelr = open("model.txt")
            TB = fmodelr.read().splitlines()
            TB = [x.split() for x in TB]
            vectorlist1 = np.zeros((1, disease_count, vector))
            for x in range(min(len(TB[0]), disease_count)):
                vectorlist1[0][x] = ICD_list_all[TB[0][x]]
            np_data[group_count] = vectorlist1
            group_count += 1

            print(group_count, '/', len(groups))
np.save(name, np_data)