#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

# 需要提前部署一台memcache虚拟机用于测试
# 这里memcache的ip为192.168.4.200,memcache默认端口为11211

# judge about memcache status
def judge(status,mem_ip,port):
    if not status == 'good':
        print('memcache is \t[\033[1;31mDOWN\033[0m]')
        cmd3 = 'time echo stats |nc '+mem_ip+' '+port+' &>/dev/null'
        os.system(cmd3)
    print('memcache is \t[\033[1;32mUP\033[0m]')

# define variables to test response time and hit rate
def define_var(mem_ip,port):
    cmd4 = "echo stats |nc "+mem_ip+" "+port+"|grep 'get_hits'|awk '{print $3}'"
    cmd5 = "echo stats |nc " + mem_ip + " " + port + "|grep 'get_misses'|awk '{print $3}'"
    hit = int(os.popen(cmd4).read())
    miss = int(os.popen(cmd5).read())
    all = hit + miss
    rate = hit / all
    print("the memcache hit is ",rate)

def main(mem_ip,port):
    cmd1 = 'printf "set test 0 0 4\r\ngood\r\n"|nc '+mem_ip+' '+port
    cmd2 = "printf 'get test\n'|nc "+mem_ip+" "+port+"|awk 'NR==2{print $0}'"
    os.system(cmd1)
    status = str(os.popen(cmd2).read().split('\n')[0])
    print(status)
    judge(status,mem_ip,port)
    define_var(mem_ip,port)

if __name__ == '__main__':
    mem_ip = '192.168.4.200'
    port = '11211'
    main(mem_ip,port)