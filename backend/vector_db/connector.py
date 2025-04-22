from pinecone import Pinecone 
import numpy as np 

import logging 
import os 
from typing import List, Dict, Any, Optional

from app.config import settings


logger = logging.getLogger(__name__)

class PineconeClient: 
    """client for pinecone"""
    
    def __init__(self):
        self.pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)