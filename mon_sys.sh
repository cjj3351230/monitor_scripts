#!/bin/bash
#############################################
# a script for monitor Linux system status  #
#          update date: 2019-9-22           #
#############################################


#initialize and globalize variables
mem_total_kB='' 		#total memory size(kB)
mem_free_kB=''			#total free memory size(kB)
mem_used_rate=''		#memory used rate
swap_total=''			#swap space total size(kB)
swap_free=''			#swap free space total size(kB)
swap_used_rate=''		#swap used space rate
file_system_total=''		#total file system space size(kB)
file_system_free=''		#total file system free space size(kB)
file_system_used_rate=''	#file system used rate
block_size_all=0		#system block size(kB)
block_usedsize_all=0		#system used block size(kB)
local_ip_all=''			#all ip in this server


#get memory's informations
function get_mem_info(){
    mem_total_kB=$(cat /proc/meminfo | grep 'MemTotal' | awk '{print $2}')
    mem_free_kB=$(cat /proc/meminfo | grep 'MemFree' | awk '{print $2}')
    mem_used_rate=$(printf "%.2f" `echo "scale=2;($mem_total_kB-$mem_free_kB)/$mem_total_kB" | bc`)

#:<< !
    mem_total_GB=$(printf "%.2f" `echo "scale=2;$mem_total_kB/1024/1024" | bc` )
    mem_free_GB=$(printf "%.2f" `echo "scale=2;$mem_free_kB/1024/1024" | bc`) 
    echo -e "内存大小共计:\t\t"$mem_total_GB" GB"
    echo -e "内存空闲共计:\t\t"$mem_free_GB" GB"
    echo -e "内存使用率为:\t\t"$mem_used_rate" %"
#!
}

#get swap space's informations
function get_swap_info(){
    swap_total=$(cat /proc/meminfo | grep -w SwapTotal | awk '{print $2}')
    swap_free=$(cat /proc/meminfo | grep -w SwapFree | awk '{print $2}')
    if [ "$swap_total" -eq 0 ];then
	swap_used_rate=0
    elif [ "$swap_total" -ne 0 ];then
        swap_used_rate=$(printf "%.2f" `echo "scale=2;($swap_total-$swap_free)/$swap_total" | bc`)  
    else 
	echo -e "\033[31m GET SWAP INFOMATION ERROR\033[0m"
    fi

#:<< !
    echo -e "交换分区总空间:\t\t"$swap_total" kB"
    echo -e "交换分区空闲:\t\t"$swap_free" kB"
    echo -e "交换分区使用率:\t\t"$swap_used_rate" %"
#!
}

#get file system's informations
function get_file_system_info(){
    file_system_total=$(df | grep -w '/' | awk '{print $2}')
    file_system_free=$(df | grep -w '/' | awk '{print $4}')
    file_system_used_rate=$(df | grep -w '/' | awk '{print $5}' | awk -F% '{print $1}')
    
#:<< !
    file_system_total_GB=$(printf "%.2f" `echo "scale=2;$file_system_total/1024/1024" |bc`)
    file_system_free_GB=$(printf "%.2f" `echo "scale=2;$file_system_free/1024/1024" |bc`)
    echo -e "文件系统总空间:\t\t"$file_system_total_GB' GB'
    echo -e "文件系统剩余空间:\t"$file_system_free_GB' GB'
    echo -e "文件系统使用率:\t\t"$file_system_used_rate" %"
#!
}

function get_block_info(){
    block_allsize_list=$(lsblk | grep -v "loop"| grep ':0' | awk '{print $4}' | awk -F'G' '{print $1}')
    block_usedsize_list=$(lsblk | grep -v -e ':0' -e 'NAME' | awk '{print $4}' | awk -F'G' '{print $1}')

    #calculate size about block multi-size and multi-size used information
    for simple_block_size in $block_allsize_list
        do
	block_size_all=$(echo -e "scale=2;$block_size_all+$simple_block_size" | bc)	
        done 
    for simple_usedblock_size in $block_usedsize_list
        do
	block_usedsize_all=$(echo -e "scale=2;$block_usedsize_all+$simple_usedblock_size" | bc)
        done

    block_used_rate=$(printf "%.2f" `echo "scale=2;$block_usedsize_all/$block_size_all" | bc`)

#:<< !
    echo -e "磁盘总空间:\t\t"$block_size_all" G"
    echo -e "磁盘使用空间:\t\t"$block_usedsize_all" G"
    echo -e "磁盘使用率:\t\t"$block_used_rate" %"
#!
}

#get network informations 
function get_network_info(){
    local_ip_all=$(ifconfig | grep -w inet | awk '{print $2}')
    curl -I --connect-timeout 1 -m 1 www.baidu.com &> /dev/null
    if [ $? -eq 0 ];then
        echo -e "能否访问外网:\t\tyes"
    else
        echo -e "能否访问外网:\t\tno"
    fi
    echo "本机所有ip如下:"
    for ip in $local_ip_all
    do
	echo "               "$ip
    done
} 

#get cpu informations
function get_cpu_info(){
    cpu_name=$(cat /proc/cpuinfo | grep "model name" | awk -F': ' 'NR==1{print $2}')
    cpu_num=$(cat /proc/cpuinfo | grep "physical id" |wc -l)
    cpu_cores=$(cat /proc/cpuinfo | grep "cpu cores" |wc -l)
    let per_cpu_cores=cpu_cores/cpu_num
    cpu_processors=$(cat /proc/cpuinfo | grep "processor" | wc -l)
    let per_core_logic=cpu_processors/cpu_cores
    echo -e "cpu处理器型号:\t\t$cpu_name"
    echo -e "cpu处理器个数:\t\t$cpu_num"
    echo -e "单cpu核心数:\t\t$per_cpu_cores"
    echo -e "单cpu划分逻辑处理器数:\t$per_core_logic"
}

#difine main function
function main(){
    echo -e "\033[36m############ network information ##############\033[0m"
    get_network_info
    echo -e "\033[36m############ memory information ###############\033[0m"
    get_mem_info
    echo -e "\033[36m########## swap space information #############\033[0m"
    get_swap_info
    echo -e "\033[36m########## file system information ############\033[0m"
    get_file_system_info
    echo -e "\033[36m############# block information ###############\033[0m"
    get_block_info
    echo -e "\033[36m############## cpu information ################\033[0m"
    get_cpu_info
}

main
