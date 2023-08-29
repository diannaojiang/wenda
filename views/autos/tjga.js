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
func.push({
    name: "AI师兄",
    question: async () => {
        let Q = app.question

        // lsdh(false)
        kownladge = (await find_dynamic(Q, 2,{'libraryStategy':"rtst:10:tjga",'maxItmes':2})).map(i => ({
            title: get_title_form_md(i.title),
            url: get_url_form_md(i.title),
            content: i.content
        }))
        kownladge = merge_same_title(kownladge)
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