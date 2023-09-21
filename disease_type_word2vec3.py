from gensim.models import Word2Vec
from boltons.iterutils import remap
import os
import numpy as np
from IPython.display import clear_output

# 人數
personCount = 35304
#每個人平均得到多少疾病
disease_count = 80
#維度
vector = 5
#檔案位置
fileadress = 'D:/nkust_198_Lab/bipolar/person_disease/control_split_with_id_other_times/3_times'
#生成出來的檔案名
filename = "word2vecbipolarControl_5_3times.npy"

ICD9_list_all_set = set()
ICD9_list_all_dict = {}

np_data = np.zeros((personCount, disease_count, vector))

for count, info in enumerate(os.listdir(fileadress)):

    domain = os.path.abspath(fileadress)  # 獲取資料夾的路徑，此處其實沒必要這麼寫，目的是為了熟悉os的資料夾操作
    info = os.path.join(domain, info)  # 將路徑與檔名結合起來就是每個檔案的完整路徑
    info = open(info, 'r')  # 讀取檔案內容
    line = info.readlines()

    for data in line:
        icd = [data[53:59], data[59:65], data[65:71], data[71:77], data[77:83]]
        for x in icd:
            x = x.strip('\n')
            x = x.strip()
            x = x.strip('')
            x = x.strip(',')
            ICD9_list_all_set.add(x)
            ICD9_list_all_dict.setdefault(x, )

    clear_output(wait=True)
    print(count, "/", personCount)

ICD9_list_all_set = str(ICD9_list_all_set)
ICD9_list_all_set = ICD9_list_all_set.replace("'", '')
ICD9_list_all_set = ICD9_list_all_set.replace(",", '')
ICD9_list_all_set = ICD9_list_all_set.replace("{", '')
ICD9_list_all_set = ICD9_list_all_set.replace("}", '')
ICD9_list_all_set = ICD9_list_all_set.replace(".", '')

fmodelw = open("icd.txt", "w")
fmodelw.write(ICD9_list_all_set)
fmodelw.close()

fmodelr = open("icd.txt")
word2veclist = open("word2vec.txt","w")

TB = fmodelr.read().splitlines()
TB = [x.split() for x in TB]
myWord2Vec1 = Word2Vec(TB, min_count = 1, vector_size = vector, epochs=9, sg=1)
for x in range(len(myWord2Vec1.wv.index_to_key)):
    ICD9_list_all_dict[myWord2Vec1.wv.index_to_key[x]] = myWord2Vec1.wv.vectors[x]
    word2veclist.writelines(str(myWord2Vec1.wv.index_to_key[x])+str(":")+str(myWord2Vec1.wv.vectors[x])+str("\n"))
    print(x, '/', len(myWord2Vec1.wv.index_to_key))

# 清除字典中的None
drop_falsey = lambda path, key, value: value is not None
ICD9_list_all_dict = remap(ICD9_list_all_dict, visit=drop_falsey)

word2veclist.close()



for count, info in enumerate(os.listdir(fileadress)):

    vectorlist1 = []
    vectorlist2 = []
    word_list = []

    fmodelw = open("model.txt", "w")
    domain = os.path.abspath(fileadress)  # 獲取資料夾的路徑，此處其實沒必要這麼寫，目的是為了熟悉os的資料夾操作
    info = os.path.join(domain, info)  # 將路徑與檔名結合起來就是每個檔案的完整路徑
    info = open(info, 'r')  # 讀取檔案內容
    line = info.readlines()

    for data in line:
        icd = [data[53:59], data[59:65], data[65:71], data[71:77], data[77:83]]
        for x in icd:
            x = x.strip('\n')
            x = x.strip()
            x = x.strip('')
            x = x.strip(',')
            word_list.append(x)
    word_list = set(word_list)
    word_list = str(word_list)
    word_list = word_list.strip('\n')
    word_list = word_list.strip()
    word_list = word_list.replace("'", '')
    word_list = word_list.replace(",", '')
    word_list = word_list.replace(".", '')
    word_list = word_list.replace("{", '')
    word_list = word_list.replace("}", '')
    fmodelw.write(word_list)
    fmodelw.close()

    fmodelr = open("model.txt")
    TB = fmodelr.read().splitlines()
    TB = [x.split() for x in TB]

    vectorlist1 = np.zeros((1, disease_count, vector))
    for x in range(min(len(TB[0]), disease_count)):
        vectorlist1[0][x] = ICD9_list_all_dict[TB[0][x]]
    np_data[count] = vectorlist1

    clear_output(wait=True)
    print(count, "/", personCount)

np.save(filename, np_data)