#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep


# check installing for mysql
def check_db_exist(user,passwd):
    status = int(os.popen("which mysql &>/dev/null; echo $?").read())
    if status != 0:
        print('Mariadb not exists,Please waiting for installing now...')
        sleep(2)
        os.system("yum -y install mariadb-server mariadb;"
                  "systemctl start mariadb;systemctl enable mariadb")
        print('Mariadb has been installed')
        print('#' * 30)
        print('Please waiting for adding user...')
        add_user_local="grant all on *.* to "+user+"@'localhost' identified by '"+passwd+"';"
        os.system('mysql -e "%s"' % (add_user_local))
        add_user_all = "grant all on *.* to "+user+"@'%' identified by '"+passwd+"';"
        os.system('mysql -e "%s"' % (add_user_all))
        sleep(2)
        print('Add user successful')

# check if mysql is actived
def check_db(user,passwd,ip,port):

    # method 1:lsof
    file="lsof -i:"+port+"|wc -l"
    if int(os.popen("%s" % (file)).read()) >= 1:

    # method 2:netstat
    # port_lines="netstat -tunlp | grep "+port+"|wc -l"
    # if int(os.popen("%s" % (port_lines)).read()) >= 1:

    # method 3:mysql
    # db_show='show databases;'
    # db_command="mysql -u"+user+" -p"+passwd+" -h"+ip+" -P"+port
    # db_list=os.popen("%s -e '%s' |wc -l" % (db_command,db_show)).read()
    # if int(db_list) >= 1:

        print('Mysql is ok', '\t', '[\033[1;32mTrue\033[0m]')
    else:
        print('Mysql is not ok', '\t', '[\033[1;31mFalse\033[0m]')


# main
def main(user,passwd,ip,port):
    check_db_exist(user,passwd)
    while 1:
        check_db(user,passwd,ip,port)
        sleep(3)

if __name__ == '__main__':
    port='3306'
    user='mha'
    passwd='123qqq...A'
    ip='127.0.0.1'
    main(user,passwd,ip,port)
