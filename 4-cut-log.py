#!/root/桌面/shell_to_python/venv/bin/python
import os
import datetime
import shutil
from time import sleep

# judge for closing httpd or not
def judge_port():
    if os.popen("netstat -atnup | grep ':80'").read():
        print("[\033[1;34mPort 80 has been used,Closing now...\033[0m]")
        sleep(1)
        os.system("systemctl stop httpd")

# judge for installing nginx or not
def judge_nginx_exist():
    exist = int(os.popen("rpm -qa nginx |wc -l").read())
    if exist == 0:
        print("[\033[1;34mYou have no nginx server,Installing now...\033[0m]")
        sleep(2)
        yum_path = "/etc/yum.repos.d/nginx.repo"
        if not os.path.exists(yum_path):
            with open(yum_path,'a+') as f:
                f.write("[nginx]\n")
                f.write("name=nginx repo\n")
                f.write("baseurl=http://nginx.org/packages/centos/$releasever/$basearch/\n")
                f.write("gpgcheck=0\n")
                f.write("enabled=1")
            f.close()
        os.system("yum -y install nginx; systemctl restart nginx")
        os.system("systemctl enable nginx")

# move log to datetime-log
def mv_log(logs_path):
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    log_now = logs_path+'access.log'
    log_cut = logs_path+str(yesterday)+'-access.log'
    shutil.move("%s" % (log_now), "%s" % (log_cut))

# create a new log file
def send_signal(pid_path):
    with open(pid_path,'r') as f:
        pid = f.read()
    f.close()
    os.system("kill -USR1 %s" % pid)

# main
def main(logs_path,pid_path):
    judge_port()
    judge_nginx_exist()
    mv_log(logs_path)
    send_signal(pid_path)
    print("#" * 30)
    print('log cut successful!','\t','[\033[1;32mTrue\033[0m]')

if __name__ == '__main__':
    logs_path = '/var/log/nginx/'
    pid_path = '/var/run/nginx.pid'
    main(logs_path,pid_path)