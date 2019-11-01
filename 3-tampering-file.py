#!/root/桌面/shell_to_python/venv/bin/python
import os
from time import sleep

# generate md5 values
def md5_value(file):
    md5_file = file+".md5"
    os.system("md5sum %s > %s" % (file,md5_file))

# create test file to verify
def create_test_file(file,file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    os.system("cp /etc/passwd %s" % (file_path+file))
    os.mknod("%s.md5" % (file_path+file))
    file_full = file_path+file
    md5_value(file_full)

# check md5 value about page file
def check_www(file):
    md5_file = file+'.md5'
    value = os.popen("md5sum -c %s &>/dev/null;echo $?" % md5_file).read()
    if int(value) == 0:
         print('file has not been changed','\t','[\033[1;32mTrue\033[0m]')
    else:
         print('file has been changed','\t','[\033[1;31mFalse\033[0m]')

# create a test file for md5 verification
def make_test_file(file,file_path):
    print('%s not exist.' % (file))
    print('Creating test file now...')
    create_test_file(file, file_path)
    sleep(2)
    print('Creating file successfully!')
    sleep(1)

# main to circle
def main(file,file_path):
    while 1:
        if not os.path.exists(file_path+file):
            make_test_file(file,file_path)
        check_www(file_path+file)
        sleep(3)

if __name__ == '__main__':
    file_path = '/var/html/www/'
    file = 'test.log'
    os.system("LANG=en")
    main(file,file_path)
