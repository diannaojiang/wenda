import requests
import re
from plugins.common import settings


profile = "neo4j://10.37.41.248:7687"
neo4j_user = "neo4j"
neo4j_pwd = "cssailab"

import json
from collections import defaultdict

import re


def remove_meaningless_symbols(item):
    # 定义无意义符号的正则表达式模式
    pattern = r"^[,.!?，。！？\s]+|[,.!?，。！？\s]+$"
    # 使用正则表达式替换空白字符和无意义符号
    cleaned_text = re.sub(pattern, "", item)
    return cleaned_text

def process_entities(input_string):
    entities_start_index = input_string.index("关键词：") + len("关键词：")
    entities_string = input_string[entities_start_index:].strip()
    entity_list = [remove_meaningless_symbols(i) for i in entities_string.split("、")]
    return entity_list


def process_triplets(triplets):
    triplets_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for triplet in triplets:
        node1, relationship, node2 = triplet
        source_name = node1["name"]
        source_label = node1["实体类型"]
        target_label = node2["实体类型"]

        triplets_dict[source_name + source_label][relationship][target_label].append(node2)

    return triplets_dict

def format_nodes(nodes2_dict):
    return "".join([f"{node2_label}{nodes2}" for node2_label, nodes2 in nodes2_dict.items()])


def process_kg_prompt(kg_recall_data):
    if not kg_recall_data:
        return ""
    union_prompt = "***相关背景知识如下***\n" + "\n".join(kg_recall_data)
    return union_prompt


def get_entity_triplets_base(output_text):
    kg_recall_data = []
    entity_list = process_entities(output_text)
    for entity in entity_list:
        triplets = get_node_triplets(entity)
        if triplets:
            for tabel_key, items in triplets.items():
                triplets_table = tabel_key + "\n| ------ | ------ | ------ |\n"
                for item in items:
                    triplets_table += "| " + " | ".join(item) + " |" + "\n"
                kg_recall_data.append(triplets_table)
    return kg_recall_data


def get_entity_triplets(output_text):
    kg_recall_data = []
    entity_list = process_entities(output_text)
    triplets = get_related_triplets(entity_list)
    print()
    # for entity in entity_list:
    #     triplets = get_node_triplets(entity)
    #     other_dict = process_triplets(triplets)
    #     kg_recall_data.append(other_dict) if other_dict else None
    return kg_recall_data


import pandas as pd
from py2neo import Graph
from copy import deepcopy

graph = Graph(profile=profile, user=neo4j_user, password=neo4j_pwd)

def get_node_triplets(node_name):
    # 构建Cypher查询语句
    cypher_query = (
        f"MATCH (n)-[r]-(m) "
        f"WHERE n.name = '" + node_name + "' "
        "RETURN n.name AS n_name, labels(n)[0] AS n_label, type(r) AS rel, m.name AS m_name, labels(m)[0] AS m_label"
    )

    # 执行查询
    results = graph.run(cypher_query)
    results_copy = deepcopy(results.data())

    tabel_dict = {}
    if results_copy:
        for result in results_copy:
            label_key = "| " + result["n_label"] + " | 关系 | " + result["m_label"] + " |"
            if label_key not in tabel_dict:
                tabel_dict.update({label_key: [[result["n_name"], result["rel"], result["m_name"]]]})
            else:
                tabel_dict[label_key].append([result["n_name"], result["rel"], result["m_name"]])
        return tabel_dict
    else:
        return None

def get_related_triplets(entity_list):
    queries = []
    for i in range(len(entity_list)):
        for j in range(i+1, len(entity_list)):
            cypher_query = (
                f"MATCH path = allShortestPaths((a)-[*]-(b)) "
                f"WHERE a.name CONTAINS '" + entity_list[i] + "' <> b.name CONTAINS '" + entity_list[j] + "' "
                f"RETURN path"
            )
            queries.append(cypher_query)
    results = []
    for query in queries:
        result = graph.run(query)
        results.append(result)
    return results



# 定义一个函数，输入一个字符串，输出一个还原Unicode的字符串
def decode_unicode(string):
  # 使用正则表达式匹配Unicode编码
  import re
  pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
  # 使用循环替换每个匹配的编码为对应的字符
  while True:
    match = pattern.search(string)
    if match:
      code = match.group()
      char = chr(int(code[2:], 16))
      string = string.replace(code, char)
    else:
      break
  # 返回还原后的字符串
  return string


def find(search_query,step = 0):
    kg_recall_data = get_entity_triplets_base(search_query)
    # union_prompt = process_kg_prompt(kg_recall_data)
    print(kg_recall_data[0])
    return [{'title': "知识图谱",'content':re.sub(r'\n+', "\n", kg_recall_data[0])}]