import psutil

# =========================================
# RAM INFORMATION
# =========================================

def capture_memory_info():
    memory = psutil.virtual_memory()

    memory_data = {
        "total_memory": memory.total,
        "used_memory": memory.used,
        "available_memory": memory.available
    }

    return memory_data
