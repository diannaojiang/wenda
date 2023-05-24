from plugins .common import settings #line:1:from plugins.common import settings
import re #line:2:import re
if settings .llm .strategy .startswith ("Q"):#line:4:if settings.llm.strategy.startswith("Q"):
    runtime ="cpp"#line:5:runtime = "cpp"
    from typing import Optional #line:7:from typing import Optional
    import torch #line:8:import torch
    import tokenizers #line:9:import tokenizers
    from llms .rwkvcpp .sampling import sample_logits #line:10:from llms.rwkvcpp.sampling import sample_logits
    logits :Optional [torch .Tensor ]=None #line:11:logits: Optional[torch.Tensor] = None
    state :Optional [torch .Tensor ]=None #line:12:state: Optional[torch.Tensor] = None
    END_OF_LINE_TOKEN :int =187 #line:14:END_OF_LINE_TOKEN: int = 187
    def process_tokens (_OOO0O0OO0O0O00000 :list [int ],O000O0OOOOOOO00OO :float =0.0 )->None :#line:16:def process_tokens(_tokens: list[int], new_line_logit_bias: float = 0.0) -> None:
        global logits ,state #line:17:global logits, state
        for _OO000O0O000000OOO in _OOO0O0OO0O0O00000 :#line:19:for _token in _tokens:
            logits ,state =model .eval (_OO000O0O000000OOO ,state ,state ,logits )#line:20:logits, state = model.eval(_token, state, state, logits)
        logits [END_OF_LINE_TOKEN ]+=O000O0OOOOOOO00OO #line:22:logits[END_OF_LINE_TOKEN] += new_line_logit_bias
    def chat_init (OOOOOO0OOO000OOOO ):#line:24:def chat_init(history):
        global state ,logits #line:25:global state,logits
        if settings .llm .historymode !='string':#line:26:if settings.llm.historymode!='string':
            if OOOOOO0OOO000OOOO is not None and len (OOOOOO0OOO000OOOO )>0 :#line:27:if history is not None and len(history) > 0:
                pass #line:28:pass
            else :#line:29:else:
                state =None #line:30:state = None
                logits =None #line:31:logits = None
        else :#line:32:else:
            O0OO00O00OOOO0000 =[]#line:33:tmp = []
            for OOOO00OOOO0OO00O0 ,OOO00000O00OO0OO0 in enumerate (OOOOOO0OOO000OOOO ):#line:35:for i, old_chat in enumerate(history):
                if OOO00000O00OO0OO0 ['role']=="user":#line:36:if old_chat['role'] == "user":
                    O0OO00O00OOOO0000 .append (f"{user}{interface} "+OOO00000O00OO0OO0 ['content'])#line:37:tmp.append(f"{user}{interface} "+old_chat['content'])
                elif OOO00000O00OO0OO0 ['role']=="AI":#line:38:elif old_chat['role'] == "AI":
                    O0OO00O00OOOO0000 .append (f"{bot}{interface} "+OOO00000O00OO0OO0 ['content'])#line:39:tmp.append(f"{bot}{interface} "+old_chat['content'])
                else :#line:40:else:
                    continue #line:41:continue
            OOOOOO0OOO000OOOO ='\n\n'.join (O0OO00O00OOOO0000 )#line:42:history='\n\n'.join(tmp)
            state =None #line:43:state = None
            logits =None #line:44:logits = None
            return OOOOOO0OOO000OOOO #line:45:return history
    def chat_one (OO0O0O0OO00O0O0O0 ,O0000OOOOO0000000 ,O00000OO0O00O000O ,O00000OO0O0O0OOOO ,OO0O0OOO0OO0OO000 ,OO00O0O0O00000OO0 =False ):#line:48:def chat_one(prompt, history, max_length, top_p, temperature, zhishiku=False):
        global state ,resultChat ,token_stop ,logits #line:49:global state,resultChat,token_stop,logits
        OO0OO00OO0OOO00OO =O00000OO0O00O000O #line:50:token_count = max_length
        OO0O00O0OO0O0O00O =0.2 #line:51:presencePenalty = 0.2
        O0000O0O000OO00O0 =0.2 #line:52:countPenalty = 0.2
        token_stop =[0 ]#line:53:token_stop=[0]
        resultChat =""#line:55:resultChat = ""
        if OO00O0O0O00000OO0 :#line:57:if zhishiku:
            OO0000O00O00OOOOO ="\n\n"+OO0O0O0OO00O0O0O0 .replace ('system:','Bob:').replace ('\n\n',"\n")+f"\n\n{bot}{interface}"#line:60:.replace('\n\n',"\n")+f"\n\n{bot}{interface}"
            OO0000O00O00OOOOO =re .sub ('网页','',OO0000O00O00OOOOO )#line:61:ctx = re.sub('网页', '', ctx)
            OO0000O00O00OOOOO =re .sub ('原标题：','',OO0000O00O00OOOOO )#line:62:ctx = re.sub('原标题：', '', ctx)
        else :#line:63:else:
            if OO0O0O0OO00O0O0O0 .startswith ("raw!"):#line:64:if prompt.startswith("raw!"):
                print ("RWKV raw mode!")#line:65:print("RWKV raw mode!")
                OO0000O00O00OOOOO =OO0O0O0OO00O0O0O0 .replace ("raw!","")#line:66:ctx=prompt.replace("raw!","")
            else :#line:67:else:
                OO0000O00O00OOOOO =f"\n\n{user}{interface} {OO0O0O0OO00O0O0O0}\n\n{bot}{interface}"#line:68:ctx = f"\n\n{user}{interface} {prompt}\n\n{bot}{interface}"
        if settings .llm .historymode =='string':#line:69:if settings.llm.historymode=='string':
            OO0000O00O00OOOOO =O0000OOOOO0000000 +OO0000O00O00OOOOO #line:70:ctx=history+ctx
        yield str (len (OO0000O00O00OOOOO ))+'字正在计算'#line:71:yield str(len(ctx))+'字正在计算'
        O0O0O000O00O0OO00 =OO0000O00O00OOOOO .strip ()#line:72:new = ctx.strip()
        print (f'{O0O0O000O00O0OO00}',end ='')#line:73:print(f'{new}', end='')
        process_tokens (tokenizer .encode (O0O0O000O00O0OO00 ).ids ,new_line_logit_bias =-999999999 )#line:75:process_tokens(tokenizer.encode(new).ids, new_line_logit_bias=-999999999)
        O0O0O0OOO0000OOO0 :list [int ]=[]#line:77:accumulated_tokens: list[int] = []
        OOO0OO00O0OO00O0O :dict [int ,int ]={}#line:78:token_counts: dict[int, int] = {}
        for O000OOO0O00OOOO0O in range (int (OO0OO00OO0OOO00OO )):#line:80:for i in range(int(token_count)):
            for O0O000000O000OOOO in OOO0OO00O0OO00O0O :#line:81:for n in token_counts:
                logits [O0O000000O000OOOO ]-=OO0O00O0OO0O0O00O +OOO0OO00O0OO00O0O [O0O000000O000OOOO ]*O0000O0O000OO00O0 #line:82:logits[n] -= presencePenalty + token_counts[n] * countPenalty
            O00000O0O00OO00OO :int =sample_logits (logits ,OO0O0OOO0OO0OO000 ,O00000OO0O0O0OOOO )#line:84:token: int = sample_logits(logits, temperature, top_p)
            if O00000O0O00OO00OO in token_stop :#line:86:if token in token_stop:
                break #line:87:break
            if O00000O0O00OO00OO not in OOO0OO00O0OO00O0O :#line:89:if token not in token_counts:
                OOO0OO00O0OO00O0O [O00000O0O00OO00OO ]=1 #line:90:token_counts[token] = 1
            else :#line:91:else:
                OOO0OO00O0OO00O0O [O00000O0O00OO00OO ]+=1 #line:92:token_counts[token] += 1
            process_tokens ([O00000O0O00OO00OO ])#line:94:process_tokens([token])
            O0O0O0OOO0000OOO0 +=[O00000O0O00OO00OO ]#line:97:accumulated_tokens += [token]
            OOOO0O0O0O00O00O0 :str =tokenizer .decode (O0O0O0OOO0000OOO0 )#line:99:decoded: str = tokenizer.decode(accumulated_tokens)
            if '\uFFFD'not in OOOO0O0O0O00O00O0 :#line:101:if '\uFFFD' not in decoded:
                resultChat =resultChat +OOOO0O0O0O00O00O0 #line:102:resultChat = resultChat + decoded
                if resultChat .endswith ('\n\n')or resultChat .endswith (f"{user}{interface}")or resultChat .endswith (f"{bot}{interface}"):#line:103:if resultChat.endswith('\n\n') or resultChat.endswith(f"{user}{interface}") or resultChat.endswith(f"{bot}{interface}"):
                    resultChat =remove_suffix (remove_suffix (remove_suffix (remove_suffix (resultChat ,f"{user}{interface}"),f"{bot}{interface}"),'\n'),'\n')#line:110:'\n')
                    yield resultChat #line:111:yield resultChat
                    break #line:112:break
                yield resultChat #line:113:yield resultChat
                O0O0O0OOO0000OOO0 =[]#line:114:accumulated_tokens = []
    def remove_suffix (O0O00O0O0O0OO000O ,OO00O0000OOO0O0O0 ):#line:117:def remove_suffix(input_string, suffix):  # 兼容python3.8
        if OO00O0000OOO0O0O0 and O0O00O0O0O0OO000O .endswith (OO00O0000OOO0O0O0 ):#line:118:if suffix and input_string.endswith(suffix):
            return O0O00O0O0O0OO000O [:-len (OO00O0000OOO0O0O0 )]#line:119:return input_string[:-len(suffix)]
        return O0O00O0O0O0OO000O #line:120:return input_string
    interface =":"#line:123:interface = ":"
    user ="Bob"#line:124:user = "Bob"
    bot ="Alice"#line:125:bot = "Alice"
    model =None #line:126:model = None
    state =None #line:127:state = None
    tokenizer =None #line:128:tokenizer = None
    def load_model ():#line:130:def load_model():
        global model ,tokenizer #line:131:global model,tokenizer
        from llms .rwkvcpp .rwkv_cpp_shared_library import load_rwkv_shared_library #line:133:from llms.rwkvcpp.rwkv_cpp_shared_library import load_rwkv_shared_library
        O0OO0OO00O0OO0O00 =load_rwkv_shared_library ()#line:134:library = load_rwkv_shared_library()
        print (f'System info: {O0OO0OO00O0OO0O00.rwkv_get_system_info_string()}')#line:135:print(f'System info: {library.rwkv_get_system_info_string()}')
        print ('Loading RWKV model')#line:136:print('Loading RWKV model')
        from llms .rwkvcpp .rwkv_cpp_model import RWKVModel #line:137:from llms.rwkvcpp.rwkv_cpp_model import RWKVModel
        try :#line:138:try:
            O00OOO00O00000OOO =int (settings .llm .strategy .split ('->')[1 ])#line:139:cpu_count = int(settings.llm.strategy.split('->')[1])
            model =RWKVModel (O0OO0OO00O0OO0O00 ,settings .llm .path ,O00OOO00O00000OOO )#line:140:model = RWKVModel(library, settings.llm.path,cpu_count)
        except :#line:141:except:
            model =RWKVModel (O0OO0OO00O0OO0O00 ,settings .llm .path )#line:142:model = RWKVModel(library, settings.llm.path)
        print ('Loading 20B tokenizer')#line:143:print('Loading 20B tokenizer')
        tokenizer =tokenizers .Tokenizer .from_file (str ('20B_tokenizer.json'))#line:144:tokenizer = tokenizers.Tokenizer.from_file(str('20B_tokenizer.json'))
