get_title_form_md = (s) => {
    console.log(s)
    try {
        return s.match('\\[(.+)\\]')[1]
    } catch {
        return s
    }
}
get_url_form_md = (s) => {
    console.log(s)
    try {
        return s.match('\\((.+)\\)')[1]
    } catch {
        return s
    }
}
window.answer_with_kg = async (Q) => {
    // lsdh(false)
    app.chat = [{ "role": "user", "content": "从以下语句中抽取出关键词：处级的领导都有哪些？" },
                { "role": "AI", "content": "关键词：处级、领导" },
                { "role": "user", "content": "从以下语句中抽取出关键词：广东省统计局最近推出了哪些疫情防控的公文？" },
                { "role": "AI", "content": "关键词：广东省、统计局、疫情防控、公文" }
    ]
    zsk(false)
    lsdh(true)//打开历史对话
    
    resp = (await send("从以下语句中抽取出关键词：" + Q))
    .replace(/\n- /g, '\n1.')//兼容不同格式
    .split("\n")

    app.chat = []
    
    // app.chat.push({ "role": "user", "content": Q })


    kownladge = (await find(resp[0], 1)).map(i => ({
        title: get_title_form_md(i.title),
        url: get_url_form_md(i.title),
        content: i.content
    }))
    console.log(kownladge)
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
        console.log(kownladge)
        var kg_content = kownladge[0].content
        // var result = kg_content.split("\n"); // 按照回车符分割字符串，得到一个数组
        // result = result.slice(0, 6); // 取数组的前五个元素，得到一个新的数组
        // kg_content = result.join("\n"); 
        // app.chat.push({ "role": "AI", "content": kg_content })
        let prompt = "根据提供信息回答问题。" + '\n' + kg_content + "\n问题：" + Q
        // let prompt = "Answer the questions based only on the table below." + '\n' + kg_content + "\nQuestion：" + Q
        console.log(prompt)
        return await send(prompt, keyword = Q, show = true, sources = kownladge)
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
