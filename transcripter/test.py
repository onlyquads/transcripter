import torch
print("CUDA available:", torch.cuda.is_available())  # Should be True
print("Device name:", torch.cuda.get_device_name(0))  # Should be RTX 2080 Ti
print("PyTorch version:", torch.__version__)
print("CUDA version:", torch.version.cuda)  # Should match your installed CUDA