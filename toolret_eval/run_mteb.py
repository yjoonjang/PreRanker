from mteb import MTEB
import mteb
from sentence_transformers import CrossEncoder, SentenceTransformer

import torch

dual_encoder = SentenceTransformer("nvidia/NV-Embed-v2", trust_remote_code=True, model_kwargs={"torch_dtype": torch.bfloat16})

tasks = mteb.get_tasks(tasks=["ToolRetrieval"], languages=["eng"])
eval_splits = ["dev"]
evaluation = MTEB(tasks=tasks)

# Use NV-Embed-v2 for first stage retrieval
evaluation.run(
    dual_encoder,
    eval_splits=eval_splits,
    save_predictions=True, # save_predictions should be `True` to evaluate reranker models based on first stage retrieval
    output_folder="results/stage1",
    batch_size=1
)

# use reranker for second stage reranking
# cross_encoder_model_name = "BAAI/bge-reranker-v2-m3"
# cross_encoder_model_name = "jinaai/jina-reranker-v2-base-multilingual"
# cross_encoder_model_name = "Alibaba-NLP/gte-reranker-modernbert-base"
# cross_encoder_model_name = "Alibaba-NLP/gte-multilingual-reranker-base"
cross_encoder_model_name = "yjoonjang/preranker"

cross_encoder = CrossEncoder(cross_encoder_model_name, trust_remote_code=True, model_kwargs={"torch_dtype": torch.bfloat16})

evaluation.run(
    cross_encoder,
    eval_splits=eval_splits,
    top_k=100, # evaluate from top100 retrieved tools from first stage retrieval
    save_predictions=False,
    output_folder=f"results/stage2/{cross_encoder_model_name}",
    previous_results="results/stage1/ToolRetrieval_default_predictions.json",
    batch_size=8
)