
#Add folder Connection vào path để khi thực thi trên cmd, các file trong Connection nó cùng
# level với file thực thi
import sys
sys.path.insert(1, './Connection')
from bson.objectid import ObjectId
import pandas as pd
#print(sys.path)
import connectionDB as connDB

DB = connDB.connectionDB('','','AREA')

myColl = DB['province']
t = new ObjectId('5f94f327d90d01fb1ee0c535')
df = pd.DataFrame(list(myColl.find({'_id' : t})))
print(df)
#connDB.mycoll.delete_many({})



