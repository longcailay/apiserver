import pymongo
import urllib
#Trả về kết nối tới một server local
def connServer(serverURL = "localhost", port = "27017"):
    connServer = pymongo.MongoClient("mongodb://"+str(serverURL)+":"+str(port)+"/")
    return connServer

#Trả kết nối tới server atlas ông tín 500MB
def connServerAtlas():
    password = urllib.parse.quote('admin@123')
    connection_url = 'mongodb+srv://admin:' + password + '@succcessfullanddb.te07y.mongodb.net/SuccessfullLand_DB?retryWrites=true&w=majority'
    print(connection_url)
    return pymongo.MongoClient(connection_url)

#Trả kết nối tới server atlas trên máy ảo
def connServerAtlas2():
    password = urllib.parse.quote('admin123')
    connection_url = 'mongodb://admin:' + password + '@47.241.7.27:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
    return pymongo.MongoClient(connection_url)

#Trả kết nối tới server atlas của ông Hiển
def connServerAtlas3():
    # password = urllib.parse.quote('longho')
    connection_url = 'mongodb+srv://longho:longho@cluster0.0g1dc.mongodb.net/LongHoDB?ssl=true&ssl_cert_reqs=CERT_NONE'
    return pymongo.MongoClient(connection_url)


#Quan trọng, muốn kết nối từ máy ảo ubuntu ra mongodb atlas ta thêm "?ssl=true&ssl_cert_reqs=CERT_NONE" vào uri