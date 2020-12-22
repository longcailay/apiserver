import connectionServer
#trả về kết nối tới một database của một server
def connectionDB(serverURL,port,databaseName):
    connServer = None
    if (serverURL == '') and (port == ''):
        connServer = connectionServer.connServer()
    else:
        connServer = connectionServer.connServer(serverURL, port)
    connDB = connServer[databaseName]
    return connDB

#Trả về kết nối tới một database của Atlas
def connectionDBAtlas(databaseName):
    return connectionServer.connServerAtlas()[databaseName]

#Trả về kết nối tới một database của Atlas
def connectionDBAtlas2(databaseName):
    return connectionServer.connServerAtlas2()[databaseName]

