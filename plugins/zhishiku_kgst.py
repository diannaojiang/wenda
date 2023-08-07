
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

from langchain.embeddings import HuggingFaceEmbeddings
import sentence_transformers
import numpy as np
import re, os
from plugins.common import settings, allowCROS
from plugins.common import error_helper
from plugins.common import success_print
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from bottle import route, response, request, static_file, hook
import bottle



if settings.librarys.rtst.backend == "Annoy":
    from langchain.vectorstores.annoy import Annoy as Vectorstore
else:
    from langchain.vectorstores.faiss import FAISS as Vectorstore
divider = '\n'

if not os.path.exists('memory'):
    os.mkdir('memory')
cunnrent_setting = settings.librarys.rtst


def get_doc_by_id(id, memory_name):
    return vectorstores[memory_name].docstore.search(vectorstores[memory_name].index_to_docstore_id[id])


def process_strings(A, C, B):
    # find the longest common suffix of A and prefix of B
    common = ""
    for i in range(1, min(len(A), len(B)) + 1):
        if A[-i:] == B[:i]:
            common = A[-i:]
    # if there is a common substring, replace one of them with C and concatenate
    if common:
        return A[:-len(common)] + C + B
    # otherwise, just return A + B
    else:
        return A + B


def get_title_by_doc(doc):
    return re.sub('【.+】', '', doc.metadata['source'])


def get_doc(id, score, step, memory_name):
    doc = get_doc_by_id(id, memory_name)
    final_content = doc.page_content
    # print("文段分数：",score,[doc.page_content])
    if step > 0:
        for i in range(1, step + 1):
            try:
                doc_before = get_doc_by_id(id - i, memory_name)
                if get_title_by_doc(doc_before) == get_title_by_doc(doc):
                    final_content = process_strings(doc_before.page_content, divider, final_content)
                    # print("上文分数：",score,doc.page_content)
            except:
                pass
            try:
                doc_after = get_doc_by_id(id + i, memory_name)
                if get_title_by_doc(doc_after) == get_title_by_doc(doc):
                    final_content = process_strings(final_content, divider, doc_after.page_content)
            except:
                pass
    if doc.metadata['source'].endswith(".pdf") or doc.metadata['source'].endswith(".txt"):
        title = f"[{doc.metadata['source']}](/txt/{doc.metadata['source']})"
    else:
        title = doc.metadata['source']
    return {'title': title, 'content': re.sub(r'\n+', "\n", final_content), "score": score}




model_path = cunnrent_setting.model_path

try:
    if model_path.startswith("http"):  # "http://127.0.0.1:3000/"
        from langchain.embeddings import OpenAIEmbeddings
        import os

        os.environ["OPENAI_API_TYPE"] = "open_ai"
        os.environ["OPENAI_API_BASE"] = model_path
        os.environ["OPENAI_API_KEY"] = "your OpenAI key"

        from langchain.embeddings.openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(
            deployment="text-embedding-ada-002",
            model="text-embedding-ada-002"
        )
    else:
        from langchain.embeddings import HuggingFaceEmbeddings

        embeddings = HuggingFaceEmbeddings(model_name='')
        embeddings.client = sentence_transformers.SentenceTransformer(
            model_path, device="cuda")
except Exception as e:
    error_helper("embedding加载失败",
                 r"https://github.com/l15y/wenda")
    raise e
vectorstores = {}


def get_vectorstore(memory_name):
    try:
        return vectorstores[memory_name]
    except Exception as e:
        try:
            vectorstores[memory_name] = Vectorstore.load_local(
                'memory/' + memory_name, embeddings=embeddings)
            return vectorstores[memory_name]
        except Exception as e:
            success_print("没有读取到RTST记忆区%s，将新建。" % memory_name)
    return None


#######################################################

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
    similar_sentences = [(score, sentence) for score, sentence in sorted_combined if score > threshold]

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
def create_markdown_table_new(triplets):
    candidate_data = defaultdict()

    for labels, items in triplets.items():
        for item in items:
            sequence = f"{labels[0]}{item[0]}，{item[1]}，{labels[1]}{item[2]}"
            line = f"| {item[0]} | {item[1]} | {item[2]} |\n"
            title = "知识图谱"
            candidate_data[sequence] = {"title": title, "content": line}

    return candidate_data

def create_markdown_table_path_new(path_triplets):
    candidate_data = defaultdict()
    for path_triplet in path_triplets:
        sentence = "".join(path_triplet.split(" | "))
        line = "| " + path_triplet + " |"
        title = "知识图谱"
        candidate_data[sentence] = {"title": title, "content": line}
    return candidate_data


def get_entity_triplets_node(output_text):
    entity_list = process_entities(output_text)
    all_triplets = defaultdict(list)

    for entity in entity_list:
        triplets = get_node_triplets(entity)
        for labels, items in triplets.items():
            all_triplets[labels].extend(items)

    kg_recall_data = create_markdown_table_new(all_triplets)
    return kg_recall_data

def get_entity_triplets_path(output_text):
    entity_list = process_entities(output_text)
    path_triplets = get_path_triplets(entity_list)
    kg_recall_data = create_markdown_table_path_new(path_triplets)
    return kg_recall_data



def find_rtst(query, step=0, memory_name="CSSRegulations"):
    try:
        embedding = get_vectorstore(memory_name).embedding_function(query)
        scores, indices = vectorstores[memory_name].index.search(
            np.array([embedding], dtype=np.float32),
            int(cunnrent_setting.count)
        )
        docs = defaultdict()
        for j, i in enumerate(indices[0]):
            if i == -1:
                continue
            if scores[0][j] > 260: continue
            content = get_doc(i, scores[0][j], step, memory_name)["content"]
            title = get_doc(i, scores[0][j], step, memory_name)["title"]
            docs[content] = {"title":title, "content": content}

        return docs
    except Exception as e:
        print(e)
        return defaultdict()


def find_kg(output_text, step = 0):
    try:
        kg_recall_data = get_entity_triplets_node(output_text)
        kg_recall_data.update(get_entity_triplets_path(output_text))
        return kg_recall_data
    except Exception as e:
        print(e)
        return defaultdict()

def filter_data(recall_data, query):
    sentence_list = list(recall_data.keys())
    answer_data = []
    similarity_sentence_list = calculate_similarity(query, sentence_list)
    for score, sentence in similarity_sentence_list:
        if sentence in sentence_list:
            recall_data[sentence].update({"score": score})
            answer_data.append(recall_data[sentence])
    return answer_data


def find(search_query, step=0, memory_name="CSSRegulations"):
    output_text, query = search_query.split("||")
    kg_recall_data = find_kg(output_text, step)
    rtst_recall_data = find_rtst(query, step=step, memory_name="CSSRegulations")
    recall_data = defaultdict()
    recall_data.update(kg_recall_data)
    recall_data.update(rtst_recall_data)
    answer_data = filter_data(recall_data, query)
    return answer_data