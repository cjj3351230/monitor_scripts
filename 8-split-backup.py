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
    # get databases except Database and schema
    cmd1 = mysqlcom+' -e "show databases;"|egrep -v "Database|schema"'
    # get the list of databases
    databases = os.popen(cmd1).read().split()
    for database in databases:
        # get tables about each database except table which named Tables_in_*
        cmd2 = mysqlcom + ' -e "show tables from '+database+';"|egrep -v "Tables_in_"'
        # get the list of tables for each database
        tables = os.popen(cmd2).read().split()
        # backup each table
        for t in tables:
            cmd3 = mysqldump+' '+database+' '+t+' |gzip >'+backup+'/'\
                   +database+'_'+t+'_$(date +%F).sql.gz'
            os.system(cmd3)

# define main function
def main(usr,pwd,socket):
    mysqldump = 'mysqldump -u'+usr+' -p'+pwd+' -S'+socket+' -x -F -R'
    mysqlcom = 'mysql -u' + usr + ' -p' + pwd
    judge_mysql(usr, pwd)
    create_backup(backup, mysqlcom, mysqldump)

if __name__ == '__main__':
    usr = 'root'
    pwd = '123qqq...A'
    socket = '/var/lib/mysql/mysql.sock'
    backup = '/var/sqlbackup2'
    main(usr,pwd,socket)