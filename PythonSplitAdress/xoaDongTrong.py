import pandas as pd
import numpy as np
import csv
import re

#chỉ cần thay đổi tên file đầu vào là được
#Goi lệnh: python sliptAddress.py
fileName = 'hcm_restaurantResult.csv'

df = pd.read_csv(fileName)
fileNameResult = 'NhaHangFinish.csv'
# Get names of indexes for which column Age has value 30

nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset = ['title'], inplace = True)
df.to_csv(fileNameResult,index=False, encoding='utf-8-sig')
