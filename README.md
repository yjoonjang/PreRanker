<h1 align="center">📊 Pre:Ranker - reranking tools beforehand</h1> 

## News
- 2025.04.09: [🤗 preranker-v1](https://huggingface.co/yjoonjang/preranker-v1), [MTEB-ToolRetrieval](https://github.com/yjoonjang/preranker?tab=readme-ov-file#MTEB-ToolRet) released!

## About Pre:Ranker
So many tools and functions to use? Try **Pre:Ranker** ! <br>
**Pre:Ranker** is designed to optimize the function calling process of modern LLMs by narrowing down the corpus of available tools based on a given query.

## Installation
```bash
pip install -r requirements.txt
```

## Exapmle Usage
```python
from sentence_transformers.cross_encoder import CrossEncoder

model = CrossEncoder('yjoonjang/preranker-v1')
model.eval()
pairs = [
    ["Is 'https://www.apple.com' available in the Wayback Machine on September 9, 2015?", "{'name': 'availability', 'description': 'Checks if a given URL is archived and currently accessible in the Wayback Machine.', 'parameters': {'url': {'description': 'The URL to check for availability in the Wayback Machine.', 'type': 'str', 'default': 'http://mashape.com'}, 'timestamp': {'description': \"The timestamp to look up in Wayback. If not specified, the most recent available capture is returned. The format of the timestamp is 1-14 digits (YYYYMMDDhhmmss). Defaults to '20090101'.\", 'type': 'str, optional', 'default': '20090101'}, 'callback': {'description': 'An optional callback to produce a JSONP response. Defaults to None.', 'type': 'str, optional', 'default': ''}}}"],
    ["Is 'https://www.apple.com' available in the Wayback Machine on September 9, 2015?", "{'name': 'top_grossing_mac_apps', 'description': 'Fetches a list of the top-grossing Mac apps from the App Store.', 'parameters': {'category': {'description': \"The category ID for the apps to be fetched. Defaults to '6016' (general category).\", 'type': 'str', 'default': '6016'}, 'country': {'description': \"The country code for the App Store. Defaults to 'us'.\", 'type': 'str', 'default': 'us'}, 'lang': {'description': \"The language code for the results. Defaults to 'en'.\", 'type': 'str', 'default': 'en'}, 'num': {'description': 'The number of results to return. Defaults to 100. Maximum allowed value is 200.', 'type': 'int', 'default': '100'}}}"],
    ["Is 'https://www.apple.com' available in the Wayback Machine on September 9, 2015?", "{'name': 'top_paid_mac_apps', 'description': 'Retrieves a list of the top paid Mac apps from the App Store.', 'parameters': {'category': {'description': \"Category of the apps to retrieve. Default is '6016'.\", 'type': 'str', 'default': '6016'}, 'country': {'description': \"Country code to filter the app results. Default is 'us'.\", 'type': 'str', 'default': 'us'}, 'lang': {'description': \"Language code for the results. Default is 'en'.\", 'type': 'str', 'default': 'en'}, 'num': {'description': 'Number of results to return. Default is 100. Maximum is 200.', 'type': 'int', 'default': '100'}}}"]
]

scores = model.predict(pairs)
print(scores) # [0.91427845 0.7625548  0.7656321]
```

---


## MTEB-ToolRet
Changed [ToolRet Benchmark](https://github.com/mangopy/tool-retrieval-benchmark) into BEIR format to make it MTEB compatible. check `make_toolret_to_beir_format.ipynb` for more details.

### Evaluation Code
```bash
cd toolret_eval
python run_mteb.py
```

### Evaluation Results

| Model Name | Model Parameter | Recall@10 | MAP@10 | MRR@10 | Precision@10 | NDCG@10 |
|--------|--------|-----------|--------|--------|--------------|---------|
| **[yjoonjang/preranker-v1](https://huggingface.co/yjoonjang/preranker-v1)** | 150M | **0.540** | **0.361** | **0.462** | **0.088** | **0.428** |
| [Alibaba-NLP/gte-reranker-modernbert-base](https://huggingface.co/Alibaba-NLP/gte-reranker-modernbert-base) | 150M | 0.524 | 0.356 | 0.454 | 0.086 | 0.422 |
| [jinaai/jina-reranker-v2-base-multilingual](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) | 278M | 0.502 | 0.331 | 0.414 | 0.083 | 0.395 |
| [Alibaba-NLP/gte-multilingual-reranker-base](https://huggingface.co/Alibaba-NLP/gte-multilingual-reranker-base) | 306M | 0.474 | 0.299 | 0.383 | 0.078 | 0.363 |
| [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) | 568M | 0.461 | 0.293 | 0.370 | 0.076 | 0.355 |

## Training Details
- preranker-v1 is a fine-tuned model based on [Alibaba-NLP/gte-reranker-modernbert-base](https://huggingface.co/Alibaba-NLP/gte-reranker-modernbert-base), via [sentence-transformers](https://sbert.net/)
- Training data will soon be released.

### Training Procedure
- loss: [ListNetLoss](https://sbert.net/docs/package_reference/cross_encoder/losses.html#listnetloss)
- batch size: 4
- learning rate: 2e-5
- epoch: 1

## License
- `apache-2.0`

## Citation
```bibtex
@misc{Pre:Ranker,
  publisher = {Youngjoon Jang, Seongtae Hong},
  year = {2025},
  url = {https://github.com/yjoonjang/preranker}
},
```
