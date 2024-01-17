#!/usr/bin/env python3

__author__ = "Leona Gottfried"
__version__ = "0.1.0"
__license__ = "MIT"

import json
import logging
from pathlib import Path

# from bertopic import BERTopic
# from glassplitter import Tokenizer
from arxiv_dataset import ArXiVDataset
from pdf_extract import PdfDocument

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

for line in Path("sample/arxiv_sample.json").read_text().splitlines():
    logger.debug(line)
    paper = json.loads(line)

    object = {
        "id": paper["id"],
        "title": paper["title"],
        "date": paper["update_date"],
        "text": PdfDocument(ArXiVDataset.get(paper["id"])).poppler_extract_text(),
        "topics" : {"1" : 0.46, "2": 0.111} #TODO(leogott): implementation
    }

    print(object)

# { "topics" : {"id":"1", "top 5": ["bag", "image", "cup"] }}
