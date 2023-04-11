
set "WINPYDIR=%~dp0\WPy64-38100\python-3.8.10.amd64"
set "PATH=%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%PATH%;"

set logging=1
rem ��־

set PORT=17860
rem WebUI Ĭ�������˿ں�

set "PYTHON=%WINPYDIR%\python.exe "
rem python����λ�ã���ʹ�ø�Ϊ����·��

set glm_path=model\chatglm-6b-int4
rem glmģ��λ��


set "glm_strategy=cuda fp16"


rem glm ģ�Ͳ���  ֧�֣�
rem "cpu fp32"  ����glmģ�� Ҫֱ������cpu�϶�����ʹ���������
rem "cpu fp32i8" fp16ԭ��ģ�� Ҫ��������Ϊint8����cpu�Ͽ���ʹ���������
rem "cpu fp32i4" fp16ԭ��ģ��Ҫ ��������Ϊint4����cpu�Ͽ���ʹ���������
rem "cuda fp16"  ����glmģ�� Ҫֱ������gpu�϶�����ʹ���������
rem "cuda fp16i8"  fp16ԭ��ģ�� Ҫ��������Ϊint8����gpu�Ͽ���ʹ���������
rem "cuda fp16i4"  fp16ԭ��ģ�� Ҫ��������Ϊint4����gpu�Ͽ���ʹ���������
    
set glm_lora_path=
rem glmģ��΢��Ȩ��Ŀ¼·��  Ϊ���򲻼���LoRA

set rwkv_path=..\RWKV-4-Raven-7B-v7-ChnEng-20230404-ctx2048.pth
rem rwkvģ��λ��

set "rwkv_strategy=cuda fp16i8 *18+"
rem rwkvģ�Ͳ���

set rwkv_lora_path=""
rem rwkvģ��lora΢��Ȩ��Ŀ¼·��  Ϊ���򲻼���LoRA

set rwkv_lora_alpha="16"
rem rwkvģ��lora΢��Ȩ��alpha  ��ѵ��ʱ����ֵ�ҹ�

set llm_type=glm6b
rem  LLMģ������:glm6b��rwkv

set zsk_type=bingsite
rem  ֪ʶ������:
rem  s����ͳ����
rem  x������Sentence  Transformer ���������ݿ�
rem  bing��cn.bing�����������ڿ���
rem  bingxs��cn.bingѧ�������������ڿ���
rem  bingsite��cn.bingվ�������������ڿ��ã���������ַ��
rem cn.bingվ��������ַ:
rem set site=www.jianbiaoku.com
rem  �����
set site=www.12371.cn
rem  ������Ա��

set zsk_show_soucre=0
rem  ֪ʶ����ʾ��Դ

set zsk_folder=zsk
rem  ֪ʶ����ļ���Ŀ¼���ƣ���������Ϊtxt

set embeddings_path=model\simcse-chinese-roberta-wwm-ext
rem embeddingsģ��λ��

set vectorstore_path=xw
rem vectorstore����λ��

set chunk_size=200
rem chunk_size

set chunk_count=5
rem chunk_count

