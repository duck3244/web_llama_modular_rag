from huggingface_hub import snapshot_download

model_id = "torchtorchkimtorch/Llama-3.2-Korean-GGACHI-1B-Instruct-v1"
path = snapshot_download(repo_id=model_id)
print(f"{model_id} → {path}")
