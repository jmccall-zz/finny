# Default configuration file for IEX API requests
config = {
    'stock': {
        'DEFAULT': {
            'freshness': '7d',
        },
        # /stable/stock/{symbol}/company
        'company': {
            'freshness': '365d',
        },
        # /stable/stock/{symbol}/dividends/ytd
        'dividends/ytd': {
            'freshness': '60d',
        },
        # /stable/stock/{symbol}/quote/latestPrice
        'quote/latestPrice': {
            'freshness': '24h',
        },
    }
}
