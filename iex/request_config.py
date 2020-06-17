# Default configuration file for IEX API requests
config = {
    'DEFAULT': {
        'freshness': '7d',
    },

    'stable/stock/SYMBOL/quote/latestPrice': {
        'freshness': '24h',
    },

    'stable/stock/SYMBOL/company': {
        'freshness': '365d',
    }
}
