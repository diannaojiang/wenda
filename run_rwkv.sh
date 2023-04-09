# /bin/bash
source setting.sh
if [ -z "$PYTHON" ]; then
    CUDA_VISIBLE_DEVICES=0 python rwkvAPI.py
else
    CUDA_VISIBLE_DEVICES=0 $PYTHON rwkvAPI.py
fi
