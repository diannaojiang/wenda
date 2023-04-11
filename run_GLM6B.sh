#!/bin/bash
source setting.sh
export llm_type="glm6b"
export PORT="17861"
while true
do
    if [ -z "$PYTHON" ]; then
        CUDA_VISIBLE_DEVICES=1 python wenda.py
    else
        CUDA_VISIBLE_DEVICES=1 $PYTHON wenda.py
    fi
sleep 1
done
