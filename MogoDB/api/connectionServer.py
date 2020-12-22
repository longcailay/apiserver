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

#Trả kết nối tới server atlas
def connServerAtlas2():
    password = urllib.parse.quote('admin123')
    connection_url = 'mongodb://admin:' + password + '@47.241.7.27:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    return pymongo.MongoClient(connection_url)
