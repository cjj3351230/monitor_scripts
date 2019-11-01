#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

# install mariadb
def judge_mysql(usr,pwd):
    status = int(os.popen("which mysql &>/dev/null; echo $?").read())
    if status != 0:
        print('Mariadb not exists,Please waiting for installing now...')
        sleep(2)
        os.system("yum -y install mariadb-server mariadb;"
                  "systemctl start mariadb;systemctl enable mariadb")
        print('Mariadb has been installed')
        print('#' * 30)
        print('Please waiting for adding user...')
        add_user_local = "grant all on *.* to " + usr + "@'localhost' identified by '" + pwd + "';"
        os.system('mysql -e "%s"' % (add_user_local))
        add_user_all = "grant all on *.* to " + usr + "@'%' identified by '" + pwd + "';"
        os.system('mysql -e "%s"' % (add_user_all))
        sleep(2)
        print('\033[1;34mAdd user successfully\033[0m]')

# create backup file for each database
def create_backup(backup,mysqlcom,mysqldump):
    if not os.path.exists(backup):
        os.mkdir(backup)
    cmd1 = mysqlcom+' -e "show databases;"|egrep -v "Database|schema"'
    databases = os.popen(cmd1).read().split()
    for database in databases:
        cmd2 = mysqldump+' '+database+'|gzip >'+backup+'/'+database
        cmd3 = cmd2+"_$(date +%F).sql.gz"
        os.system(cmd3)

# define main function
def main(usr,pwd,socket,backup):
    mysqldump = 'mysqldump -u'+usr+' -p'+pwd+' -S'+socket+' -x -B -F -R'
    mysqlcom = 'mysql -u'+usr+' -p'+pwd
    judge_mysql(usr,pwd)
    create_backup(backup,mysqlcom,mysqldump)

if __name__ == '__main__':
    usr = 'root'
    pwd = '123qqq...A'
    socket='/var/lib/mysql/mysql.sock'
    backup='/var/sqlbackup'
    main(usr,pwd,socket,backup)