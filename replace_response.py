# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from functools import reduce
import datetime
import psutil
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_EXECUTOR_REMOVED
from apscheduler.schedulers.background import BackgroundScheduler
# -------------SETTINGS------------------


REPlACE_DICT = {
"GLM-6B": "CBM",
"GLM": "CBM",
"清华大学 KEG 实验室": "中国软件研究院",
"清华大学KEG实验室": "中国软件研究院",
"智谱 AI ": "中国软件",
"智谱AI ": "中国软件"
}

EXPIRY_DATETIME = "2023-04-06 15:48:00"  # 过期时间
DATETIME_FORMATE = '%Y-%m-%d %H:%M:%S'  # 时间格式
PORT = 17860
# ------------
# replace_list = [(k,v) for k,v in replace_dict.items()]
# replace_function = lambda check_str: reduce(lambda x,y:x.replace(y[0],y[1]),replace_list, check_str)


def check_response(response, check_pass_length, pass_response):
    """"检测模型每次输出的字符串"""
    # 需要检测的部分字符\E4\B8?
    check_response = response[check_pass_length:]

    # 默认不存在可疑字符
    is_questionable = False
    # 默认检测后可输出pass_response
    is_output = True
    max_questionable_str_count = 0

    # 在字符串中进行关键词查找并替换
    for k, v in REPlACE_DICT.items():

        # 先检测字符串中是否存在关键词部分字符
        str_index = check_response.find(k[0])
        if str_index == -1:
            # 字符串中不存\E5\9C?关键词的部分字符，检测下一个关键词
            continue
        else:
            # 字符串中 存在关键词部分字符，继续检测字符串可疑部分是否以关键词部分字符为前缀
            is_questionable = k.startswith(check_response[str_index:len(k) + str_index])
            # 如果不是，继续循环检测下一个关键词
            if not is_questionable:
                continue
            else:
                # 替换
                replace_check_response = check_response.replace(k, v)
                is_replaced = False if replace_check_response == check_response else True
                check_response = replace_check_response

                # 上一步从检测出的位置,到末尾,如果有匹配的就会全替换掉;不管替换没替换掉,在字符串的末尾可能有改关键字的疑似字符
                # 那就匹配下最后一个疑似位置到末尾,看看是否全部疑似
                questionable_str_count = check_response[::-1].find(k[0])+1

                if k.startswith(check_response[-questionable_str_count:]):
                    # 全部疑似,不输出
                    is_output = False
                    # 可疑字符串的个数（有可能末尾是多个关键词的可疑字符串，那就选取可疑字符串最大值）
                    max_questionable_str_count = max(max_questionable_str_count, questionable_str_count)
                else:
                    # 末尾不是该关键词可疑字符,继续监测下一个关键词
                    continue

                    # # 对特殊替换词的替换进行特殊处理
                    # # 如果发生了替换
                    # if is_replaced:
                    #     if k == '':
                    #         check_response[]

    if is_output:
        # 字符串检测通过

        # 更新检测通过的字符串,和长度
        check_pass_length = len(response)
        pass_response += check_response

    else:
        # 末尾存在可疑字符，更新检测通过的字符串和长度位置到可疑字符位置
        check_pass_length = len(response) - max_questionable_str_count
        pass_response += check_response[:-max_questionable_str_count]

    return check_pass_length, pass_response


def license_check_func(*args,**kwargs):
    """检查程序是否到期,到期了kill掉该程序"""
    print(f"过期时间:{EXPIRY_DATETIME}")
    # 当期时间
    current_date = datetime.datetime.today()
    # 判断是否已经到期
    if current_date >= datetime.datetime.strptime(EXPIRY_DATETIME, DATETIME_FORMATE):
        print(f'当前时间{current_date}已到期')
        # 过期了, kill掉程序
        # # 找到程序的PID
        pid = None
        net_con = psutil.net_connections()
        for con_info in net_con:
            if con_info.laddr.port == int(PORT):
                pid = con_info.pid
                print(f'port:{PORT}的pid是:{pid}, 结束该pid')
                os.system(f"kill -9 {pid}")
                break
        if pid is None:
            print(f"port:{PORT}的进程不存在")
    else:
        pass
        print("未到期")

    return


# 定时任务开启
class LicenseCheckTask:

    def __init__(self):

        self.func = license_check_func
        self.scheduler = BackgroundScheduler()
        # self.scheduler = BlockingScheduler()

    def monitor(self, event):
        if event.exception:
            print("任务出错了")
        else:
            print("任务照常运行")

    def run(self):

        # self.scheduler.add_job(self.func, "cron", hour=0, minute=1, end_date=datetime.datetime.strptime(EXPIRY_DATETIME, DATETIME_FORMATE) + datetime.timedelta(minutes=2), timezone="Asia/Shanghai")
        # # self.scheduler.add_job(self.func, "interval", seconds=self.interval_days, timezone="Asia/Shanghai")
        # self.scheduler.add_listener(self.monitor, EVENT_JOB_EXECUTED|EVENT_JOB_ERROR|EVENT_EXECUTOR_REMOVED)
        # self.scheduler.start()
        # print("定时任务开启成功")
        print("暂关闭")


if __name__ == "__main__":
    # str1 = "我是一个///我是一个名为///我是一个名为 Chat///我是一个名为 ChatGL///我是一个名为 ChatGLM///我是一个名为 ChatGLM-///我是一个名为 ChatGLM-6///我是一个名为 ChatGLM-6B///我是一个名为 ChatGLM-6B///我是一个名为 ChatGLM-6B 的///我是一个名为 ChatGLM-6B 的人工智能///我是一个名为 ChatGLM-6B 的人工智能助手///我是一个名为 ChatGLM-6B 的人工智能助手，///我是一个名为 ChatGLM-6B 的人工智能助手，是基于///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 K///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 20///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 202///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我的任务///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我的任务是针对///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我的任务是针对用户///我是一个名为 ChatGLM-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我的任务是针对用户的问题///"
    # generate_response = str1.split("///")
    # print(generate_response, '\n-------------')
    #
    # # 字符串检测通过长度
    # cache_check_pass_length = 0
    # cache_pass_response = ''
    #
    # for response in generate_response:
    #     if response:
    #         cache_check_pass_length, cache_pass_response = check_response(response, cache_check_pass_length, cache_pass_response)
    #         print(cache_pass_response)
    #
    # if len(response) != len(cache_pass_response):
    #
    #     print(cache_pass_response + response[cache_check_pass_length:])

    # LicenseCheckTask().run()
    pass



