#!/bin/bash

#initialize and globalize variables
mem_total_kB=''
mem_free_kB=''
mem_used_rate=''
swap_total=''
swap_free=''
swap_used_rate=''

#get memory informa
function get_mem_info(){
    mem_total_kB=$(cat /proc/meminfo | grep 'MemTotal' | awk '{print $2}')
    mem_free_kB=$(cat /proc/meminfo | grep 'MemFree' | awk '{print $2}')
    mem_total_GB=$(printf "%.2f" `echo "scale=2;$mem_total_kB/1024/1024" | bc` )
    mem_free_GB=$(printf "%.2f" `echo "scale=2;$mem_free_kB/1024/1024" | bc`) 
    mem_used_rate=$(printf "%.2f" `echo "scale=2;($mem_total_kB-$mem_free_kB)/$mem_total_kB" | bc`)%

    echo "内存大小共计: "$mem_total_GB"GB"
    echo "空闲内存共计: "$mem_free_GB"GB"
    echo "内存使用率为: "$mem_used_rate
}

function get_swap_info(){
    swap_total=$(cat /proc/meminfo | grep -w SwapTotal | awk '{print $2}')
    swap_free=$(cat /proc/meminfo | grep -w SwapFree | awk '{print $2}')

    if [ "$swap_total" -eq 0 ];then
	swap_used_rate=0%
    elif [ "$swap_total" -ne 0 ];then
        swap_used_rate=$(printf "%.2f" `echo "scale=2;($swap_total-$swap_free)/$swap_total" | bc`)%  
    else 
	echo -e "\033[31m GET SWAP INFOMATION ERROR\033[0m"
    fi
:<< !
    echo '交换分区总空间: '$swap_total"kB"
    echo '空闲交换分区空间: '$swap_free"kB"
    echo '交换分区使用率: '$swap_used_rate
!
}

function get_block_info(){
    block_total=$(df | grep -w '/' | awk '{print $2}')
    block_free=$(df | grep -w '/' | awk '{print $4}')
    block_used_rate=$(df | grep -w '/' | awk '{print $5}')
}





function main(){
    get_mem_info
    get_swap_info
}

main
