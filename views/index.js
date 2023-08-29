func = [
  {
    name: "",
    description: "input_question",
    question: "",
  }
];
  
   //获取用户输入
   input = async (title = '请输入', input = '') => {
    app.dialog_title = title
    app.dialog_input = input
    app.show_dialog = true

    await new Promise(resolve => {
      window.dialog_input_resolver = resolve
    })
    return app.dialog_input
  }
  //编辑会话内容
  edit = async (current_conversation) => {
    let s修改后的内容 = await input('请输入修改后的内容', current_conversation.content)
    if (s修改后的内容) {
      current_conversation.content = s修改后的内容
      if(typeof current_conversation.keyword !== 'undefined'){
        current_conversation.keyword = s修改后的内容
      }
      alert('修改成功')
    } else
      alert('取消修改')
  }
  // 加载指定功能
  load_func = (func) => {
    app.current_func = func.name;
    app.drawer = false;
  };

  // 从 app 的 chat 数组中删除当前的对话项并保存更新后的历史记录
  delete_current_conversation = (item) => {
    app.chat.splice(Math.floor(app.chat.indexOf(item) / 2) * 2, 2);
    save_history();
  };

  // 将 is_abord 标志设置为 true 并关闭 WebSocket 连接
  abort_chatting = () => {
    is_abord = true;
    ws.close();
  };

  // 处理表单提交事件并将用户的输入发送到服务器
  submit = async (e) => {
    if (e && e.shiftKey) {
      return
    }
    e && e.preventDefault()
    if (typeof app.func_mode.question == "function") {
      await app.func_mode.question(app.question);
      app.question = ''
    } else {
      let Q = app.question

      if (app.history_on)
        await send(app.func_mode.question + Q, Q, show = true, sources = [],
          addition_args = { cfg_factor: app.cfg_factor, cfg_ctx: Q });
      else
        await send(app.func_mode.question + Q, Q);
    }
  };

  // 重新生成用户的最后一条消息并将其发送到服务器
  re_generate = () => {
    let last_send = app.chat[app.chat.length - 2];
    app.chat.splice(app.chat.length - 2, 2);
    if (last_send.keyword) app.question = last_send.keyword;
    else app.question = last_send.content;

    submit();
  };

  // 总结聊天历史记录并提示用户提取关键信息
  summerize_history = async () => {
    zsk(false);
    lsdh(false);
    let prompt =
      "提取以下对话中的关键信息。\n" +
      app.chat
        .map(
          (i) =>
            (i.role == "user" ? "Alice: " : "Bob: ") +
            i.content.replace(/\n/g, "")
        )
        .join("\n");
    await send(prompt);
    lsdh(true);
    app.loading = true;
    app.chat = app.chat.slice(app.chat.length - 2);
    app.chat[0].content = "提供本次对话中的关键信息。";
  };

  // 将用户的输入发送到服务器并更新 app 的 chat 数组
  // 参数s为用户输入的内容，keyword为用户输入的关键词，show为是否显示用户输入的内容，sources为知识库的来源
  let last_cost = []
  send = async (s, keyword = "", show = true, sources = [], addition_args = {}) => {
    app.question = ''
    if (keyword == "") keyword = s;
    is_abord = false;
    app.loading = true;

    let QA_history;
    // 如果历史记录开启,则将历史记录保存到 QA_history 中
    if (app.history_on) {
      if (
        app.history_limit != 0 &&
        app.chat.length + 1 >= app.history_limit * 2
      ) {
        if (app.simplify_historical_information) {
          alert(`历史信息过长，自动进行总结`);
          await summerize_history();
          QA_history = app.chat
        } else {
          alert(
            `历史信息过长，将仅保留最后${app.history_limit}次chat记忆。setting为0不限制`
          );
          QA_history = app.chat.slice(
            app.chat.length - app.history_limit * 2
          );
        }
      } else {
        QA_history = app.chat
      }
      QA_history = QA_history.filter(i => !i.no_history)
    } else {
      QA_history = [];
    }
    let current_session = { role: "AI", content: "……", sources: sources };
    if (show) {
      app.chat.push({ role: "user", content: s, keyword: keyword });
      app.chat.push(current_session);
    }
    setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 0);
    // 调用websocket聊天，具体函数在wd_sdk.js中
    let last_token_time = Date.now()
    await send_raw(s.replace(/\r\n/g, "\n"), keyword, QA_history, (message) => {
      current_session.content = message;
      let now = Date.now()
      let cost = now - last_token_time
      last_cost.push(cost)
      if (last_cost.length > 10) last_cost.shift()
      let avg_cost = 0
      last_cost.forEach(v => avg_cost += v)
      avg_cost /= last_cost.length
      app.TPS = 1000 / avg_cost
      last_token_time = now
    }, addition_args);
    if (app.tts_on) {
      speak(current_session.content);
    }
    app.loading = false;
    save_history();
    if (is_abord) throw new MyException("已中断");
    return current_session.content;
  };


  // 覆盖 console.warn 函数以不执行任何操作
  console.warn = function () { };