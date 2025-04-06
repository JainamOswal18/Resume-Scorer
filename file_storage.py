import os
import shutil
from fastapi import UploadFile
from fastapi.responses import FileResponse
from typing import Optional, Tuple
import uuid

# Create uploads directory if it doesn't exist
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile, filename: Optional[str] = None) -> Tuple[str, str]:
    """
    Save an uploaded file to local storage
    
    Args:
        upload_file: The uploaded file
        filename: Optional custom filename, if not provided a unique name will be generated
        
    Returns:
        Tuple of (file_path, file_url)
    """
    # Generate a unique filename if not provided
    if not filename:
        file_extension = os.path.splitext(upload_file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
    
    # Make sure the filename is safe
    safe_filename = os.path.basename(filename)
    
    # Create the file path
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
        
    # Generate a URL for the file (for local development it's a relative path)
    file_url = f"/uploads/{safe_filename}"
    
    return file_path, file_url

def get_file_path(file_url: str) -> str:
    """
    Convert a file URL to a local file path
    
    Args:
        file_url: The file URL (e.g., /uploads/file.pdf)
        
    Returns:
        The local file path
    """
    filename = os.path.basename(file_url)
    return os.path.join(UPLOAD_DIR, filename)

def file_exists(file_url: str) -> bool:
    """
    Check if a file exists in the local storage
    
    Args:
        file_url: The file URL
        
    Returns:
        True if the file exists, False otherwise
    """
    file_path = get_file_path(file_url)
    return os.path.exists(file_path) and os.path.isfile(file_path)

def serve_file(file_url: str) -> Optional[FileResponse]:
    """
    Serve a file from local storage
    
    Args:
        file_url: The file URL
        
    Returns:
        FileResponse if the file exists, None otherwise
    """
    file_path = get_file_path(file_url)
    if file_exists(file_url):
        return FileResponse(file_path)
    return None

def delete_file(file_url: str) -> bool:
    """
    Delete a file from local storage
    
    Args:
        file_url: The file URL
        
    Returns:
        True if the file was deleted, False otherwise
    """
    file_path = get_file_path(file_url)
    if file_exists(file_url):
        os.remove(file_path)
        return True
    return False 