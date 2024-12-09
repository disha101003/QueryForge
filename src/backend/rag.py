import os
import re
import uuid
import torch
import numpy as np
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config.config import config, OPENAI_API_KEY
# Load database paths from config
directory_path_ourconnect = config["database_paths"]["ourconnect"]
directory_path_professors = config["database_paths"]["professors"]
directory_path_vip = config["database_paths"]["vip"]
directory_path_duri = config["database_paths"]["duri"]

# Load model details from config
model_name = config["model"]["name"]
tokenizer = config["model"]["tokenizer"]  # Pre-initialized tokenizer
model = config["model"]["model"]          # Pre-initialized model

# Load processing parameters from config
chunk_size = config["processing"]["chunk_size"]
para_seperator = config["processing"]["para_separator"]
separator = config["processing"]["separator"]
top_k = config["processing"]["top_k"]
# Add your OPENAI_API_KEY here before running
openai_model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

chat = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)


def chunking(
        directory_path,
        tokenizer,
        chunk_size,
        para_seperator=" /n /n",
        separator=" "):

    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    documents = {}
    all_chunks = {}
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(filename)
        base = os.path.basename(file_path)
        sku = os.path.splitext(base)[0]
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            doc_id = str(uuid.uuid4())

            paragraphs = re.split(para_seperator, text)

            for paragraph in paragraphs:
                words = paragraph.split(separator)
                current_chunk_str = ""
                chunk = []
                for word in words:
                    if current_chunk_str:
                        new_chunk = current_chunk_str + separator + word
                    else:
                        new_chunk = current_chunk_str + word
                    if len(tokenizer.tokenize(new_chunk)) <= chunk_size:
                        current_chunk_str = new_chunk
                    else:
                        if current_chunk_str:
                            chunk.append(current_chunk_str)
                        current_chunk_str = word

                if current_chunk_str:
                    chunk.append(current_chunk_str)

                for chunk in chunk:
                    chunk_id = str(uuid.uuid4())
                    all_chunks[chunk_id] = {
                        "text": chunk, "metadata": {
                            "file_name": sku}}
        documents[doc_id] = all_chunks
    return documents

# Make Document Embeddings


def map_document_embeddings(documents, tokenizer, model):
    mapped_document_db = {}
    for id, dict_content in documents.items():
        mapped_embeddings = {}
        for content_id, text_content in dict_content.items():
            text = text_content.get("text")
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True)
            with torch.no_grad():
                embeddings = model(
                    **inputs).last_hidden_state.mean(dim=1).squeeze().tolist()
            mapped_embeddings[content_id] = embeddings
        mapped_document_db[id] = mapped_embeddings
    return mapped_document_db

# Retrieve Information by implementing similarity search from queries


def retrieve_information(query, top_k, mapped_document_db):
    query_inputs = tokenizer(
        query,
        return_tensors="pt",
        padding=True,
        truncation=True)
    query_embeddings = model(
        **query_inputs).last_hidden_state.mean(dim=1).squeeze()
    query_embeddings = query_embeddings.tolist()
    # converting query embeddings to numpy array
    query_embeddings = np.array(query_embeddings)

    scores = {}
    # Now calculating cosine similarity
    for doc_id, chunk_dict in mapped_document_db.items():
        for chunk_id, chunk_embeddings in chunk_dict.items():
            # converting chunk embedding to numpy array for efficent
            # mathmetical operations
            chunk_embeddings = np.array(chunk_embeddings)

            # Normalizing chunk embeddings and query embeddings  to get cosine
            # similarity score
            normalized_query = np.linalg.norm(query_embeddings)
            normalized_chunk = np.linalg.norm(chunk_embeddings)

            if normalized_chunk == 0 or normalized_query == 0:
                # this is being done to avoid division with zero which will
                # give wrong results i.e infinity. Hence to avoid this we set
                # score to 0
                score = 0
            else:
                # Now calculationg cosine similarity score
                score = np.dot(chunk_embeddings, query_embeddings) / \
                    (normalized_chunk * normalized_query)

            # STORING SCORES WITH THE REFERENCE
            scores[(doc_id, chunk_id)] = score

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True)[
        :top_k]

    top_results = []
    for ((doc_id, chunk_id), score) in sorted_scores:
        results = (doc_id, chunk_id, score)
        top_results.append(results)
    return top_results

# Function to compute embeddings


def compute_embeddings(query, tokenizer, model):
    query_inputs = tokenizer(
        query,
        return_tensors="pt",
        padding=True,
        truncation=True)
    query_embeddings = model(
        **query_inputs).last_hidden_state.mean(dim=1).squeeze()
    query_embeddings = query_embeddings.tolist()
    return query_embeddings

# Function to compute Cosine Similarity Search


def calculate_cosine_similarity_score(query_embeddings, chunk_embeddings):
    normalized_query = np.linalg.norm(query_embeddings)
    normalized_chunk = np.linalg.norm(chunk_embeddings)
    if normalized_chunk == 0 or normalized_query == 0:
        score = 0
    else:
        score = np.dot(chunk_embeddings, query_embeddings) / \
            (normalized_chunk * normalized_query)
    return score

# Retrieve Top Matches


def retrieve_top_k_scores(query_embeddings, mapped_document_db, top_k):
    scores = {}

    for doc_id, chunk_dict in mapped_document_db.items():
        for chunk_id, chunk_embeddings in chunk_dict.items():
            # converting chunk embedding to numpy array for efficent
            # mathmetical operations
            chunk_embeddings = np.array(chunk_embeddings)
            score = calculate_cosine_similarity_score(
                query_embeddings, chunk_embeddings)
            scores[(doc_id, chunk_id)] = score
    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True)[
        :top_k]

    return sorted_scores

