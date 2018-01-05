from pexpect import pxssh
import getpass


hostname = '9.111.215.191'
username = 'root'
password = 'Passw0rd2018'

try:
    s = pxssh.pxssh()
    # hostname = raw_input('hostname: ')
    # username = raw_input('username: ')
    # password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('uptime')   # run a command
    s.prompt()             # match the prompt
    print(s.before)        # print everything before the prompt.
    s.sendline('ls -l')
    s.prompt()
    print(s.before)
    s.sendline('df')
    s.prompt()
    print(s.before)
    s.logout()
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)