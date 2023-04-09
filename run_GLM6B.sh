# /bin/bash
source setting.sh
if [ -z "$PYTHON" ]; then
    CUDA_VISIBLE_DEVICES=1 python GLM6BAPI.py
else
    CUDA_VISIBLE_DEVICES=1 $PYTHON GLM6BAPI.py
fi
