from plugins .common import settings #line:1
import re #line:2
if settings .llm .strategy .startswith ("Q"):#line:4
    runtime ="cpp"#line:5
    from typing import Optional #line:7
    import torch #line:8
    import tokenizers #line:9
    from llms .rwkvcpp .sampling import sample_logits #line:10
    logits :Optional [torch .Tensor ]=None #line:11
    state :Optional [torch .Tensor ]=None #line:12
    END_OF_LINE_TOKEN :int =187 #line:14
    def process_tokens (_O0O000O0O0O000O0O :list [int ],new_line_logit_bias :float =0.0 )->None :#line:16
        global logits ,state #line:17
        for _OO00000O0OO00O000 in _O0O000O0O0O000O0O :#line:19
            logits ,state =model .eval (_OO00000O0OO00O000 ,state ,state ,logits )#line:20
        logits [END_OF_LINE_TOKEN ]+=new_line_logit_bias #line:22
    def chat_init (OOO00000O0O0OOOOO ):#line:24
        global state ,logits #line:25
        if settings .llm .historymode !='string':#line:26
            if OOO00000O0O0OOOOO is not None and len (OOO00000O0O0OOOOO )>0 :#line:27
                pass #line:28
            else :#line:29
                state =None #line:30
                logits =None #line:31
        else :#line:32
            OO0O000OOOO0O0O00 =[]#line:33
            for O000O0OO0OO0O0OO0 ,O0O0O0O00O00OOOO0 in enumerate (OOO00000O0O0OOOOO ):#line:35
                if O0O0O0O00O00OOOO0 ['role']=="user":#line:36
                    OO0O000OOOO0O0O00 .append (f"{user}{interface} "+O0O0O0O00O00OOOO0 ['content'])#line:37
                elif O0O0O0O00O00OOOO0 ['role']=="AI":#line:38
                    OO0O000OOOO0O0O00 .append (f"{bot}{interface} "+O0O0O0O00O00OOOO0 ['content'])#line:39
                else :#line:40
                    continue #line:41
            OOO00000O0O0OOOOO ='\n\n'.join (OO0O000OOOO0O0O00 )#line:42
            state =None #line:43
            logits =None #line:44
            return OOO00000O0O0OOOOO #line:45
    def chat_one (O0O0OO0OOOO0000OO ,O0O0OOOO0O00OOO0O ,O0O0OO0OO00OO0OO0 ,O0O0O0OOO0OO0OO0O ,OO00OO000OO00O000 ,zhishiku =False ):#line:48
        global state ,resultChat ,token_stop ,logits #line:49
        O00OOOOOOO00O0000 =O0O0OO0OO00OO0OO0 #line:50
        O0OO00OO00O0O0O0O =0.2 #line:51
        O0O00O0OO0O0O000O =0.2 #line:52
        token_stop =[0 ]#line:53
        resultChat =""#line:55
        if zhishiku :#line:57
            O00O00OOO00OOO000 ="\n\n"+O0O0OO0OOOO0000OO .replace ('system:','Bob:').replace ('\n\n',"\n")+f"\n\n{bot}{interface}"#line:60
            O00O00OOO00OOO000 =re .sub ('网页','',O00O00OOO00OOO000 )#line:61
            O00O00OOO00OOO000 =re .sub ('原标题：','',O00O00OOO00OOO000 )#line:62
        else :#line:63
            if O0O0OO0OOOO0000OO .startswith ("raw!"):#line:64
                print ("RWKV raw mode!")#line:65
                O00O00OOO00OOO000 =O0O0OO0OOOO0000OO .replace ("raw!","")#line:66
            else :#line:67
                O00O00OOO00OOO000 =f"\n\n{user}{interface} {O0O0OO0OOOO0000OO}\n\n{bot}{interface}"#line:68
        if settings .llm .historymode =='string':#line:69
            O00O00OOO00OOO000 =O0O0OOOO0O00OOO0O +O00O00OOO00OOO000 #line:70
        yield str (len (O00O00OOO00OOO000 ))+'字正在计算'#line:71
        OOO00OOO00OO0OO00 =O00O00OOO00OOO000 .strip ()#line:72
        print (f'{OOO00OOO00OO0OO00}',end ='')#line:73
        process_tokens (tokenizer .encode (OOO00OOO00OO0OO00 ).ids ,new_line_logit_bias =-999999999 )#line:75
        OO0O00OOO0OOO000O :list [int ]=[]#line:77
        OOO000O00O0O00O0O :dict [int ,int ]={}#line:78
        for OO000O000O00O000O in range (int (O00OOOOOOO00O0000 )):#line:80
            for OOOO0OO0O0OO00OOO in OOO000O00O0O00O0O :#line:81
                logits [OOOO0OO0O0OO00OOO ]-=O0OO00OO00O0O0O0O +OOO000O00O0O00O0O [OOOO0OO0O0OO00OOO ]*O0O00O0OO0O0O000O #line:82
            O00OOOOOO00O0OO00 :int =sample_logits (logits ,OO00OO000OO00O000 ,O0O0O0OOO0OO0OO0O )#line:84
            if O00OOOOOO00O0OO00 in token_stop :#line:86
                break #line:87
            if O00OOOOOO00O0OO00 not in OOO000O00O0O00O0O :#line:89
                OOO000O00O0O00O0O [O00OOOOOO00O0OO00 ]=1 #line:90
            else :#line:91
                OOO000O00O0O00O0O [O00OOOOOO00O0OO00 ]+=1 #line:92
            process_tokens ([O00OOOOOO00O0OO00 ])#line:94
            OO0O00OOO0OOO000O +=[O00OOOOOO00O0OO00 ]#line:97
            O000O0O0000000OO0 :str =tokenizer .decode (OO0O00OOO0OOO000O )#line:99
            if '\uFFFD'not in O000O0O0000000OO0 :#line:101
                resultChat =resultChat +O000O0O0000000OO0 #line:102
                if resultChat .endswith ('\n\n')or resultChat .endswith (f"{user}{interface}")or resultChat .endswith (f"{bot}{interface}"):#line:103
                    resultChat =remove_suffix (remove_suffix (remove_suffix (remove_suffix (resultChat ,f"{user}{interface}"),f"{bot}{interface}"),'\n'),'\n')#line:110
                    yield resultChat #line:111
                    break #line:112
                yield resultChat #line:113
                OO0O00OOO0OOO000O =[]#line:114
    def remove_suffix (OOOO0O000OOOOOO0O ,OOO00O0OO0OOOOOO0 ):#line:117
        if OOO00O0OO0OOOOOO0 and OOOO0O000OOOOOO0O .endswith (OOO00O0OO0OOOOOO0 ):#line:118
            return OOOO0O000OOOOOO0O [:-len (OOO00O0OO0OOOOOO0 )]#line:119
        return OOOO0O000OOOOOO0O #line:120
    interface =":"#line:123
    user ="Bob"#line:124
    bot ="Alice"#line:125
    model =None #line:126
    state =None #line:127
    tokenizer =None #line:128
    def load_model ():#line:130
        global model ,tokenizer #line:131
        from llms .rwkvcpp .rwkv_cpp_shared_library import load_rwkv_shared_library #line:133
        O0O0OO0O00O0OO0O0 =load_rwkv_shared_library ()#line:134
        print (f'System info: {O0O0OO0O00O0OO0O0.rwkv_get_system_info_string()}')#line:135
        print ('Loading RWKV model')#line:136
        from llms .rwkvcpp .rwkv_cpp_model import RWKVModel #line:137
        try :#line:138
            OO0OO0O00OOO000O0 =int (settings .llm .strategy .split ('->')[1 ])#line:139
            model =RWKVModel (O0O0OO0O00O0OO0O0 ,settings .llm .path ,OO0OO0O00OOO000O0 )#line:140
        except :#line:141
            model =RWKVModel (O0O0OO0O00O0OO0O0 ,settings .llm .path )#line:142
        print ('Loading 20B tokenizer')#line:143
        tokenizer =tokenizers .Tokenizer .from_file (str ('20B_tokenizer.json'))#line:144
