// 从插件内容中提取描述信息
get_auto_description = (plugin) => {
  try {
    return plugin.content.match(/@description (.+)\n/)[1].trim();
  } catch { }
  return "";
};

// 判断是否禁用了某个插件
get_auto_disabled = (plugin, name) => {
  if (disabled_auto[name] == undefined)
    return !!plugin.content.match(/wenda_auto_default_disabled/);
  return disabled_auto[name];
};

// 从插件内容中提取名称信息
get_auto_name = (plugin) => {
  try {
    return (
      plugin.content.match(/@name (.+)\n/)[1].trim() + `(${plugin.name})`
    );
  } catch { }
  return plugin.name;
};
 // 加载所有插件并将其添加到 app.autos 数组中
load_plugins = async () => {
  disabled_auto = JSON.parse(localStorage["wenda_disabled_auto"] || "{}");
  server_auto = await fetch("/api/plugins");
  server_auto = await server_auto.json();
  server_auto.forEach((plugin) => {
    let name = get_auto_name(plugin);
    let auto = {
      name: name,
      description: get_auto_description(plugin),
      content: plugin.content,
      disabled: get_auto_disabled(plugin, name),
    };
    app.autos.push(auto);
    setTimeout(()=>{
      if (!auto.disabled) eval(plugin.content);
    },0)
  });

  saved_auto = JSON.parse(localStorage["wenda_saved_auto"] || "[]");
  saved_auto.forEach((auto) => {
    app.autos.push(auto);
    setTimeout(()=>{
      if (!auto.disabled) eval(auto.content);
    },0)
  });
};
// load_plugins();
// 将启用的插件内容添加到 app.autos 数组中，显示在菜单中
add_auto = (content) => {
  let plugin = { content: content, name: "用户添加" };
  let name = get_auto_name(plugin);
  let auto = {
    name: name,
    description: get_auto_description(plugin),
    content: plugin.content,
    disabled: false,
  };
  saved_auto.push(auto);
  app.autos.push(auto);
  try {

    if (!auto.disabled) eval(plugin.content);
  } catch {

  }
  localStorage["wenda_saved_auto"] = JSON.stringify(saved_auto);
};

// 查找指定名称的插件在 saved_auto 数组中的索引
find_auto = (name) => saved_auto.findIndex((a) => a.name == name);

// 删除指定名称的插件
del_auto = (name) => {
  let auto_index = find_auto(name);
  saved_auto.splice(auto_index, 1);
  localStorage["wenda_saved_auto"] = JSON.stringify(saved_auto);
  location.reload();
};