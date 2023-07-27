
profile = "neo4j://10.37.41.248:7687"
neo4j_user = "neo4j"
neo4j_pwd = "cssailab"

import json
from collections import defaultdict

import re

from py2neo import Graph
from copy import deepcopy

graph = Graph(profile=profile, user=neo4j_user, password=neo4j_pwd)



def get_node_triplets(node_name):
    # Construct Cypher parameterized query
    cypher_query = (
        "MATCH (n)-[r]-(m) "
        "WHERE n.name CONTAINS $node_name "
        "RETURN n, labels(n)[0] AS n_label, type(r) AS rel, m, labels(m)[0] AS m_label"
    )

    # Execute parameterized query
    results = graph.run(cypher_query, node_name=node_name)
    data_set = set()

    tabel_dict = defaultdict(list)

    for record in results:
        result = record.data()
        label_key = f"| {result['n_label']} | 关系 | {result['m_label']} |"

        def format_node_data(node):
            return "-".join([f"({key}){value}" for key, value in node.items()])

        node_n_data = format_node_data(dict(result['n']))
        node_m_data = format_node_data(dict(result['m']))

        n_m_data = node_n_data + node_m_data
        m_n_data = node_m_data + node_n_data

        if n_m_data not in data_set and m_n_data not in data_set:
            data_set.add(n_m_data)
            data_set.add(m_n_data)
            tabel_dict[label_key].append([node_n_data, result['rel'], node_m_data])

    if not tabel_dict:
        return None

    return tabel_dict


def remove_meaningless_symbols(item):
    # 定义无意义符号的正则表达式模式
    pattern = r"^[,.!?，。！？\s]+|[,.!?，。！？\s]+$"
    # 使用正则表达式替换空白字符和无意义符号
    cleaned_text = re.sub(pattern, "", item)
    return cleaned_text

def process_entities(input_string):
    entities_start_index = input_string.index("关键词：") + len("关键词：")
    entities_string = input_string[entities_start_index:].strip()
    entity_list = [remove_meaningless_symbols(i) for i in re.split(r"、|，", entities_string)]
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
    union_prompt = "只根据以下的表格内容回答问题\n" + "***\n".join(kg_recall_data)
    return union_prompt

def process_text(kg_recall_data):
    if not kg_recall_data:
        return ""
    union_prompt =  "***\n".join(kg_recall_data)
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


def find(search_query,step = 0):
    kg_recall_data = process_text(list(set(get_entity_triplets_base(search_query))))
    # union_prompt = process_kg_prompt(kg_recall_data)
    # print(kg_recall_data)
    return [{'title': "知识图谱",'content':re.sub(r'\n+', "\n", kg_recall_data).strip()}]