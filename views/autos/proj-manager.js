func.push({
    name: "项目管理",
    
    question: async () => {
        var reg1 = /新增|增加|添加|填写/
        var reg2 = /审核|通过|审批/
        var str = app.question
        var random = false
        if (reg1.test(str)) {
            app.chat = [{ "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：帮我新增一个工作项，调试服务器，用时一小时。" },
            { "role": "AI", "content": "工作项内容：\n调试服务器\n工作时长：\n1小时" },
            { "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：新增工作项，修改控制面板，耗时四小时。" },
            { "role": "AI", "content":  "工作项内容：\n修改控制面板\n工作时长：\n4小时"}
            // { "role": "user", "content": "从以下语句中抽取出工作项内容和工作时长：帮我在税珍珠项目里面添加一个工作项，打扫卫生，三小时。" },
            // { "role": "AI", "content":  "工作项内容：\n打扫卫生\n工作时长：\n3"}
            ]
            zsk(false)
            lsdh(true)//打开历史对话
            let Q = app.question
            Q = "从以下语句中抽取出工作项内容和工作时长：" + Q
            // await send(Q)
            let cbmAnswer = await send(Q)

            // var arr = cbmAnswer.split("\n") // 按照\n分割字符串
            // let content = arr[1] // 取第二个元素，即冒号后面的内容
            var arr = cbmAnswer.split("\n") // 按照\n分割字符串
            let content = arr[1] // 取第二个元素，即冒号后面的内容
            // et duration = parseFloat(arr[3]) // 取第四个元素，即工作时长
            var reg3 = /一个工作项/
            if (reg3.test(content)){
                content = arr[2]
            }
            let duration = cbmAnswer.replace(/\n/g, "").match(/\d+\.?\d*/g) // 取第四个元素，即工作时长
            
            // 将汉字数字转换为阿拉伯数字
            if (duration === null){
                var numMap = {
                    "零": 0,
                    "一": 1,
                    "二": 2,
                    "三": 3,
                    "四": 4,
                    "五": 5,
                    "六": 6,
                    "七": 7,
                    "八": 8,
                    "九": 9,
                  }
                  // 遍历字符串中的每个字符
                for (var i = cbmAnswer.length - 1; i >= 0; i--) {
                    // 获取当前字符
                    var char = cbmAnswer[i]
                    
                    // 判断当前字符是否是汉字数字
                    if (numMap[char] !== undefined) {
                    // 如果是，就返回对应的阿拉伯数字
                        duration = numMap[char]
                        break
                    }
                }
                
                // 如果没有找到汉字数字，就返回 NaN
                if (duration === null){
                    duration = 1
                }
            }
            else{
                duration = Number(duration.pop())
            }
            if (duration >= 8){
                duration = 8
            }

            // *********************************************************演示用随机数生成日期**********************************************
            // 定义起始日期和结束日期
            if (random){
                var startDate = new Date("2020-01-01");
                var endDate = new Date("2023-07-10");
    
                // 计算日期之间的毫秒数差
                var diff = endDate.getTime() - startDate.getTime();
    
                // 生成一个随机数，乘以差值，加上起始日期的毫秒数，得到一个随机日期的毫秒数
                var randomDate = new Date(startDate.getTime() + Math.random() * diff);
    
                // 格式化日期为 yyyy-mm-dd 的形式
                var year = randomDate.getFullYear();
                var month = randomDate.getMonth() + 1; // 月份从 0 开始，所以要加 1
                var day = randomDate.getDate();
    
                // 如果月份或者日期小于 10，要在前面补 0
                if (month < 10) {
                month = "0" + month;
                }
                if (day < 10) {
                day = "0" + day;
                }
    
                // 拼接字符串，得到最终结果
                var today = year + "-" + month + "-" + day;
            }

            // *********************************************************演示用随机数生成日期**********************************************
            else{
                // 帮我增加一个工作项，写控制面板，用时1小时。
                var today = new Date() // 创建一个Date对象
                var dd = String(today.getDate()).padStart(2, '0') // 获取日期，1到31，并转换为字符串，如果长度小于2，则在前面加上0
                var mm = String(today.getMonth() + 1).padStart(2, '0') // 获取月份，0到11，并转换为字符串，如果长度小于2，则在前面加上0
                var yyyy = today.getFullYear() // 获取年份，四位数
                
                // 把日期格式化为yyyy-mm-dd的形式
                today = yyyy + '-' + mm + '-' + dd
            }


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
                    console.log(res)
                    app.chat.push({ "role": "AI", "content": '工作项添加已完成\n责任人：刘明达\n工作项类型：开发\n工作项名称：' + content + '\n登记工时：' + duration +'小时\n'+ '计划完成日期：' + today + '\n审核状态：项目经理审核'})
                }
                else{
                    app.chat.push({ "role": "AI", "content": '工作项添加失败\n失败原因：'+ res.reason+'\n明细：'+res.detail})
                }
            })
        }
                
        else if (reg2.test(str)) {
            app.chat = [{ "role": "user", "content": "从以下语句中抽取出工作项绩效：帮我审核所有工作项，绩效优秀。" },
                        { "role": "AI", "content": "工作项绩效：\n优秀" },
                        { "role": "user", "content": "从以下语句中抽取出工作项绩效：审批所有工作项，绩效合格。" },
                        { "role": "AI", "content": "工作项绩效：\n合格" },
                        // { "role": "user", "content": "从以下语句中抽取出工作项绩效：通过所有工作项。" },
                        // { "role": "AI", "content": "工作项绩效：\n优秀" }
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
                "合格": 3,
                "不合格": 4
            }

            var relation_lev = {
                1: 'A',
                2: 'B',
                3: 'C',
                4: 'D'
            }

            let performance = relation[level]


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
                    console.log(res)
                    app.chat.push({ "role": "AI", "content": '工作项审核已完成\n责任人：刘明达\n工作项类型：开发\n状态：已完成\n绩效：' + relation_lev[performance] + "\n审核状态：已通过"})
                }
                else{
                    app.chat.push({ "role": "AI", "content": '工作项审核失败\n失败原因：'+ res.reason +'\n明细：'+res.detail})
                }
            })
        }
        else{
            app.chat.push({ "role": "AI", "content": '暂不支持此种命令，请输入新增或审核工作项'})
            zsk(false)
            lsdh(true)//打开历史对话
        }
    },
    description: "新增工作项：自动填写工作项内容和工作时长；或者审核工作项：根据提供绩效自动审核所有工作项。",
})
