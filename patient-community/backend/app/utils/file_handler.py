import os
import uuid
from fastapi import UploadFile
from ..config import settings

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'}

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_file(upload_file: UploadFile) -> str:
    """保存上传的文件并返回文件路径"""
    if not allowed_file(upload_file.filename):
        raise ValueError("不支持的文件类型")
    
    # 生成唯一文件名
    file_ext = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # 确保上传目录存在
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        content = upload_file.file.read()
        buffer.write(content)
    
    return file_path

def delete_file(file_path: str) -> bool:
    """删除文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False
