import pymongo
#Trả về kết nối tới một server
def connServer(serverURL = "localhost", port = "27017"):
    connServer = pymongo.MongoClient("mongodb://"+str(serverURL)+":"+str(port)+"/")
    return connServer