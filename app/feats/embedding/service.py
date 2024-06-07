from fastapi import Depends
import os
import sys
import pickle
import numpy as np

import openai as OpenAI
from app.settings import settings

OPENAI_MODEL = "gpt-3.5-turbo-1106"
OPENAI_EMB_MODEL = "text-embedding-3-small"


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.gpt_key)


def load_embed(path):
    with open(path, "rb") as f:
        embed = pickle.load(f)
    return embed


RAG_DB = load_embed(sys.argv[1])


def get_embedding(text, client):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=OPENAI_EMB_MODEL).data[0].embedding
    )


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_RAG(embed, code, nbest=1):
    score = {}
    for k in embed:
        score[k] = cosine_similarity(code, embed[k])
    score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    return score[0:nbest]


def get_best_RAG(query, client: OpenAI):
    code = get_embedding(query, client)
    best_chunk = search_RAG(RAG_DB, code, 3)
    return " ".join(map(lambda it: it[0], best_chunk))
