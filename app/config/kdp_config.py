# app/config/kdp_config.py

KDP_SETTINGS = {
    'book_dimensions': {
        'width': 8.5,
        'height': 11.0,
        'bleed': 0.125
    },
    'pricing': {
        'base_price': 9.99,
        'premium_addon': 2.00,
        'minimum_margin': 2.00
    },
    'categories': {
        'mandala': ['Games & Activities', 'Games & Activities / Coloring Books'],
        'nature': ['Art', 'Art / Techniques / Color'],
        'fantasy': ['Games & Activities', 'Games & Activities / Activity Books'],
        'pattern': ['Games & Activities', 'Games & Activities / Coloring Books']
    },
    'keywords': {
        'base': ['coloring book', 'adult coloring', 'stress relief'],
        'mandala': ['mandala', 'geometric', 'meditation'],
        'nature': ['flowers', 'gardens', 'wildlife'],
        'fantasy': ['dragons', 'mythical creatures', 'fantasy art'],
        'pattern': ['patterns', 'abstract', 'decorative']
    }
}