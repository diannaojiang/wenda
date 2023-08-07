func.push({
    name: "AI师兄",
    question: async () => {
        let Q = app.question

        // lsdh(false)
        kownladge = (await find_dynamic(Q, 1,{'libraryStategy':"rtst:10:tjga",'maxItmes':1})).map(i => ({
            title: get_title_form_md(i.title),
            url: get_url_form_md(i.title),
            content: i.content
        }))
        if (kownladge.length > 0) {
            let prompt = app.zsk_answer_prompt + '\n' +
                kownladge.map((e, i) => i + 1 + "." + e.content).join('\n') + "\n问题：" + Q
            await send(prompt, keyword = Q, show = true, sources = kownladge)
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