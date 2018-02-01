import os

def isFlaskRunning():
    flag = False
    ps_res = os.popen('ps -A|grep flask').read()
    if ps_res != '':
        flag = True
    return flag

def startFlask():
    pass

if __name__ == '__main__':
    ''' check if flask is running,
    if not start the app'''
    isRunning = isFlaskRunning()
    if isRunning == False:
        startFlask()