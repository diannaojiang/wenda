#!/bin/bash
PYTHON="/mnt/data/anaconda3/envs/ChatCBM/bin/python"
# python程序位置，可搭配一键包或是省去每次切换环境

while true
do
    if [ -z "$PYTHON" ]; then
        CUDA_VISIBLE_DEVICES=0 python wenda.py -t glm6b -p 17860
    else
        CUDA_VISIBLE_DEVICES=0 $PYTHON wenda.py -t glm6b -p 17860
    fi
sleep 1
done
