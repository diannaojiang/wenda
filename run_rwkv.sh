#!/bin/bash
source setting.sh
export llm_type="rwkv"
export PORT="17860"
while true
do
    if [ -z "$PYTHON" ]; then
        CUDA_VISIBLE_DEVICES=0 RWKV_CUDA_ON=1 python wenda.py
    else
        CUDA_VISIBLE_DEVICES=0 RWKV_CUDA_ON=1 $PYTHON wenda.py
    fi
sleep 1
done
