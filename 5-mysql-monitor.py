#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

#install or start mariadb
# def install_mysql():
#     print("[\033[1;34mInstalling mariadb now...\033[0m]")
#     sleep(2)
#     os.system("yum -y install mariadb-server mariadb")
#     os.system("systemctl restart mariadb")
#     os.system("systemctl enable mariadb")
#     print("\033[1;34mMariadb installed successfully\033[0m]")
#     sleep(1)
#
#judge and start mysql
# def is_run(port):
#     cmd = "lsof -i:"+port+"|wc -l"
#     judge = int(os.popen(cmd).read())
#     if judge < 2:
#         print("[\033[1;34mMariadb has not started or installed\033[0m]")
#         judge_install = "rpm -qa *mariadb* |wc -l"
#         mariadb_packages = int(os.popen(judge_install).read())
#         # no mariadb in system
#         if mariadb_packages <= 1:
#             install_mysql()
#         # mariadb exists but not started
#         else:
#             os.system("systemctl restart mariadb")
#             os.system("systemctl enable mariadb")

# judge error about mysql-slave
def judge_error(MysqlCmd1,list_status,error_code):
    if list_status[2] in error_code:
        os.system("%s 'stop slave;SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;"
                  "start slave;'" % MysqlCmd1)
    else:
        a = list_status[2]
        print("mysql is [\033[1;31mfailed\033[0m],error id is [\033[1;31m%s\033[0m]" % a)

# judge status about mysql-slave
def judge_status(MysqlCmd1,list_status,error_code):
    if list_status[0] == 'Yes' and list_status[1] == 'Yes' \
           and list_status[3] == '2923':
        print('Mysql slave is OK','\t','[\033[1;32mTrue\033[0m]')
    else:
        judge_error(MysqlCmd1,list_status,error_code)


# main to circle
def main(port,MysqlCmd1,MysqlCmd2,error_code):
    list_status = os.popen(MysqlCmd2).read().split()
    while 1:
        #is_run(port)
        judge_status(MysqlCmd1,list_status,error_code)
        sleep(5)

if __name__ == '__main__':
    port = 3306
    MysqlCmd1 = "mysql -uroot -p192.168.51.9 -e"
    MysqlCmd2 = "cat mas_sla_test.txt | egrep '_Running|" \
                "Last_Errno|Behind_Master'|awk -F': ' '{print $NF}'|" \
                "awk 'NR<5{print}'"
    error_code = ('1158','1159','1008','1007','1062')

    main(port,MysqlCmd1,MysqlCmd2,error_code)
