#!/bin/bash
source setting.sh
export llm_type="rwkv"
export PORT="17860"
if [ -z "$PYTHON" ]; then
    CUDA_VISIBLE_DEVICES=0 python wenda.py
else
    CUDA_VISIBLE_DEVICES=0 $PYTHON wenda.py
fi
