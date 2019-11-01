#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

# judge if log exists and create
def create_log(log,content):
    if not os.path.exists(log):
        print("[\033[1;34mFile doesn't exists,Creating now...\033[0m]")
        sleep(1)
        os.mknod(log)
    log_content = os.popen(content).read()
    with open(log,'w') as f:
        f.write(log_content)
    f.close()

# add ip ,which concurrency larger than 100, in to iptables
def add_tables(log):
    ip_list = os.popen("awk '$1>100{print $2}' %s" % log).read().split()
    for ip in ip_list:
        ip_num = int(os.popen("iptables -nL|grep %s|wc -l" % ip).read())
        if ip_num <= 1:
            os.system("iptables -I INPUT -s %s -j DROP" % ip)
            print("ip: [\033[1;31m%s\033[0m] has been droped" % ip)

# define main function
def main(log,content):
    create_log(log,content)
    while 1:
        add_tables(log)
        sleep(3)


if __name__ == '__main__':
    log = '/tmp/ipdos.log'
    content = "netstat -an | grep ESTABLISHED |" \
              "awk '{print $5}'|awk -F':' '{print $1}' |" \
              "sort|uniq -c"
    main(log,content)