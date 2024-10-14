import kagglehub

# Download latest version
path = kagglehub.dataset_download("puneetbhaya/online-retail")

print("Path to dataset files:", path)