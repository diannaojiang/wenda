func = [
  {
    name: "",
    description: "input_question",
    question: "",
  }
];
  
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
      this.question += "\n";
    } else if (typeof app.func_mode.question == "function") {
      app.func_mode.question();
    } else {
      let Q=app.question
      await send(app.func_mode.question +Q , Q);
      app.question=''
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
  send = async (s, keyword = "", show = true, sources = []) => {
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
      QA_history=QA_history.filter(i=>!i.no_history)
    } else {
      QA_history = [];
    }
    // 如果是等待对话状态,则将 is_wait_till 设置为 true
    is_wait_till = false;
    setTimeout(display_queue_length, 3000);
    let current_session = { role: "AI", content: "……", sources: sources }
    if (show) {
      app.chat.push({ role: "user", content: keyword, keyword: keyword })
      app.chat.push(current_session);
    }
    setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 0)
    // 调用websocket聊天，具体函数在wd_sdk.js中
    await send_raw( s.replace(/\r\n/g, "\n"), keyword, QA_history, (message) => {
      is_wait_till = true;
      current_session.content = message;
    })

    if (app.tts_on) {
      speak(current_session.content);
    }
    app.loading = false;
    is_wait_till = true;
    save_history();
    if (is_abord) throw new MyException("已中断");
    return current_session.content;
  };

  // 在用户等待超过 3 秒后显示当前队列长度
  display_queue_length = async () => {
    if (!is_wait_till) {
      let queue_length = await get_queue_length();
      if (queue_length != 0) alert("当前排队数量：" + queue_length);
      setTimeout(display_queue_length, 3000);
    }
  };

  // 覆盖 console.warn 函数以不执行任何操作
  console.warn = function () { };