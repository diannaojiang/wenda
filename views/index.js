功能 = []
alert = text => {
  app.snackbar_text = text// .replace(/\n/g,"<br>")
  app.snackbar = true
}

load_feature = (功能) => {
  app.会话模式 = 功能
  app.drawer = false
}
delete_current_conversation = (item) => {
  app.chat.splice(Math.floor(app.chat.indexOf(item) / 2) * 2, 2)
  save_history()
}
save_history = () => {
  localStorage['wenda_chat_history'] = JSON.stringify(app.chat)
}
中断 = () => {
  is_abord = true
  controller.abort()
  controller = new AbortController()
  signal = controller.signal
}
controller = new AbortController()
signal = controller.signal
提交 = () => {
  if (typeof app.会话模式.问题 === 'function') {
    app.会话模式.问题()
  } else {
    send(app.会话模式.问题 + app.问题, app.问题)
  }
}
re_generate = () => {
  const last_send = app.chat[app.chat.length - 2]
  app.chat.splice(app.chat.length - 2, 2)
  if (last_send.keyword) { app.问题 = last_send.keyword } else { app.问题 = last_send.content }

  提交(last_send.content, last_send.keyword)
}
send = async(s, keyword = '', show = true) => {
  if (keyword == '') keyword = s
  is_abord = false
  app.loading = true
  let QA_history
  if (app.history_on) {
    if (app.history_limit != 0 && (app.chat.length + 1) >= (app.history_limit * 2)) {
      if (app.simplify_historical_information) {
        alert(`历史信息过长，自动进行总结`)
        const zdk_stste = app.zhishiku_on
        zsk(false)
        lsdh(false)
        const prompt = '提取以下对话中的关键信息。\n' +
                    app.chat.map(i => (i.role == 'user' ? 'Alice: ' : 'Bob: ') + i.content.replace(/\n/g, '')).join('\n')
        await send(prompt)
        zsk(zdk_stste)
        lsdh(true)
        app.loading = true
        app.chat = app.chat.slice(app.chat.length - 2)
        app.chat[0].conent = '提供本次对话中的关键信息。'
        QA_history = app.chat.concat()
      } else {
        alert(`历史信息过长，将仅保留最后${app.history_limit}次chat记忆。setting为0不限制`)
        QA_history = app.chat.slice(app.chat.length - app.history_limit * 2)
      }
    } else {
      QA_history = app.chat.concat()
    }
  } else {
    QA_history = []
  }
  已排队到 = false
  setTimeout(read_now, 3000)
  app.问题 = s.replace(/\r\n/g, '\n')
  const 当前会话 = { role: 'AI', content: '……' }
  if (show) {
    app.chat.push({ role: 'user', content: app.问题, keyword: keyword })
    app.chat.push(当前会话)
  }
  setTimeout(() =>
    window.scrollTo(0, document.body.scrollHeight)
  , 0)
  try {
    response = await fetch('/api/chat_stream', {
      signal: signal,
      method: 'post',
      body: JSON.stringify({
        prompt: app.问题,
        keyword: keyword,
        temperature: app.temperature,
        top_p: app.top_p,
        max_length: app.max_length,
        history: QA_history,
        zhishiku: app.zhishiku_on
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    let buffer = ''
    app.问题 = ''
    const reader = response.body.getReader()
    while (true) {
      const { value, done } = await reader.read()
      已排队到 = true
      const res = new TextDecoder('utf-8').decode(value)
      buffer += res
      while (buffer.indexOf('///') > -1) {
        if (buffer == '/././') { // 应对网络问题
          done = true
          break
        }
        buffer = buffer.split('///')
        当前会话.content = buffer[buffer.length - 2]
        buffer = buffer[buffer.length - 1]
      }
      if (done) break
    }
  } catch { }
  if (app.语音播报) {
    if (app.zhishiku_on) { speak(当前会话.content.replace(/###[\s\S]*/, '')) } else { speak(当前会话.content) }
  }

  app.loading = false
  已排队到 = true
  save_history()
  if (is_abord) { throw new MyException('已中断') }
  return 当前会话.content
}
function MyException(message) {
  this.message = message
}
read_now = async() => {
  if (!已排队到) {
    response = await fetch('/api/chat_now', {
      method: 'get'
    })
    const j = JSON.parse(await response.text())
    if (j.queue_length != 0) { alert(j.queue_length) }
    setTimeout(read_now, 3000)
  }
}

find = async(s, step = 1) => {
  response = await fetch('/api/find', {
    method: 'post',
    body: JSON.stringify({
      prompt: s,
      step: step
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const json = await response.json()
  console.table(json)
  app.zhishiku = json
  return json
}

find_dynamic = async(s, step = 1, paraJson) => {
  console.table(paraJson)
  response = await fetch('/api/find_dynamic', {
    method: 'post',
    body: JSON.stringify({
      prompt: s,
      step: step,
      paraJson: paraJson
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  const json = await response.json()
  console.table(json)
  app.zhishiku_dynamic = json
  return json
}

function md2html(conent) {
  // return conent
  conent = String(conent)
  const md = new markdownit()
  // md.disable(['link', 'image'])
  return md.render(conent).replace(/<a /g, '<a target="_blank"')
}
zsk = (b) => {
  app.zhishiku_on = b
}
lsdh = (b) => {
  app.history_on = b
}

speak = (s) => {
  msg = new SpeechSynthesisUtterance()
  msg.rate = 1
  msg.pitch = 10
  msg.text = s
  msg.volume = 1
  speechSynthesis.speak(msg)
}
stop_listen = () => {
  recognition.stop()
  app.loading = true
}
listen = () => {
  recognition = new window.webkitSpeechRecognition()
  let final_transcript = ''
  recognition.continuous = true
  recognition.interimResults = true
  recognition.onstart = function() {
  }
  recognition.onresult = function(event) {
    let interim_transcript = ''
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript
        console.log(final_transcript)
        app.问题 = final_transcript
      } else {
        interim_transcript += event.results[i][0].transcript
      }
    }
  }
  recognition.onerror = function(e) {
    console.log(final_transcript)
    alert('语音识别失败:', e.error)
    app.语音输入中 = false
    app.loading = false
    console.log('======================' + 'error' + '======================', e)
  }
  recognition.onend = function() {
    console.log(final_transcript)
    app.问题 = final_transcript
    if (final_transcript.length > 1) { 提交() }
    app.语音输入中 = false
    app.loading = false
    console.log('======================' + 'end' + '======================')
  }
  recognition.lang = 'zh-CN'
  recognition.start()
  app.语音输入中 = true
}

copy = (s) => {
  navigator.permissions.query({ name: 'clipboard-write' }).then(result => {
    if (result.state == 'granted' || result.state == 'prompt') {
      navigator.clipboard.writeText(s.replace(/\n+/g, '\n'))
        .then(() => {
          alert('文本已经成功复制到剪切板')
          console.log('文本已经成功复制到剪切板')
        })
        .catch(err => {
        })
    } else {
      alert('当前无操作权限。请使用最新版本Chrome浏览器，并在浏览器高级设置-页面设置中允许访问剪切板')
      console.log('当前无操作权限。请使用最新版本Chrome浏览器，并在浏览器高级设置-页面设置中允许访问剪切板')
    }
  })
}
add_conversation = (role, content) => {
  app.chat.push({ 'role': role, 'content': content })
}
