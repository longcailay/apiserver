import connectionServer
def connectionDB(serverURL,port,databaseName):
    connServer = None
    if (serverURL == '') and (port == ''):
        connServer = connectionServer.connServer()
    else:
        connServer = connectionServer.connServer(serverURL, port)
    connDB = connServer[databaseName]
    return connDB

