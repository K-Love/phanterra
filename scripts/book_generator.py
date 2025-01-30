# scripts/book_generator.py
from ai_coloring_platform.generators import MandalaGenerator
from app.services import KDPUploader

def generate_complete_book(theme: str, pages: int = 50):
    generator = MandalaGenerator()
    uploader = KDPUploader()

    designs = [generator.generate() for _ in range(pages)]
    book_package = prepare_book(designs)
    uploader.upload(book_package)

# Created/Modified files:
# - output/books/{timestamp}_complete_book.pdf