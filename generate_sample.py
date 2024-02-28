#!/usr/bin/env python3

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import operator
from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd
from glassplitter import Tokenizer
from rich.logging import RichHandler
from sklearn import set_config
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import make_pipeline

from arxiv_dataset import fetch_arxiv_sample
from main import tokenize_only
from pdf_extract import PdfDocument, unbox_text
from utils import execution_time

## Logger

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(log_time_format="%X")],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

## Config

set_config(transform_output="pandas")
N_CLUSTERS = 5

## Data, Metadata

arxiv_sample = fetch_arxiv_sample(Path("sample/50_ids.txt"))
metadata = pd.DataFrame({
    "arxiv_id": arxiv_sample.ids,
    "title": arxiv_sample.titles,
    "date": arxiv_sample.dates,
})
corpus = arxiv_sample.data

## Tokenizer

tokenizer = Tokenizer(lang="en", clean=True, doc_type="pdf")

## Preprocessor

stop_words = ["", "the"]


def custom_analyzer(tokenizer):
    """Turn a pdf into a list of str tokens.

    Preprocessor and tokenizer in one.
    """

    def wrapped_custom_analyzer(pdf):
        # No sentence segmentation, assume each text-box contains exactly one sentence
        textboxes = PdfDocument(pdf).poppler_textboxes_flat()
        # TODO(leogott): insert preproc pipeline here
        sentences = unbox_text(textboxes)

        # TODO(leogott): String Transformation / str.lower

        tokens = reduce(operator.add, tokenize_only(tokenizer, sentences))

        # filter-out stop words
        return list(filter(lambda t: t not in stop_words, tokens))

    return wrapped_custom_analyzer


analyzer = custom_analyzer(tokenizer)
data = []
with execution_time() as t:
    for i, pdf in enumerate(corpus):
        logger.debug("Analyzing pdf %s", arxiv_sample.ids[i])
        try:
            data.append(analyzer(pdf))
        except:
            logger.exception(
            "An error occured while handling arxiv_id %s", arxiv_sample.ids[i]
        )
            raise
logger.info(f"Tokenized {len(data)=} PDFs in {t()}")

## Tfidf Vectorizer

tfidf_vectorizer = make_pipeline(
    CountVectorizer(
        # max_df=0.5, # Percentage of docs
        # min_df=3, # Absolute number of docs to contain feature (word)
        analyzer=lambda x: x,
        max_features=5000,
        # stop_words="english", # not used since analyzer in use
        # ngram_range=(1, 2),
    ),
    TfidfTransformer(sublinear_tf=True),
)
with execution_time() as t:
    tfidf_matrix = tfidf_vectorizer.fit_transform(data)
logger.info(f"Vectorization done in {t()}")

## KMeans Clustering

kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=0)
with execution_time() as t:
    kmeans.fit(tfidf_matrix)
logger.info(f"Clustering done in {t()}")

## Analysis: Clusters

_cluster_ids, cluster_sizes = np.unique(kmeans.labels_, return_counts=True)
logger.info(f"Number of elements assigned to each cluster: {cluster_sizes}")

original_space_centroids = kmeans.cluster_centers_
order_centroids = original_space_centroids.argsort()[:, ::-1]
terms = tfidf_vectorizer.get_feature_names_out()

for i in range(N_CLUSTERS):
    print(f"Cluster {i}: ", end="")
    for ind in order_centroids[i, :10]:
        print(f"'{terms[ind]}' ", end="")
    print()

# { "topics" : {"id":"1", "top 5": ["bag", "image", "cup"] }}
topics = {"kmeans": [{"cluster": str(i), "size": cluster_sizes[i], "top 5": [terms[tid] for tid in order_centroids[i, :5]]} for i in range(N_CLUSTERS)]}


## Analysis: Documents

kmeans_pipeline = make_pipeline(tfidf_vectorizer, kmeans)

cluster_distances: pd.DataFrame = kmeans_pipeline.transform(data)
# cluster_distances = cluster_distances.assign(cluster=kmeans_pipeline.predict(data))
cluster_distances = cluster_distances.assign(cluster=kmeans.labels_)
cluster_metadata = cluster_distances.join(metadata)
print(cluster_metadata)
