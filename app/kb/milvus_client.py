# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/23 12:05
"""
from pymilvus import CollectionSchema, DataType, FieldSchema, MilvusClient

from app.config import settings

COLLECTION = "knowledge"
DIM = 1024

# 获取向量数据库的客户端
def get_client(uri: str | None | None) -> MilvusClient:
    return MilvusClient(uri=uri or settings.milvus_uri)

# 建集合（有幂等性判断），集合的schema，及创建索引
def ensure_collection(client: MilvusClient) -> None:
    if client.has_collection(COLLECTION):
        client.load_collection(COLLECTION)
        return

    schema = CollectionSchema([
        FieldSchema("id", DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema("vector", DataType.FLOAT_VECTOR, dim=DIM),
        FieldSchema("question", DataType.VARCHAR, max_len=2048),
        FieldSchema("answer", DataType.VARCHAR, max_len=2048),
    ])

    client.create_collection(COLLECTION, schema=schema)

    index_params = client.prepare_index_params()
    index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")
    client.create_index(COLLECTION, index_params=index_params)
    client.load_collection(COLLECTION)
    return

# 写入数据，可批量操作
def upsert_vectors(client: MilvusClient, rows : list[dict]) -> None:
    client.upsert(COLLECTION, rows)

# search方法，根据向量相似度查找数据（向量相似度检索）
def search(client : MilvusClient, vector : list[dict], top_k : int) -> list[dict]:
    res = client.search(COLLECTION, data=[vector], limit=top_k,
                        output_fields=["question", "answer"],
                        search_params={"metric_type": "COSINE"})
    return [
        {"id": h["id"], "score": float(h["distance"]),
        "question": h["entity"]["question"], "answer": h["entity"]["answer"]}
        for h in res[0]
    ]

# query方法，可根据字段筛选数据（标量查询）
def count(client: MilvusClient) -> int:
    return client.query(COLLECTION, filter="id >= 0", output_fields=["count(*)"])[0]["count(*)"]