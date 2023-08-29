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

func.push({
    name: "知识库",
    description: "通过知识图谱回答问题",
    question: async () => {
        answer_with_kg(app.question)
    }
})


func.push({
    name: "快速知识库",
    question: async () => {
        let Q = app.question

        // lsdh(false)
        kownladge = (await find(Q, app.zsk_step)).map(i => ({
            title: get_title_form_md(i.title),
            url: get_url_form_md(i.title),
            content: i.content
        }))
        if (kownladge.length > 0) {
            let prompt = app.zsk_answer_prompt + '\n' +
                kownladge.map((e, i) => i + 1 + "." + e.content).join('\n') + "\n问题：" + Q
            await send(prompt, keyword = Q, show = true, sources = kownladge,
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
}
)