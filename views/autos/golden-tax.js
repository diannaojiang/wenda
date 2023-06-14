
window._golden_tax_url = 'http://114.246.84.186:17860' //'http://39.130.240.104:8091' //
app.plugins.push({ icon: 'gold', url: "http://39.130.240.104:8091/shuiwu/zhenzhu/#/" })
// chrome://flags/#unsafely-treat-insecure-origin-as-secure
app.golden_tax_faqs = [
    '2022年北京市金融业的入库税额总计是多少？',
    '2022年广东高新技术企业的净利润总计是多少？',
    '2022年北京市千户集团企业的应纳税额总计是多少？',
    '2022年广东省高新技术企业小米集团的营业收入是多少？'
]
func.push({
    name: "金小税",
    icon: 'gold',
    settings:{
        autoPrintZhenzhulian: {
            type: Boolean,
            label: '税珍珠打字机效果',
            default: false
        },
        scrollToBottomWhileAnswer:{
            type: Boolean,
            label: '应答时滚动条触底',
            default: true
        },
        printSpeed:{
            type: Number,
            label: '打字速度',
            default:100
        }
    },
    description: "请输入内容",
    question: async () => {
        let Q = app.question
        const origText = Q
        app.question = ''
        app.max_length = 4096
        if(Q.indexOf('标签、指标、维度')===-1){
            Q +=  '\n请帮我抽取这段话中的标签、指标、维度。'
        }
        
        let cbmAnswer = await send(Q, Q, true)
        if(!cbmAnswer || cbmAnswer === '……'){
            // cbm未生成文字
            return
        }

        let answerZhenZhuLian = { role: "AI", content: '……' }
        let answerZhaiYao = { role: "AI", content: '……' }
        let retDataZhaiYao = null
        var isFirstPrintOver = { watchValue:false }
        var lastTimeValue=isFirstPrintOver.watchValue
        let lazyPrintZhaiyao = false

        Object.defineProperty(isFirstPrintOver, 'watchValue', {
            get: function() {
                return watchValue;
            },
            set: function(value) {
                watchValue = value;
                if(lastTimeValue!=watchValue){
                    lastTimeValue=watchValue;
                    if(value){
                        if(!retDataZhaiYao){
                            lazyPrintZhaiyao = true
                        }else{
                            app.loopPrintWords(answerZhaiYao, '摘要', retDataZhaiYao,true)
                        }
                    }

                }
            }
        })

        app.chat.push(answerZhenZhuLian)
        app.$request({
            url:_golden_tax_url + '/tax_cbm/AIanswer',
            method:'post',
            data:{
                inputData: cbmAnswer
            }
        }).then(res=>{
            if(res.status === 200){
                app.loading=false
                const propInfo = '珍珠链情况'
                if(res.data[propInfo]){
                    answerZhenZhuLian.content = `#### ${propInfo}: \n` + res.data[propInfo]
                    app.scrollToBottom()
                    isFirstPrintOver.watchValue = true
                }
            }
        })
        
        app.$request({
            url:_golden_tax_url + '/tax_cbm_abs/AI_abs',
            method:'post',
            data:{
                inputData: cbmAnswer,
                text: origText
            }
        }).then(res=>{
            if(res.status === 200){
                app.loading=false
                const propSummary = '摘要'
                if(res.data[propSummary]){
                    retDataZhaiYao = res.data[propSummary]
                    if(lazyPrintZhaiyao){
                        app.loopPrintWords(answerZhaiYao, propSummary, retDataZhaiYao, true)
                    }
                }
            }
        })
    }
})