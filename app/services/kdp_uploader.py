# app/services/kdp_uploader.py

import os
import json
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyPDF2 import PdfMerger
from PIL import Image
import requests
from dotenv import load_dotenv

load_dotenv()

class KDPUploader:
    def __init__(self):
        self.kdp_email = os.getenv('KDP_EMAIL')
        self.kdp_password = os.getenv('KDP_PASSWORD')
        self.base_url = "https://kdp.amazon.com"
        self.driver = None
        
    def upload_batch(self, designs: List[Dict]) -> List[Dict]:
        """
        Upload multiple books to KDP
        """
        results = []
        self.driver = webdriver.Chrome()  # or use undetected_chromedriver
        
        try:
            self._login()
            
            for book_designs in self._group_designs_by_niche(designs):
                try:
                    # Prepare book files
                    book_data = self._prepare_book_files(book_designs)
                    
                    # Upload to KDP
                    result = self._upload_single_book(book_data)
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'niche': book_designs[0].get('niche'),
                        'status': 'failed',
                        'error': str(e)
                    })
                    
        finally:
            if self.driver:
                self.driver.quit()
                
        return results

    def _prepare_book_files(self, designs: List[Dict]) -> Dict:
        """
        Prepare all necessary files for KDP upload
        """
        niche = designs[0].get('niche', 'General')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        book_id = f"{niche}_{timestamp}"
        
        # Create output directory
        output_dir = os.path.join('output', 'kdp_books', book_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Prepare interior PDF
        interior_pdf = self._create_interior_pdf(designs, output_dir)
        
        # 2. Generate cover
        cover_pdf = self._create_cover(designs[0], output_dir)
        
        # 3. Prepare metadata
        metadata = self._generate_metadata(designs[0])
        
        return {
            'book_id': book_id,
            'interior_pdf': interior_pdf,
            'cover_pdf': cover_pdf,
            'metadata': metadata,
            'niche': niche
        }

    def _create_interior_pdf(self, designs: List[Dict], output_dir: str) -> str:
        """
        Create interior PDF with coloring pages