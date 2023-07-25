func.push({
    name: "抽取知识图谱",
    question: async () => {
        app.chat = [{ "role": "user", "content": "从以下语句中抽取出实体和关系：关于疫情防控的公文有多少" },
                    { "role": "AI", "content": "实体(Entity)：\n1. 疫情防控\n2. 公文\n关系(Relationship)：\n- '关于'：连接'疫情防控'和'公文'\n- '有多少'：查询'疫情防控'主题下的'公文'数量" },
                    { "role": "user", "content": "从以下语句中抽取出实体和关系：据北京新闻广播报道，也就是在这个中午，49岁的导游“龚哥”在带领一个研学团从颐和园结束行程后晕倒在了大巴车内，送医后抢救无效去世。医院证明显示，“龚哥”是因为热射病去世的。" },
                    { "role": "AI", "content": "实体(Entity)：\n1. 北京新闻广播\n2. 龚哥\n3. 导游\n4. 研学团\n5. 颐和园\n6. 大巴车\n7. 医院\n8. 热射病\n关系(Relationship)：\n- '据...报道'：连接'北京新闻广播'和整个报道的事件\n- '也就是在这个中午'：表示事件发生的时间\n- '49岁'：描述'龚哥'的年龄\n- '导游'：描述'龚哥'的职业\n- '在带领一个研学团...结束行程后'：描述'龚哥'与'研学团'和'颐和园'的关系，以及事件发生的背景\n- '晕倒在了大巴车内'：'龚哥'与'大巴车'的状态关系\n- '送医后抢救无效去世'：描述'龚哥'的状态改变\n- '医院证明显示'：'医院'与'证明'及事件的关系\n- '因为热射病去世'：'龚哥'与'热射病'和'去世'的关系" }
        ]
        zsk(false)
        lsdh(true)//打开历史对话
        let Q = app.question
        Q = "从以下语句中抽取出实体和关系：" + Q
        await send(Q)
    },
    description: "从语句中抽取出实体和关系",
})


func.push({
    name: "抽取事件图谱",
    question: async () => {
        app.chat = [{ "role": "user", "content": "从以下语句中抽取出事件类型、事件触发词、论元角色和论元：中国外运2019年上半年归母净利润增长17%：收购了少数股东股权。" },
                    { "role": "AI", "content": "事件类型：收购\n事件触发词：收购了\n论元角色和论元：\n事件主体：中国外运\n时间：2019年上半年\n归母净利润增长：17%\n被收购的对象：少数股东股权\n" },
                    { "role": "user", "content": "从以下语句中抽取出事件类型、事件触发词、论元角色、论元：美国亚特兰大航展13日发生一起表演机坠机事故，飞行员弹射出舱并安全着陆，事故没有造成人员伤亡。" },
                    { "role": "AI", "content": "事件类型：表演机坠机事故\n事件触发词：发生\n论元角色和论元：\n事件地点：美国亚特兰大航展\n事件时间：13日\n主要参与者：飞行员\n行为：弹射出舱并安全着陆\n结果：事故没有造成人员伤亡\n" }
        ]
        zsk(false)
        lsdh(true)//打开历史对话
        let Q = app.question
        Q = "从以下语句中抽取出事件类型、事件触发词、论元角色和论元：" + Q
        await send(Q)
    },
    description: "从语句中抽取出事件类型、事件触发词、论元角色和论元",
})


func.push({
    name: "公安扫黄打非智能抽取",
    question: async () => {
        app.chat = [{ "role": "user", "content": "从以下语句中抽取要素：分析一下近一个月站街女都在哪些公园出没" },
                    { "role": "AI", "content": "地点：公园\n人群：站街女\n意图：哪些\n时间：近一个月\n场景：查询一段时间站街女出现频次topN的几个地方\n" },
                    { "role": "user", "content": "从以下语句中抽取要素：分析一下近一个月站街女都在哪些广场出没" },
                    { "role": "AI", "content": "地点：广场\n人群：站街女\n意图：哪些\n时间：近一个月\n场景：查询一段时间站街女出现频次topN的几个地方\n" },
                    { "role": "user", "content": "从以下语句中抽取要素：分析一下近一个月站街女都在哪些公园广场出没" },
                    { "role": "AI", "content": "地点：公园广场\n人群：站街女\n意图：哪些\n时间：近一个月\n场景：查询一段时间站街女出现频次topN的几个地方\n" },
                    { "role": "user", "content": "从以下语句中抽取要素：查询近一个月站街女都在什么位置出现" },
                    { "role": "AI", "content": "地点：位置\n人群：站街女\n意图：什么\n时间：近一个月\n场景：查询一段时间站街女出现频次topN的几个地方\n" },
                    { "role": "user", "content": "从以下语句中抽取要素：查询近一个月站街女都经常在什么位置出现" },
                    { "role": "AI", "content": "地点：位置\n人群：站街女\n意图：什么\n时间：近一个月\n场景：查询一段时间站街女出现频次topN的几个地方\n" }
        ]
        zsk(false)
        lsdh(true)//打开历史对话
        let Q = app.question
        Q = "从以下语句中抽取要素：" + Q
        await send(Q)
    },
    description: "从以下语句中抽取要素",
})