else :#line:147:else:
    runtime ="torch"#line:148:runtime = "torch"
    def chat_init (O00OO0OOOO0OOOOO0 ):#line:150:def chat_init(history):
        global state #line:151:global state
        if settings .llm .historymode !='string':#line:152:if settings.llm.historymode!='string':
            if O00OO0OOOO0OOOOO0 is not None and len (O00OO0OOOO0OOOOO0 )>0 :#line:153:if history is not None and len(history) > 0:
                pass #line:154:pass
            else :#line:155:else:
                state =None #line:156:state = None
        else :#line:157:else:
            OOO0OO0O00OOOOOOO =[]#line:158:tmp = []
            for O00OOO00O000O0O0O ,O00OOO00OOO0OOO0O in enumerate (O00OO0OOOO0OOOOO0 ):#line:160:for i, old_chat in enumerate(history):
                if O00OOO00OOO0OOO0O ['role']=="user":#line:161:if old_chat['role'] == "user":
                    OOO0OO0O00OOOOOOO .append (f"{user}{interface} "+O00OOO00OOO0OOO0O ['content'])#line:162:tmp.append(f"{user}{interface} "+old_chat['content'])
                elif O00OOO00OOO0OOO0O ['role']=="AI":#line:163:elif old_chat['role'] == "AI":
                    OOO0OO0O00OOOOOOO .append (f"{bot}{interface} "+O00OOO00OOO0OOO0O ['content'])#line:164:tmp.append(f"{bot}{interface} "+old_chat['content'])
                else :#line:165:else:
                    continue #line:166:continue
            O00OO0OOOO0OOOOO0 ='\n\n'.join (OOO0OO0O00OOOOOOO )#line:167:history='\n\n'.join(tmp)
            state =None #line:168:state = None
            return O00OO0OOOO0OOOOO0 #line:169:return history
    def chat_one (OO000OO00OOOOO00O ,O000O0O0O00O0O0O0 ,OO000000O00O0O0O0 ,OO0OOOO0OO0OO0OO0 ,OOO000O00O00OOOO0 ,O0OOOOO00000OOOO0 =False ):#line:172:def chat_one(prompt, history, max_length, top_p, temperature, zhishiku=False):
        global state #line:173:global state
        OOO0O0000O0O0OOOO =OO000000O00O0O0O0 #line:174:token_count = max_length
        OOO00OO0OOO0OO000 =0.2 #line:175:presencePenalty = 0.2
        OO000O0O0O0OO00O0 =0.2 #line:176:countPenalty = 0.2
        OOO00OO0O00O0O000 =PIPELINE_ARGS (temperature =max (0.2 ,float (OOO000O00O00OOOO0 )),top_p =float (OO0OOOO0OO0OO0OO0 ),alpha_frequency =OO000O0O0O0OO00O0 ,alpha_presence =OOO00OO0OOO0OO000 ,token_ban =[],token_stop =[0 ])#line:181:token_stop=[0])  # stop generation whenever you see any token here
        if O0OOOOO00000OOOO0 :#line:183:if zhishiku:
            O00OOO0OO00O0000O ="\n\n"+OO000OO00OOOOO00O .replace ('system:','Bob:').replace ('\n\n',"\n")+f"\n\n{bot}{interface}"#line:186:.replace('\n\n',"\n")+f"\n\n{bot}{interface}"
            O00OOO0OO00O0000O =re .sub ('网页','',O00OOO0OO00O0000O )#line:187:ctx = re.sub('网页', '', ctx)
            O00OOO0OO00O0000O =re .sub ('原标题：','',O00OOO0OO00O0000O )#line:188:ctx = re.sub('原标题：', '', ctx)
        else :#line:189:else:
            if OO000OO00OOOOO00O .startswith ("raw!"):#line:190:if prompt.startswith("raw!"):
                print ("RWKV raw mode!")#line:191:print("RWKV raw mode!")
                O00OOO0OO00O0000O =OO000OO00OOOOO00O .replace ("raw!","")#line:192:ctx=prompt.replace("raw!","")
            else :#line:193:else:
                O00OOO0OO00O0000O =f"\n\n{user}{interface} {OO000OO00OOOOO00O}\n\n{bot}{interface}"#line:194:ctx = f"\n\n{user}{interface} {prompt}\n\n{bot}{interface}"
        if settings .llm .historymode =='string':#line:195:if settings.llm.historymode=='string':
            O00OOO0OO00O0000O =O000O0O0O00O0O0O0 +O00OOO0OO00O0000O #line:196:ctx=history+ctx
        yield str (len (O00OOO0OO00O0000O ))+'字正在计算'#line:198:yield str(len(ctx))+'字正在计算'
        OO0O0O000O0O00OOO =[]#line:199:all_tokens = []
        O00OO0OO000OO00O0 =0 #line:200:out_last = 0
        OO0O0O0OOOOO000O0 =''#line:201:response = ''
        OOOOO00O0OOOOOO00 ={}#line:202:occurrence = {}
        for OO0O0OO0O0OOOOO0O in range (int (OOO0O0000O0O0OOOO )):#line:203:for i in range(int(token_count)):
            O0OOOO000OOO0OO00 ,state =model .forward (pipeline .encode (O00OOO0OO00O0000O )if OO0O0OO0O0OOOOO0O ==0 else [OOO0O000O0OOOO0O0 ],state )#line:205:ctx) if i == 0 else [token], state)
            for O0000OOO000O0O000 in OOO00OO0O00O0O000 .token_ban :#line:206:for n in args.token_ban:
                O0OOOO000OOO0OO00 [O0000OOO000O0O000 ]=-float ('inf')#line:207:out[n] = -float('inf')
            for O0000OOO000O0O000 in OOOOO00O0OOOOOO00 :#line:208:for n in occurrence:
                O0OOOO000OOO0OO00 [O0000OOO000O0O000 ]-=(OOO00OO0O00O0O000 .alpha_presence +OOOOO00O0OOOOOO00 [O0000OOO000O0O000 ]*OOO00OO0O00O0O000 .alpha_frequency )#line:210:* args.alpha_frequency)
            OOO0O000O0OOOO0O0 =pipeline .sample_logits (O0OOOO000OOO0OO00 ,temperature =OOO00OO0O00O0O000 .temperature ,top_p =OOO00OO0O00O0O000 .top_p )#line:213:out, temperature=args.temperature, top_p=args.top_p)
            if OOO0O000O0OOOO0O0 in OOO00OO0O00O0O000 .token_stop :#line:214:if token in args.token_stop:
                break #line:215:break
            OO0O0O000O0O00OOO +=[OOO0O000O0OOOO0O0 ]#line:216:all_tokens += [token]
            if OOO0O000O0OOOO0O0 not in OOOOO00O0OOOOOO00 :#line:217:if token not in occurrence:
                OOOOO00O0OOOOOO00 [OOO0O000O0OOOO0O0 ]=1 #line:218:occurrence[token] = 1
            else :#line:219:else:
                OOOOO00O0OOOOOO00 [OOO0O000O0OOOO0O0 ]+=1 #line:220:occurrence[token] += 1
            O0000O00000O00000 =pipeline .decode (OO0O0O000O0O00OOO [O00OO0OO000OO00O0 :])#line:222:tmp = pipeline.decode(all_tokens[out_last:])
            if '\ufffd'not in O0000O00000O00000 :#line:223:if '\ufffd' not in tmp:
                OO0O0O0OOOOO000O0 +=O0000O00000O00000 #line:224:response += tmp
                if OO0O0O0OOOOO000O0 .endswith ('\n\n')or OO0O0O0OOOOO000O0 .endswith (f"{user}{interface}")or OO0O0O0OOOOO000O0 .endswith (f"{bot}{interface}"):#line:225:if response.endswith('\n\n') or response.endswith(f"{user}{interface}") or response.endswith(f"{bot}{interface}"):
                    OO0O0O0OOOOO000O0 =remove_suffix (remove_suffix (remove_suffix (remove_suffix (OO0O0O0OOOOO000O0 ,f"{user}{interface}"),f"{bot}{interface}"),'\n'),'\n')#line:232:'\n')
                    break #line:233:break
                O00OO0OO000OO00O0 =OO0O0OO0O0OOOOO0O +1 #line:235:out_last = i + 1
                yield OO0O0O0OOOOO000O0 .strip ()#line:236:yield response.strip()
    def remove_suffix (OOO0OO0O00O00OO00 ,OO0OO0O0OO0O0O0O0 ):#line:239:def remove_suffix(input_string, suffix):  # 兼容python3.8
        if OO0OO0O0OO0O0O0O0 and OOO0OO0O00O00OO00 .endswith (OO0OO0O0OO0O0O0O0 ):#line:240:if suffix and input_string.endswith(suffix):
            return OOO0OO0O00O00OO00 [:-len (OO0OO0O0OO0O0O0O0 )]#line:241:return input_string[:-len(suffix)]
        return OOO0OO0O00O00OO00 #line:242:return input_string
    interface =":"#line:245:interface = ":"
    user ="Bob"#line:246:user = "Bob"
    bot ="Alice"#line:247:bot = "Alice"
    pipeline =None #line:248:pipeline = None
    PIPELINE_ARGS =None #line:249:PIPELINE_ARGS = None
    model =None #line:250:model = None
    state =None #line:251:state = None
    def load_model ():#line:254:def load_model():
        global pipeline ,PIPELINE_ARGS ,model #line:255:global pipeline, PIPELINE_ARGS, model
        import os #line:256:import os
        os .environ ['RWKV_JIT_ON']='1'#line:257:os.environ['RWKV_JIT_ON'] = '1'
        if (os .environ .get ('RWKV_CUDA_ON')==''or os .environ .get ('RWKV_CUDA_ON')==None ):#line:258:if (os.environ.get('RWKV_CUDA_ON') == '' or os.environ.get('RWKV_CUDA_ON') == None):
            os .environ ["RWKV_CUDA_ON"]='0'#line:259:os.environ["RWKV_CUDA_ON"] = '0'
        from rwkv .model import RWKV #line:262:from rwkv.model import RWKV  # pip install rwkv
        import uuid #line:264:import uuid
        import base64 #line:265:import base64
        OOOOOOOO00OO0OOOO =uuid .UUID (int =uuid .getnode ()).hex [-12 :]#line:267:mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        print ("device mac:",OOOOOOOO00OO0OOOO )#line:268:print("device mac:",mac)
        O0O000O00OO0000O0 =base64 .urlsafe_b64encode (('cssailab2023shuizhenz'+OOOOOOOO00OO0OOOO [:-1 ]).encode ())#line:269:key = base64.urlsafe_b64encode(('cssailab2023shuizhenz'+mac[:-1]).encode())
        print ("device key:",O0O000O00OO0000O0 )#line:270:print("device key:",key)
        model =RWKV (model =settings .llm .path ,strategy =settings .llm .strategy ,key =O0O000O00OO0000O0 )#line:273:model = RWKV(model=settings.llm.path, strategy=settings.llm.strategy, key=key)
        from rwkv .utils import PIPELINE ,PIPELINE_ARGS #line:278:from rwkv.utils import PIPELINE, PIPELINE_ARGS
        pipeline =PIPELINE (model ,"20B_tokenizer.json")#line:279:pipeline = PIPELINE(model, "20B_tokenizer.json")
