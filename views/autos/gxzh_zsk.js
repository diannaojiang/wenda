get_title_form_md = (s) => {
    try {
        return s.match('\\[(.+)\\]')[1]
    } catch {
        return s
    }
}
get_url_form_md = (s) => {
    try {
        return s.match('\\((.+)\\)')[1]
    } catch {
        return s
    }
}
merge_same_title = (s) => {
    let tempMap = new Map()
    let arr = []
    let finalarr = []
    for(let i=0;i<s.length;i++){
        let title = s[i].title
        if(tempMap.has(title)){
            let finalcontent = trim_duplicated_startend(tempMap.get(title), s[i].content)
            tempMap.set(title,finalcontent)
        }else{
            tempMap.set(title,s[i].content)
        }
    }
    //将map转化为数组
    tempMap.forEach((val,key)=>{
        let tmp = new Map()
        tmp.set("title",key)
        tmp.set("url",key)
        tmp.set("content",val)
        arr.push(tmp)
    })
    for(let i=0;i<arr.length;i++){
        let tmp = {};
        tmp.title = arr[i].get("title");
        tmp.url = arr[i].get("url");
        tmp.content = arr[i].get("content")
        finalarr.push(tmp)
    }
    return finalarr;
}

_stringSplitReverse = (s)=>{
    let ls_str1 = []
    let str_tmp = ""
    const arr = s.split('').reverse()
    arr.forEach(c=>{
        str_tmp = c + str_tmp
        ls_str1.push(str_tmp)
    })        
    return ls_str1
}

_stringCutDuplicated = (str1,str2)=>{
    if(str2 && str2.indexOf(str1) === 0){
        return _stringCutDuplicated(str1,str2.slice(str1.length))
    }
    return str2
}

trim_duplicated_startend = (str1, str2, endLoop)=>{
    let ls_str1 = _stringSplitReverse(str1)
    let str2_tmp = str2
    let str1_tmp
    for(let i=0;i<ls_str1.length;i++){
        str1_tmp = ls_str1[i]
        str2_tmp = _stringCutDuplicated(str1_tmp,str2_tmp)
    }
    if(str2_tmp.length < str2.length){
        return str1 + str2_tmp
    }else if(endLoop){
        return str2_tmp + str1
    }else{
        return trim_duplicated_startend(str2, str1, true)
    }
}

window.answer_with_kgst = async (Q) => {
    // lsdh(false)
    
    // app.chat = [{ "role": "user", "content": "从以下语句中抽取出关键词：处级的领导都有哪些？" },
    //             { "role": "AI", "content": "关键词：处级、领导" },
    //             { "role": "user", "content": "从以下语句中抽取出关键词：广东省统计局最近推出了哪些疫情防控的公文？" },
    //             { "role": "AI", "content": "关键词：广东省、统计局、疫情防控、公文" }
    // ]
    // zsk(false)
    // lsdh(true)//打开历史对话
    // add_conversation("user", app.question)
    // add_conversation("user", app.question)
    // add_conversation("user", app.question)
    send_raw("从以下语句中抽取出关键词：" + Q, '', [
        { "role": "user", "content": "从以下语句中抽取出关键词：处级的领导都有哪些？" },
        { "role": "AI", "content": "关键词：处级、领导" },
        { "role": "user", "content": "从以下语句中抽取出关键词：广东省统计局最近推出了哪些疫情防控的公文？" },
        { "role": "AI", "content": "关键词：广东省、统计局、疫情防控、公文" }
    ],onmessage="" )
    resp = (await send("从以下语句中抽取出关键词：" + Q, keyword = app.question, show = false))
    .replace(/\n- /g, '\n1.')//兼容不同格式
    .split("\n")

    // app.chat = []
    
    // app.chat.push({ "role": "user", "content": Q })


    kownladge = (await find_dynamic(resp[0] + '||' + Q, 1,{'libraryStategy':"kgst:10:CSSRegulations",'maxItmes':10})).map(i => ({
        title: get_title_form_md(i.title),
        url: get_url_form_md(i.title),
        content: i.content
    }))
    console.log('kownladge raw:', kownladge)
    if (kownladge.length > 0) {
        answer = {
            role: "AI",
            content: "",
            sources: kownladge
        }
        // app.chat.push(answer)
        // result = []
        // for (let i in kownladge) {
        //     answer.content = '正在查找：' + kownladge[i].title
        //     if (i > 3) continue
        //     let prompt = app.zsk_summarize_prompt + '\n' +
        //         kownladge[i].content + "\n问题：" + Q
        //     result.push(await send(prompt, keyword = Q, show = false))
        // }
        
        //合并title一致的
        kownladge = merge_same_title(kownladge)
        console.log('kownladge merge duplicated:',kownladge)
        // var result = kg_content.split("\n"); // 按照回车符分割字符串，得到一个数组
        // result = result.slice(0, 6); // 取数组的前五个元素，得到一个新的数组
        // kg_content = result.join("\n"); 
        // app.chat.push({ "role": "AI", "content": kg_content })
        let prompt = app.zsk_answer_prompt + '\n' + kownladge.map((e, i) => i + 1 + "." + e.content).join('\n') + "\n问题：" + Q
        // let prompt = "Answer the questions based only on the table below." + '\n' + kg_content + "\nQuestion：" + Q
        // console.log('prompt', prompt)
        return await send(prompt, keyword = Q, show = true, sources = kownladge,
            addition_args = { cfg_factor: app.cfg_factor, cfg_ctx: Q })
    } else {
        app.chat.pop()
        sources = [{
            title: '未匹配到知识库',
            content: '本次对话内容完全由模型提供'
        }]
        return await send(Q, keyword = Q, show = true, sources = sources)
    }
}

