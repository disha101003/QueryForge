from transformers import AutoTokenizer, AutoModel

#Add your own OPENAI API key
OPENAI_API_KEY = ''
# Configuration Dictionary
config = {
    "database_paths": {
        "ourconnect": "database/ourconnect",
        "professors": "database/professors",
        "vip": "database/vip",
        "duri": "database/DURI",
    },
    "model": {
        "name": "BAAI/bge-small-en-v1.5",
        "tokenizer": AutoTokenizer.from_pretrained("BAAI/bge-small-en-v1.5"),
        "model": AutoModel.from_pretrained("BAAI/bge-small-en-v1.5"),
    },
    "processing": {
        "chunk_size": 400,
        "para_separator": "/n /n",
        "separator": " ",
        "top_k": 10,
    },
}