from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

def read_questions(directory, file_name="all-questions.md"):
    question_file = f"output/{directory}/{file_name}"
    questions = []
    with open(question_file, 'r') as qf:
        questions = qf.readlines()
        print(f"Read {len(questions)} questions from {question_file}.")
    return questions

def cluster_questions(questions, cluster_count):
    model = SentenceTransformer("BAAI/bge-m3")
    print("Loaded model. Encoding questions...")
    embeddings = model.encode(questions)
    print("Completed encoding questions. Clustering...")
    kmeans = KMeans(n_clusters=cluster_count, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    print("Completed clustering...")
    return (embeddings, labels, kmeans)

def find_cluster_centres(cluster_count, embeddings, labels, kmeans, questions):
    representatives = []
    for cluster_id in range(cluster_count):
        idxs = [i for i, label in enumerate(labels) if label == cluster_id]
        cluster_embeddings = [embeddings[i] for i in idxs]
        sims = cosine_similarity([kmeans.cluster_centers_[cluster_id]], cluster_embeddings)
        central_idx = idxs[np.argmax(sims)]
        representatives.append((cluster_id, questions[central_idx]))
    return representatives

def find_representative_questions(directory, cluster_count, file_name="all-questions.md"):
    questions = read_questions(directory, file_name)
    (embeddings, labels, kmeans) = cluster_questions(questions, cluster_count)
    representatives = find_cluster_centres(cluster_count, embeddings, labels, kmeans, questions)
    return representatives

def print_representative_questions(representatives):
    for cluster_id, question in representatives:
        fixed_question = question.encode('unicode_escape').decode()
        print(f"Cluster {cluster_id}: {fixed_question}")

if __name__ == "__main__":
    print("Inside main")
    if len(sys.argv) < 3:
        print("Usage: python similar_questions.py <directory_with_questions> <cluster_count>")
        sys.exit(-1)
    file_name = "all-questions.md"
    if (len(sys.argv) == 4):
        file_name = sys.argv[3]
    representatives = find_representative_questions(sys.argv[1], int(sys.argv[2]), file_name)
    print_representative_questions(representatives)