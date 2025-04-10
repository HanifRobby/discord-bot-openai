import logging
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(name="discord_bot"):
    """
    Konfigurasi dan setup logger
    
    Args:
        name: Nama logger
        
    Returns:
        Logger object yang telah dikonfigurasi
    """
    # Buat logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Format logging
    log_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    
    # Buat direktori logs jika belum ada
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # File handler dengan rotasi harian
    file_handler = TimedRotatingFileHandler(
        log_dir / f"{name}.log", 
        when="midnight",
        interval=1,
        backupCount=30  # Simpan log 30 hari terakhir
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)
    
    # Tambahkan handlers ke logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger