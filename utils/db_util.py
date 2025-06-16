

def decode_bytes_in_dict(obj):
    if isinstance(obj, dict):
        return {k: decode_bytes_in_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decode_bytes_in_dict(item) for item in obj]
    elif isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')  # 디코딩 실패 시 � 로 대체
    else:
        return obj