# Selecting a sample of papers to process

In order to generate a sample, we agreed to arbitrarily choose 50 preprints on arxiv.

Therefore I downloaded the arxiv-metadata-oai-snapshot json from [kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv/data) (Version 162)
and truncated the file to the first 50 entries.

`head -n 50 arxiv-metadata-oai-snapshot.json > arxiv_sample.json`

The original metadata file is approaching 4 Gigabytes in size, and ordered by arxiv-id.

Each line is a valid json object, containing the metadata of one submission.

# Generating the Sample

https://www.kaggle.com/code/maartengr/topic-modeling-arxiv-abstract-with-bertopic/notebook
https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html
