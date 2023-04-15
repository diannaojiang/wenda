#!/bin/bash
PYTHON="/mnt/data/anaconda3/envs/ChatCBM/bin/python"
# python程序位置，可搭配一键包或是省去每次切换环境

while true
do
    if [ -z "$PYTHON" ]; then
        CUDA_VISIBLE_DEVICES=1 python wenda.py -t glm6b -p 17861
    else
        CUDA_VISIBLE_DEVICES=1 $PYTHON wenda.py -t glm6b -p 17861
    fi
sleep 1
done
