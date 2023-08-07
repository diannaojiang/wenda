
profile = "neo4j://10.37.41.248:7687"
neo4j_user = "neo4j"
neo4j_pwd = "cssailab"

import json
from collections import defaultdict

import re

from py2neo import Graph
from copy import deepcopy
import sys
import os
graph = Graph(profile=profile, user=neo4j_user, password=neo4j_pwd)
sys.path.append(os.getcwd())
from plugins.common import success_print, error_print
from plugins.common import error_helper
from plugins.common import settings
from plugins.common import CounterLock
import sentence_transformers
model_path=settings.librarys.rtst.model_path
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name='')
embeddings.client = sentence_transformers.SentenceTransformer(model_path, device="cuda")



def format_node_data(node):
    node_data = []
    for key, value in node.items():
        if key == "name":
            node_data.append(f"{value}")
        else:
            node_data.append(f"{key}：{value}")
    return "。".join(node_data)

def extract_path_info(path_value):
    ans = []
    for node in path_value:
        ans.append(format_node_data(node.start_node))
    answer = " | ".join(ans)
    return answer



def get_node_triplets(node_name):
    cypher_query = (
        "MATCH (n)-[r]->(m) "
        "WHERE n.name CONTAINS $node_name OR m.name CONTAINS $node_name "
        "RETURN n, labels(n)[0] AS n_label, type(r) AS rel, m, labels(m)[0] AS m_label"
    )
    results = graph.run(cypher_query, node_name=node_name)
    triplets = defaultdict(list)

    for record in results:
        result = record.data()
        node_n_data = format_node_data(dict(result['n']))
        node_m_data = format_node_data(dict(result['m']))
        triplets[(result['n_label'], result['m_label'])].append([node_n_data, result['rel'], node_m_data])

    return triplets

def get_path_triplets(entity_list):
    queries = []
    for i in range(len(entity_list)):
        for j in range(i+1, len(entity_list)):
            if i != j:
                cypher_query = (
                    f"MATCH p=shortestPath((s)-[r*]->(e)) "
                    f"WHERE (s.name IN ['{entity_list[i]}'] AND e.name IN ['{entity_list[j]}']) OR (s.name IN ['{entity_list[j]}'] AND e.name IN ['{entity_list[i]}']) "
                    f"WITH p, [node IN nodes(p) | node.name] as entities "
                    f"WHERE ALL(entity IN {entity_list} WHERE entity IN entities) "
                    f"RETURN "
                    f"[node IN nodes(p)] AS shortest_path_entities, "
                    f"LENGTH(p) AS path_length"
                )

                queries.append(cypher_query)
    recall_data = set()
    for query in queries:
        result = graph.run(query)
        for record in result:
            path_value = record['shortest_path_entities']
            answer = extract_path_info(path_value)
            recall_data.add(answer)
    return list(recall_data)


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


def calculate_similarity(query_sentence, candidate_sentences, threshold=0.75):
    # 加载 Sentence Transformer 模型

    model = embeddings.client

    # 对输入的句子进行编码
    query_embedding = model.encode(query_sentence, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidate_sentences, convert_to_tensor=True)

    # 计算句子之间的余弦相似度
    cosine_similarities = sentence_transformers.util.pytorch_cos_sim(query_embedding, candidate_embeddings)

    # 将相似度和句子合并，并按相似度降序排序
    combined = zip(cosine_similarities[0].tolist(), candidate_sentences)
    sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # 选择相似度高于阈值的前5个句子
    similar_sentences = [(score, sentence) for score, sentence in sorted_combined if score > threshold][:5]

    return similar_sentences


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

####################################
def create_markdown_table(triplets, query):
    candidate_data = defaultdict(list)

    for labels, items in triplets.items():
        for item in items:
            sequence = f"{labels[0]}{item[0]}，{item[1]}，{labels[1]}{item[2]}"
            line = f"| {item[0]} | {item[1]} | {item[2]} |\n"
            candidate_data[(labels[0], labels[1])] += [sequence, line]

    similar_sentences = calculate_similarity(query, [i[idx] for i in candidate_data.values() for idx in range(len(i)) if idx % 2 == 0])

    kg_recall_data = set()
    for labels, item_list in candidate_data.items():
        label_key = f"| {labels[0]} | 关系 | {labels[1]} |"
        triplets_table = f"{label_key}\n| ------ | ------ | ------ |\n"
        flag = 0
        for similarity, sentence in similar_sentences:
            if sentence in item_list:
                triplets_table += item_list[item_list.index(sentence)+1]
                flag = 1
        if flag == 1:
            kg_recall_data.add(triplets_table)

    return kg_recall_data

def create_markdown_table_path(path_triplets, query):
    # similar_sentences = calculate_similarity(query, path_triplets)
    # kg_recall_data = set()
    # for similarity, sentence in similar_sentences:
    #     kg_recall_data.add(sentence)
    # return list(kg_recall_data)
    kg_recall_data = path_triplets
    return kg_recall_data



def get_entity_triplets_node(output_text, query):
    entity_list = process_entities(output_text)
    all_triplets = defaultdict(list)

    for entity in entity_list:
        triplets = get_node_triplets(entity)
        for labels, items in triplets.items():
            all_triplets[labels].extend(items)

    kg_recall_data = create_markdown_table(all_triplets, query)
    return kg_recall_data

def get_entity_triplets_path(output_text, query):
    entity_list = process_entities(output_text)
    path_triplets = get_path_triplets(entity_list)
    kg_recall_data = create_markdown_table_path(path_triplets, query)
    return kg_recall_data



def find(search_query, step = 0):
    output_text, query = search_query.split("||")
    kg_recall_data = process_text(list(set(get_entity_triplets_node(output_text, query)))) + process_text(list(set(get_entity_triplets_path(output_text, query))))
    # union_prompt = process_kg_prompt(kg_recall_data)
    print(kg_recall_data)
    return [{'title': "知识图谱",'content':re.sub(r'\n+', "\n", kg_recall_data).strip()}]