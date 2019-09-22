#!/bin/bash
mem_total_kB=$(cat /proc/meminfo | grep 'MemTotal' | awk '{print $2}')
mem_free_kB=$(cat /proc/meminfo | grep 'MemFree' | awk '{print $2}')
mem_total_GB=$(printf "%.2f" `echo "scale=2;$mem_total_kB/1024/1024" | bc` )
mem_free_GB=$(printf "%.2f" `echo "scale=2;$mem_free_kB/1024/1024" | bc`) 
mem_used_rate=$(printf "%.2f" `echo "scale=2;($mem_total_kB-$mem_free_kB)/$mem_total_kB" | bc`)%
echo "内存大小共计: "$mem_total_GB"GB"
echo "空闲内存共计: "$mem_free_GB"GB"
echo "内存使用率为: "$mem_used_rate