app.buttons.push({
    icon: "face-agent",
    click: async () => {

        app.current_func = '知识库'
        add_conversation("AI", "欢迎使用精准客服。\n初次使用，请初始化客服向量库", [{
            title: '初始化意图向量库',
            content: '本功能只需执行一次',
            click: async () => {
                let 你好 = `你好，我是中软知道，由中国软件研究院研发的大模型支撑我的能力。`
                yt2prompt_dict = {
                    "[涉外保密工作管理办法](保密文件，请在内网访问)|好的，以下是《核心涉密人员因公出国(境)备案表》，请查看:\n![Imgur](/ktdA1UZ.png)": ['帮我打开《核心涉密人员因公出国(境)备案表》'],
                    "[外事⼯作管理办法](公司经营班子成员（含赴港澳台地区）申请，需发出正式请示文件，说明出访理由、目的、在外停留时间、费用支出安排等内容，并填写《中国电子信息产业集团有限公司因公出国（境）团组任务审批表》（以下简称《审批表》），并附外方邀请信及在外日程安排等材料，报公司外事管理部门审核。),[涉外保密⼯作管理办法](对核心涉密人员出国（境）要严格审批，任务派出单位要填写《核心涉密人员因公出国（境）备案表》（附件4), 经本单位保密主管部门及主要领导审批同意，报公司保密主管部门审批后，方可履行外事报批手续。涉密人员因公出国（境），应由派出单位对其进行保密审查和保密教育，并出具《涉密人员出国（境）同意派出函》),[保密⼯作实施细则](涉密人员因公出国（境）的，应当按照外事管理权限和程序审批。涉密人员因私出国（境）的，应由本人提出申请，填写《中国软件涉密人员因私出国（境）审批表》（附件3），一般涉密人员应提前30 天提出申请，由中国软件保密委员会审批，重要涉密人员应提前50 天提出申请，由中电集团审批，核心涉密人员因私出国（境）参照国家相关规定执行。)|因公出国需要准备以下⽂件和材料：\n1. 出访任务涉及的有关⽂件，如协议书、合同、其他批件等，需⼀并提交原件或复印件。\n2. 《因公出国(境)团组任务审批表审批表》，团组中含外单位⼈员时请注明其外事归⼝单位的称谓，以便办理《征求意⻅函》、《委托签证函》和《出国任务通知书》。\n3. 《因公临时出国⼈员备案表》或《因公临时赴港澳⼈员备案表》。团组中有涉密⼈员的，需提供涉密⼈员签订的《涉密⼈员因公出国(境)保密义务承诺书》及所在单位为其出具《涉密⼈员因公出国(境)同意派出函》。如团组中有核⼼涉密⼈员的，还需提供《核⼼涉密⼈员因公出国(境)备案表》。\n4. 出国申请报告，需阐明出国时间、事由、必要性、详细⽇程、费⽤预算及费⽤来源，并盖公章。\n5. 团组中有退休返聘⼈员时，组团或派员单位应提供返聘⽂件，70岁以上⼈员应提供健康担保证明。\n6. 如有需要，还需提供其他相关证明材料，如护照、签证、健康证明等。\n7. 公司外事管理部门将会同⼈⼒资源管理部门、纪检监察等部门，对公司及各⼦公司因公临时出国管理⼯作进⾏定期或不定期检查。公司及各⼦公司外事管理⼈员要牵头对本单位因公临时出国情况进⾏⾃查。\n8. 因公出国(境)任务按以下原则进⾏审批：办理⼀般性出国，单次及3个⽉2次、半年多次、⼀年多次往返港澳执⾏公务，常驻港澳、延⻓在港澳⼯作期限，以及办理前往免签国家的出境证明，由公司审核，并上报集团公司审批。": ['因公出国需要准备什么？'],
                    "|我是⼀个专业领域AI助⼿，您的问题超出了我的知识范围，我⽆法回答哦。您可以就产品名录、解决⽅案、制度汇编等⽅⾯向我提问，我会尽⼒助您哦。其他问题可能暂时超出了我的能⼒范围，但我会不断学习进步，感谢您的理解~": ['如何看待佩洛⻄窜台事件？'],
                    "[银河麒麟桌⾯操作系统](http://magic.ifish.site:8100/magic/#/detail?id=65564ce203674dca862b0aa2534320ec&title=)|银河麒麟桌⾯操作系统 V10 SP1 是⼀款体验好⽤、安全好⽤、⽣态好⽤、⾏业好⽤的新⼀代图形化桌⾯操作系统，为⽤户开启安全可信、流畅愉悦的体验之旅。\n![Imgur](/GXZHYHQL.jpg)\n**体验好⽤**：桌⾯环境实现界⾯⻛格和交互设计全新升级，⽀持系统主题⼀键切换和多项个性化设置，全新上线字体管理器、⼿机助⼿、麒麟管家等⾃研应⽤，⽀持⼿机电脑间多端互联；\n**安全好⽤**：⽀持可信计算 3.0 技术，并通过创新的双体系架构 , 实现⼀体化内⽣安全可信体系；\n**⽣态好⽤**：同源⽀持国内外主流处理器架构，并不断使能 GPU、桥⽚等各种新硬件，提供最优的软硬件兼容性和⼴泛的应⽤⽣态⽀持；\n**⾏业好⽤**：提供域控、私有化软件商店等多款增值产品，满⾜各⾏业需求。落地千⾏百业正版化迁移标杆案例，提供快速、完善的响应机制、遍布全国的售后服务⽹点和完善的售后服务体系。": ['银河麒麟桌⾯操作系统有什么特点？'],
                    "[银河麒麟桌⾯操作系统](http://magic.ifish.site:8100/magic/#/detail?id=65564ce203674dca862b0aa2534320ec&title=)|有的。银河麒麟桌⾯操作系统 V10 SP1 不仅满⾜了桌⾯的使⽤需求，此外配套的麒麟云桌⾯、云打印、麒麟天御安全管控平台、邮件等通⽤解决⽅案，并全⾯形成党政、⾦融、教育、通信和能源等⾏业解决⽅案。系统全⾯覆盖个⼈、企业乃⾄更⾼安全要求的⽇常和办公使⽤场景，为数字化经济时代的业务转型，提供核⼼竞争⼒。\n其中，党建云联合解决⽅案整体架构上是遵循全国党员信息库信息采集与报送规范并协同三⼤体系进⾏设计，基于中国软件⾃研的基础平台进⾏开发，整体环境运⾏于银河麒麟⾼级服务器操作系统V10之上，⽀持前后端分离和微服务架构，⽀持多种部署环境和部署⽅式，具备功能丰富、灵活定制、快速集成、安全保障的特性。在数据⽀持层，按照数据标准进⾏建设并采⽤分库设计。在业务服务层主要采⽤微服务架构，将系统拆分成各个 服务，增加系统的灵活性。在此基础上建设五⼤平台(“⼯作管理”、“互动交流”、“学习教育”、“社会治理”、“决策⽀撑”)的业务应⽤。\n相关介绍材料⻅链接：[《基于银河麒麟操作系统的党建云解决⽅案》](/GXZHYHQL.pdf)": ['有相关解决⽅案介绍么？'],
                }
                yt2prompt_dict[你好] = ['你好', '你是谁']
                for (yt in yt2prompt_dict) {
                    for (prompt in yt2prompt_dict[yt]) {
                        await add_rtst_memory(yt, yt2prompt_dict[yt][prompt], "gxzh_zsk",true)
                    }
                }
                alert("完成")
            }
        }, {
            title: '删除意图向量库',
            content: '本功能用于测试',
            click: async () => {
                await del_rtst_memory("gxzh_zsk",true)
                alert("完成")
            }
        }
        ],
            true
        )

    },
    color: () => app.color,
    description: "知识库"
})
// 定义一个函数，接受一个string参数
function splitString(str) {
    // 用‘|’分割string，得到两个子字符串
    let [first, second] = str.split('|');
    // 用‘，’分割first，得到一个数组
    let arr = first.split(',');
    // 定义一个空列表，用于存放字典
    let list = [];
    // 遍历数组中的每个元素
    for (let item of arr) {
      // 用正则表达式匹配方括号和小括号内的内容
      let match = item.match(/\[(.+?)\]\((.+?)\)/);
      // 如果匹配成功，提取title和content为方括号内的内容，url为小括号内的内容
      if (match) {
        let title = match[1];
        let url, content;
        if (match[2].startsWith("http")) {
            content = match[1];
            url = match[2];
        } else {
            content = match[2];
            url = '';
        }
        // 创建一个字典，包含title, content, url三个键值对
        let dict = {title, content, url};
        // 把字典添加到列表中
        list.push(dict);
      }
    }
    // 返回列表
    return list;
  }
  
gx展会 = async (Q) => {
    memory = await find_rtst_memory(Q, "gxzh_zsk",true)
    memory = memory.filter(i => !i.score || i.score < 100)
    if (memory.length > 0) {
        add_conversation("user", Q)
        let answer = memory[0].title.split('|')[1]
        let sources = splitString(memory[0].title)
        add_conversation("AI", answer, sources)
        save_history()
        return answer

    } else {
        return await answer_with_kgst(Q)
    }
    //+ " Alice: " + A
}
func.push({
    name: "知识库",
    question: async (Q) => {
        return await gx展会(Q)
    }
})