# Helper function to retrieve Top Matches


def retrieve_top_results(sorted_scores):
    top_results = []
    for ((doc_id, chunk_id), score) in sorted_scores:
        results = (doc_id, chunk_id, score)
        top_results.append(results)
    return top_results

# Helper function to save file


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# Helper function to read json files


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

# Helper function to retrieve text from matches


def retrieve_text(top_results, document_data):
    first_match = top_results[0]
    doc_id = first_match[0]
    chunk_id = first_match[1]
    related_text = document_data[doc_id][chunk_id]
    return related_text

# Generate LLM response


def generate_llm_response(openai_model, query, relevant_text):
    # Template with an emphasis on bullet points and extracting details
    template = """
    You are an intelligent search engine designed to assist users by
    extracting key information in an organized manner.

    You will be provided with:
    1. Some retrieved context.
    2. A user's query.

    Your task is to:
    - Parse and extract all relevant information in response to the query.
    - Present the results in clean, concise points.
    - Give lots of information, try to cover all the relevant text you get.
    - Include details such as names, roles, descriptions, contact information,
    or any other pertinent details, if available.
    - If multiple relevant entries are found in the context, list each entry
    with its details.

    Here is the context:
    <context>
    {context}
    </context>

    Question: {question}
    Provide the response below in bullet-point format.
    """
    # Build the prompt template
    prompt = ChatPromptTemplate.from_template(template=template)

    # Chain the prompt to the model
    chain = prompt | openai_model

    # If relevant_text contains multiple entries, combine them
    if isinstance(relevant_text, list):
        combined_context = " ".join(item.get("text", "")
                                    for item in relevant_text)
    else:
        combined_context = relevant_text.get("text", "")

    # Invoke the chain with the query and combined context
    response = chain.invoke({"context": combined_context, "question": query})

    return response


# Function to load JSON data
def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


# Load documents and mapped document embeddings from vector databases
document_data = load_json("documents/doc_store_2.json")  # Load document store
mapped_document_db = load_json(
    "documents/vector_store_2.json")  # Load vector store
document_data_prof = load_json("documents/doc_store_prof.json")
mapped_document_db_prof = load_json(
    "documents/vector_store_prof.json")  # Load vector store
document_data_vip = load_json("documents/doc_store_vip.json")
mapped_document_db_vip = load_json(
    "documents/vector_store_vip.json")  # Load vector store
document_data_our = load_json("documents/doc_store_ourconnect.json")
mapped_document_db_our = load_json(
    "documents/vector_store_ourconnect.json")  # Load vector store
document_data_duri = load_json("documents/doc_store_DURI.json")
mapped_document_db_duri = load_json(
    "documents/vector_store_DURI.json")  # Load vector store
# Function to handle search queries


def response(query, document_data=document_data,
             mapped_document_db=mapped_document_db):
    # Compute embeddings for the query
    query_embeddings = compute_embeddings(query, tokenizer, model)

    # Retrieve the top k scores based on the query embeddings
    sorted_scores = retrieve_top_k_scores(
        query_embeddings, mapped_document_db, top_k)

    # Get the top results
    top_results = retrieve_top_results(sorted_scores)

    # Retrieve the text of relevant chunks based on the top results
    relevant_text = retrieve_text(top_results, document_data)

    print(relevant_text)

    # Uncomment if you have an API key
    response = generate_llm_response(openai_model, query, relevant_text)
    # Safely extract the content, handling possible key errors
    content = response.content

    print(content)
    return content

# Function for professor database and response


def response_prof(query):
    return response(query, document_data_prof, mapped_document_db_prof)

# Function for OUR database and response


def response_our(query):
    return response(query, document_data_our, mapped_document_db_our)

# Function for VIP datatbase and response


def response_vip(query):
    return response(query, document_data_vip, mapped_document_db_vip)

# Function for VIP datatbase and response


def response_duri(query):
    return response(query, document_data_duri, mapped_document_db_duri)


if __name__ == "__main__":
    directory = [directory_path_duri]
    for i in directory:
        # creating document store with chunk id, doc_id, text
        documents = chunking(
            i,
            tokenizer,
            chunk_size,
            para_seperator,
            separator)

        # now embedding generation and mapping in database
        mapped_document_db = map_document_embeddings(
            documents, tokenizer, model)

        # saving json
        save_json(f'documents/doc_store_{i[11:]}.json', documents)
        save_json(f'documents/vector_store_{i[11:]}.json', mapped_document_db)

        # Retrieving most relavent data chunks
        query = "Which professors work in reinforcemnt learning?"
        query_embeddings = compute_embeddings(query, tokenizer, model)
        sorted_scores = retrieve_top_k_scores(
            query_embeddings, mapped_document_db, top_k)
        top_results = retrieve_top_results(sorted_scores)

        # reading json
        # document_data = read_json(f"documents/doc_store_{i[11:]}.json") #read
        # document store

        # #Retrieving text of relavent chunk embeddings
        # relavent_text = retrieve_text(top_results, document_data)

        # print(relavent_text)
        # print(relavent_text["text"])

        # Uncomment if you have api key
        # response = generate_llm_response(openai_model, query, relavent_text)
        # print(response)
