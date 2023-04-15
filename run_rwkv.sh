#!/bin/bash
PYTHON="/mnt/data/anaconda3/envs/ChatCBM/bin/python"
# python程序位置，可搭配一键包或是省去每次切换环境

while true
do
    if [ -z "$PYTHON" ]; then
        CUDA_VISIBLE_DEVICES=0 RWKV_CUDA_ON=0 python wenda.py -t rwkv
    else
        CUDA_VISIBLE_DEVICES=0 RWKV_CUDA_ON=0 $PYTHON wenda.py -t rwkv
    fi
sleep 1
done
