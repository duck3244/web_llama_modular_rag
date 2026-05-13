from huggingface_hub import snapshot_download

model_id = "jhgan/ko-sroberta-multitask"
path = snapshot_download(repo_id=model_id)
print(f"{model_id} → {path}")
