ip = 'dummy'
rest_ip = 'dummy'

def setIp(diff_ip):
    global ip
    ip = diff_ip
    return ip

def getIp():
    return ip

def setRestIp(diff_ip):
    global rest_ip 
    rest_ip = diff_ip
    return rest_ip

def getRestIp():
    return rest_ip