@echo off
set WINPYDIR=%~dp0\WPy64-38100\python-3.8.10.amd64
set "PATH=%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%PATH%;"

set logging=True
rem 日志

set PYTHON=%~dp0\py310\\python.exe
rem python程序位置，不使用懒人包可留空

set glm_path=model\chatglm-6b
rem glm模型位置

set glm_lora_path=
rem glm模型微调权重目录路径  为空则不加载LoRA

set zsk_type=x
rem  知识库类型:s->传统索引；x->基于Sentence  Transformer 的向量数据库

set rwkv_path=model\RWKV-4-Raven-7B-v7-ChnEng-20230404-ctx2048.pth
rem rwkv模型位置

set "rwkv_strategy=fp16"
rem rwkv模型参数

set rwkv_lora_path=""
rem rwkv模型lora微调权重目录路径  为空则不加载LoRA

set rwkv_lora_alpha="16"
rem rwkv模型lora微调权重alpha  和训练时所用值挂钩

set llm_type=glm6b
rem  LLM模型类型:glm6b、rwkv

set zsk_type=s
rem  知识库类型:s->传统索引；x->基于Sentence  Transformer 的向量数据库

set embeddings_path=model\simcse-chinese-roberta-wwm-ext
rem embeddings模型位置

set vectorstore_path=xw
rem vectorstore保存位置

set chunk_size=200
rem chunk_size

set chunk_count=3
rem chunk_count