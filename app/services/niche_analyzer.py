# app/services/niche_analyzer.py

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from typing import List, Dict

class NicheAnalyzer:
    def __init__(self):
        self.categories = [
            "Mandalas",
            "Adult Coloring",
            "Fantasy",
            "Nature",
            "Sacred Geometry"
        ]

    def get_amazon_bestsellers(self) -> List[Dict]:
        # Using selenium to avoid detection
        driver = webdriver.Chrome()
        bestsellers = []

        try:
            for category in self.categories:
                url = f"https://www.amazon.com/s?k=coloring+book+{category}"
                driver.get(url)

                products = driver.find_elements(By.CLASS_NAME, "s-result-item")
                for product in products[:10]:  # Top 10 per category
                    try:
                        title = product.find_element(By.CLASS_NAME, "a-text-normal").text
                        price = product.find_element(By.CLASS_NAME, "a-price").text
                        rating = product.find_element(By.CLASS_NAME, "a-icon-star-small").get_attribute("aria-label")

                        bestsellers.append({
                            "category": category,
                            "title": title,
                            "price": price,
                            "rating": rating
                        })
                    except Exception as e:
                        continue

        finally:
            driver.quit()

        return bestsellers

    def analyze_trends(self, data: List[Dict]) -> Dict:
        df = pd.DataFrame(data)

        analysis = {
            "top_categories": df.groupby("category")["rating"].mean().sort_values(ascending=False).to_dict(),
            "price_ranges": df.groupby("category")["price"].agg(["mean", "min", "max"]).to_dict(),
            "keyword_frequency": self._extract_keywords(df["title"].tolist())
        }

        return analysis

    def _extract_keywords(self, titles: List[str]) -> Dict:
        # Simple keyword frequency analysis
        keywords = {}
        stop_words = set(["the", "and", "for", "with", "book", "coloring"])

        for title in titles:
            words = title.lower().split()
            for word in words:
                if word not in stop_words:
                    keywords[word] = keywords.get(word, 0) + 1

        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:20])

# Created/Modified files:
# - data/market_analysis_{timestamp}.json