import pexpect.pxssh

hostname='9.111.215.191'
username='root'
password='Passw0rd2018'

command = 'ls'

def connect(hostname,username,password):
    try:
        s = pexpect.pxssh()
        s.login(hostname,username,password)
        print(s)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    connect(hostname,username,password)