import pandas as pd
import numpy as np

df = pd.read_csv('D:\school\disease_type\Otitis Media\case.csv')
df2 = pd.read_csv('D:\school\disease_type\Otitis Media\control.csv')

identity_list = []
for count in range(len(df)):
    print(count+1,"/",len(df))
    if (df.iloc[count].at["identity"]) not in identity_list:
        identity_list.append(df.iloc[count].at["identity"])

identity_list2 = []
for count in range(len(df2)):
    print(count+1,"/",len(df2))
    if (df2.iloc[count].at["identity"]) not in identity_list2:
        identity_list2.append(df2.iloc[count].at["identity"])

for i in range(len(identity_list)):
    if (identity_list[i])  in identity_list2:
        print("yes")