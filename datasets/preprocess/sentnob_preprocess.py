# -*- coding: utf-8 -*-
"""preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1atbbUrZwdowHYIV7uOP8-0K0evwEpIgu
"""

# -*- coding: utf-8 -*-
"""preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1atbbUrZwdowHYIV7uOP8-0K0evwEpIgu
"""

import csv
import os
import pandas as pd
from sklearn.model_selection import train_test_split

def numerals_normalize( df ):

  for i in range(len(df)):
    words = df['sentence'][i].split()
    st = ''
    for word in words:
      if(st != ''):
        st += ' '
      if(word[0]>='0' and word[0] <='9' and word[-1]>='0' and word[-1] <='9'):
        st += "CC"
      else:
        st += word
    df['sentence'][i] = st

  return df


df_train = pd.read_csv("./SentNoB Dataset/Train.csv")
df_train = numerals_normalize( df_train )

df_val = pd.read_csv("./SentNoB Dataset/Val.csv")
df_val = numerals_normalize( df_val )

df_test = pd.read_csv("./SentNoB Dataset/Test.csv")
df_test = numerals_normalize( df_test )

df_train.to_csv('./SentNoB Dataset/Final_Train.csv', index = False)
df_val.to_csv('./SentNoB Dataset/Final_Val.csv', index = False)
df_test.to_csv('./SentNoB Dataset/Final_Test.csv', index = False)