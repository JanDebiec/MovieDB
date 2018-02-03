import os

def isFlaskRunning():
    flag = False
    ps_res = os.popen('ps -A|grep flask').read()
    if ps_res != '':
        flag = True
    return flag

def startFlask():
    os.popen('/home/ubuntu/project/MovieDB/start_movie_db.sh')

if __name__ == '__main__':
    ''' check if flask is running,
    if not start the app'''
    isRunning = isFlaskRunning()
    if isRunning == False:
        print("starting movieDB")
        startFlask()
    else:
        print("flask app MovieDB is running")