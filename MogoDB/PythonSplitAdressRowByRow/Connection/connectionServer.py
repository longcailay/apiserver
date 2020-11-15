import pymongo
import urllib
#Trả về kết nối tới một server local
def connServer(serverURL = "localhost", port = "27017"):
    connServer = pymongo.MongoClient("mongodb://"+str(serverURL)+":"+str(port)+"/")
    return connServer

#Trả kết nối tới server atlas
def connServerAtlas():
    password = urllib.parse.quote('admin@123')
    connection_url = 'mongodb+srv://admin:' + password + '@succcessfullanddb.te07y.mongodb.net/SuccessfullLand_DB?retryWrites=true&w=majority'
    return pymongo.MongoClient(connection_url)