else :#line:147
    runtime ="torch"#line:148
    def chat_init (O000O0O0000OO0OO0 ):#line:150
        global state #line:151
        if settings .llm .historymode !='string':#line:152
            if O000O0O0000OO0OO0 is not None and len (O000O0O0000OO0OO0 )>0 :#line:153
                pass #line:154
            else :#line:155
                state =None #line:156
        else :#line:157
            OOOO0OO0OO0OOO0O0 =[]#line:158
            for OOO0000O0OO0OOOO0 ,O0O0OO000000OO0OO in enumerate (O000O0O0000OO0OO0 ):#line:160
                if O0O0OO000000OO0OO ['role']=="user":#line:161
                    OOOO0OO0OO0OOO0O0 .append (f"{user}{interface} "+O0O0OO000000OO0OO ['content'])#line:162
                elif O0O0OO000000OO0OO ['role']=="AI":#line:163
                    OOOO0OO0OO0OOO0O0 .append (f"{bot}{interface} "+O0O0OO000000OO0OO ['content'])#line:164
                else :#line:165
                    continue #line:166
            O000O0O0000OO0OO0 ='\n\n'.join (OOOO0OO0OO0OOO0O0 )#line:167
            state =None #line:168
            return O000O0O0000OO0OO0 #line:169
    def chat_one (OO0OOO000OO0OO0OO ,O00O0OO00O00OOOO0 ,OO00O000O00O00O00 ,O0O0OOOOOO0O0O00O ,OO0O00O0000O0O00O ,zhishiku =False ):#line:172
        global state #line:173
        O0O0000OO00OO0O0O =OO00O000O00O00O00 #line:174
        OO000000OOOOOOO0O =0.2 #line:175
        OO0000O0O0O0000O0 =0.2 #line:176
        O0000O0OO0O0OOOOO =PIPELINE_ARGS (temperature =max (0.2 ,float (OO0O00O0000O0O00O )),top_p =float (O0O0OOOOOO0O0O00O ),alpha_frequency =OO0000O0O0O0000O0 ,alpha_presence =OO000000OOOOOOO0O ,token_ban =[],token_stop =[0 ])#line:181
        if zhishiku :#line:183
            O00OO0OO0000O0000 ="\n\n"+OO0OOO000OO0OO0OO .replace ('system:','Bob:').replace ('\n\n',"\n")+f"\n\n{bot}{interface}"#line:186
            O00OO0OO0000O0000 =re .sub ('网页','',O00OO0OO0000O0000 )#line:187
            O00OO0OO0000O0000 =re .sub ('原标题：','',O00OO0OO0000O0000 )#line:188
        else :#line:189
            if OO0OOO000OO0OO0OO .startswith ("raw!"):#line:190
                print ("RWKV raw mode!")#line:191
                O00OO0OO0000O0000 =OO0OOO000OO0OO0OO .replace ("raw!","")#line:192
            else :#line:193
                O00OO0OO0000O0000 =f"\n\n{user}{interface} {OO0OOO000OO0OO0OO}\n\n{bot}{interface}"#line:194
        if settings .llm .historymode =='string':#line:195
            O00OO0OO0000O0000 =O00O0OO00O00OOOO0 +O00OO0OO0000O0000 #line:196
        yield str (len (O00OO0OO0000O0000 ))+'字正在计算'#line:198
        OOOOOOO0000000OO0 =[]#line:199
        O00O0000O00000000 =0 #line:200
        O00OOO000000000O0 =''#line:201
        OOO0O0OO0O0OO00OO ={}#line:202
        for OO00O0O0OOOOOOOO0 in range (int (O0O0000OO00OO0O0O )):#line:203
            OOO0OO00OO0O000OO ,state =model .forward (pipeline .encode (O00OO0OO0000O0000 )if OO00O0O0OOOOOOOO0 ==0 else [O00OOO0O00OO0OO0O ],state )#line:205
            for OO0O0OO0000000OOO in O0000O0OO0O0OOOOO .token_ban :#line:206
                OOO0OO00OO0O000OO [OO0O0OO0000000OOO ]=-float ('inf')#line:207
            for OO0O0OO0000000OOO in OOO0O0OO0O0OO00OO :#line:208
                OOO0OO00OO0O000OO [OO0O0OO0000000OOO ]-=(O0000O0OO0O0OOOOO .alpha_presence +OOO0O0OO0O0OO00OO [OO0O0OO0000000OOO ]*O0000O0OO0O0OOOOO .alpha_frequency )#line:210
            O00OOO0O00OO0OO0O =pipeline .sample_logits (OOO0OO00OO0O000OO ,temperature =O0000O0OO0O0OOOOO .temperature ,top_p =O0000O0OO0O0OOOOO .top_p )#line:213
            if O00OOO0O00OO0OO0O in O0000O0OO0O0OOOOO .token_stop :#line:214
                break #line:215
            OOOOOOO0000000OO0 +=[O00OOO0O00OO0OO0O ]#line:216
            if O00OOO0O00OO0OO0O not in OOO0O0OO0O0OO00OO :#line:217
                OOO0O0OO0O0OO00OO [O00OOO0O00OO0OO0O ]=1 #line:218
            else :#line:219
                OOO0O0OO0O0OO00OO [O00OOO0O00OO0OO0O ]+=1 #line:220
            OOOOOOOOO000OOOO0 =pipeline .decode (OOOOOOO0000000OO0 [O00O0000O00000000 :])#line:222
            if '\ufffd'not in OOOOOOOOO000OOOO0 :#line:223
                O00OOO000000000O0 +=OOOOOOOOO000OOOO0 #line:224
                if O00OOO000000000O0 .endswith ('\n\n')or O00OOO000000000O0 .endswith (f"{user}{interface}")or O00OOO000000000O0 .endswith (f"{bot}{interface}"):#line:225
                    O00OOO000000000O0 =remove_suffix (remove_suffix (remove_suffix (remove_suffix (O00OOO000000000O0 ,f"{user}{interface}"),f"{bot}{interface}"),'\n'),'\n')#line:232
                    break #line:233
                O00O0000O00000000 =OO00O0O0OOOOOOOO0 +1 #line:235
                yield O00OOO000000000O0 .strip ()#line:236
    def remove_suffix (O0OO00OO0000OO0OO ,OO00OOOO00O0OOO0O ):#line:239
        if OO00OOOO00O0OOO0O and O0OO00OO0000OO0OO .endswith (OO00OOOO00O0OOO0O ):#line:240
            return O0OO00OO0000OO0OO [:-len (OO00OOOO00O0OOO0O )]#line:241
        return O0OO00OO0000OO0OO #line:242
    interface =":"#line:245
    user ="Bob"#line:246
    bot ="Alice"#line:247
    pipeline =None #line:248
    PIPELINE_ARGS =None #line:249
    model =None #line:250
    state =None #line:251
    def load_model ():#line:254
        global pipeline ,PIPELINE_ARGS ,model #line:255
        import os #line:256
        os .environ ['RWKV_JIT_ON']='1'#line:257
        if (os .environ .get ('RWKV_CUDA_ON')==''or os .environ .get ('RWKV_CUDA_ON')==None ):#line:258
            os .environ ["RWKV_CUDA_ON"]='0'#line:259
        from rwkv .model import RWKV #line:262
        import uuid #line:264
        import base64 #line:265
        OOO00O0O0000000O0 =uuid .UUID (int =uuid .getnode ()).hex [-12 :]#line:267
        print ("device mac:",OOO00O0O0000000O0 )#line:268
        OO00OOO0OOOOOO0O0 =base64 .urlsafe_b64encode (('cssailab2023shuizhenz'+OOO00O0O0000000O0 [:-1 ]).encode ())#line:269
        print ("device key:",OO00OOO0OOOOOO0O0 )#line:270
        try :#line:272
            model =RWKV (model =settings .llm .path ,strategy =settings .llm .strategy ,key =OO00OOO0OOOOOO0O0 )#line:273
        except Exception as OO000000O0OOOOO00 :#line:274
            if str (type (OO000000O0OOOOO00 ))=="<class 'cryptography.fernet.InvalidToken'>":#line:275
                print ("密钥错误，请联系研究院开发人员。")#line:276
            print ('error:',OO000000O0OOOOO00 )#line:277
            exit (0 )#line:278
        from rwkv .utils import PIPELINE ,PIPELINE_ARGS #line:283
        pipeline =PIPELINE (model ,"20B_tokenizer.json")#line:284