func.push({
    name: "项目管理",
    
    question: async () => {
        var reg1 = /新增|增加/
        var reg2 = /审核|通过/
        var str = app.question
        if (reg1.test(str)) {
            app.chat = [{ "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：帮我新增一个工作项：调试服务器，用时8小时。" },
            { "role": "AI", "content": "工作项内容：\n调试服务器\n工作时长：\n8" },
            { "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：帮我增加一个工作项：写控制面板，耗时四小时。" },
            { "role": "AI", "content":  "工作项内容：\n写控制面板\n工作时长：\n4"},
            { "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：帮我增加一个工作项：打扫卫生，3小时。" },
            { "role": "AI", "content":  "工作项内容：\n打扫卫生\n工作时长：\n3"}
            ]
            zsk(false)
            lsdh(true)//打开历史对话
            let Q = app.question
            Q = "从以下语句中抽取出工作项内容和工作时长：" + Q
            // await send(Q)
            let cbmAnswer = await send(Q)

            // var arr = cbmAnswer.split("\n") // 按照\n分割字符串
            // let content = arr[1] // 取第二个元素，即冒号后面的内容
            // let duration = parseInt(arr[3]) // 取第四个元素，即工作时长
            var arr = cbmAnswer.split("\n") // 按照\n分割字符串
            let content = arr[1] // 取第二个元素，即冒号后面的内容
            var reg3 = /一个工作项/
            if (reg3.test(content)){
                content = arr[2]
            }
            let duration = parseInt(cbmAnswer.replace(/\n/g, "").replace(/[^0-9]/g, "")) // 取第四个元素，即工作时长
            if (duration >= 8){
                duration = 8
            }
            // 帮我增加一个工作项，写控制面板，用时1小时。
            var today = new Date() // 创建一个Date对象
            var dd = String(today.getDate()).padStart(2, '0') - 6 // 获取日期，1到31，并转换为字符串，如果长度小于2，则在前面加上0
            var mm = String(today.getMonth() + 1).padStart(2, '0') // 获取月份，0到11，并转换为字符串，如果长度小于2，则在前面加上0
            var yyyy = today.getFullYear() // 获取年份，四位数
            
            // 把日期格式化为yyyy-mm-dd的形式
            today = yyyy + '-' + mm + '-' + dd

            app.$request({
                url: '/api/addWorkItemInfoByAi',
                method:'post',
                data:{
                    creator: "cec85ab784f94f39bd71a4d5c200be6f",
                    state: "1",
                    planState: "0",
                    estimateTime: duration,
                    costTime: duration,
                    executeTime: today,
                    completeTime: today,
                    operatorId: "cec85ab784f94f39bd71a4d5c200be6f",
                    workName: content,
                    taskId: "24125ea97bf84af3b837d4534e14b171",
                    projectId: "3799b296bd574d51af2ce06b588d214c",
                    taskOperatorId: "cec85ab784f94f39bd71a4d5c200be6f",
                    isCommonWork: "0",
                    userId: "cec85ab784f94f39bd71a4d5c200be6f"
                }
            }).then(res=>{
                if(res.status === 200){
                    app.chat.push({ "role": "AI", "content": '工作项添加已完成'})
                }
            })
        }
                
        else if (reg2.test(str)) {
            app.chat = [{ "role": "user", "content": "从以下语句中抽取出工作项绩效：帮我审核刘明达的工作项，绩效优秀。" },
                        { "role": "AI", "content": "工作项绩效：\n优秀" },
                        { "role": "user", "content": "从以下语句中抽取出工作项绩效：帮我通过所有工作项，绩效良好。" },
                        { "role": "AI", "content": "工作项绩效：\n良好" }
            ]
            zsk(false)
            lsdh(true)//打开历史对话
            let Q = app.question
            Q = "从以下语句中抽取出工作项绩效：" + Q
            let cbmAnswer = await send(Q)
            var arr = cbmAnswer.split("\n") // 按照\n分割字符串
            let level = arr[1] // 取第二个元素，即冒号后面的内容
            var relation = {
                "优秀": 1,
                "良好": 2,
                "一般": 3,
                "差": 4,
                "很差": 4
              };
            let performance = relation[level]
            console.log(performance)

            app.$request({
                url: '/api/lxAuditWorkItemByAi',
                method:'post',
                data:{
                    ids: ["24125ea97bf84af3b837d4534e14b171"],
                    auditUser: "cec85ab784f94f39bd71a4d5c200be6f",
                    auditStatus: "1",
                    auditOpinion: "通过",
                    performanceLevel: performance
                  }
            }).then(res=>{
                if(res.status === 200){
                    app.chat.push({ "role": "AI", "content": '工作项审核已完成'})
                }
            })
        }
        else{
            app.chat = [{ "role": "AI", "content": "暂时不支持此种指令，请输入新增或审核工作项指令" }]
            zsk(false)
            lsdh(true)//打开历史对话
        }
    },
    description: "新增工作项：自动填写工作项内容和工作时长；或者审核工作项：自动审核所有工作项",
})
