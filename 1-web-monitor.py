#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

# check for web
def check_web(url,port):
    # method 1:ncat
    value = os.popen("nc -z -w 5 %s %s && echo 1" % (url,port)).read()
    if int(value) == 1:

    # method 2:telnet
    # if int(os.popen("echo -e '\n'|telnet %s %s |grep Connected|wc -l" \
    #                % (url,port)).read()) == 1:

    # method 3:nmap
    # os.system("a=$(which nmap &>/dev/null;echo $?);  \
    #            [[ $a -ne 0 ]] && yum -y install nmap"
    #           )
    # if int(os.popen("nmap %s -p %s|grep open|wc -l" \
    #                 % (url,port)).read()) == 1:

    # method 4:curl
    # if int(os.popen('curl -l http://%s 2>/dev/null \
    #                |egrep \"200|302|301\"|wc -l' \
    #                % (url)).read()) == 1:


    # method 5:curl
    #my_curl="curl -I -s -o /dev/null -w '%{http_code}\n'"
    #code=int(os.popen("%s %s" % (my_curl,url)).read())
    #if code == 200:

        print('web is ok','\t','[\033[1;32mTrue\033[0m]')
    else:
        print('web is not ok','\t','[\033[1;31mFalse\033[0m]')

# main
def main(url,port):
    check_web(url,port)

if __name__ == '__main__':
    port = '80'
    url = 'www.baidu.com'
    while 1:
        main(url,port)
        sleep(3)