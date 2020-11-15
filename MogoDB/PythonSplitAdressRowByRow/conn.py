
#Add folder Connection vào path để khi thực thi trên cmd, các file trong Connection nó cùng
# level với file thực thi
import sys
sys.path.insert(1, './Connection')

import pandas as pd
#print(sys.path)
import connectionDB as connDB

DB = connDB.connectionDB('','','AREA')

myColl = DB['province']
df = pd.DataFrame(list(myColl.find({_id : ObjectId('5f94f327d90d01fb1ee0c535')})))
print(df)
#connDB.mycoll.delete_many({})



