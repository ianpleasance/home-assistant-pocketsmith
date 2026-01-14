"""Constants for the PocketSmith integration."""

DOMAIN = "pocketsmith"
API_BASE_URL = "https://api.pocketsmith.com/v2"

# Configuration
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 5  # minutes

# Currency symbol mapping
CURRENCY_SYMBOLS = {
    "AED": "د.إ",  # UAE Dirham
    "AUD": "A$",   # Australian Dollar
    "BGN": "лв",   # Bulgarian Lev
    "BRL": "R$",   # Brazilian Real
    "CAD": "C$",   # Canadian Dollar
    "CHF": "Fr",   # Swiss Franc
    "CNY": "¥",    # Chinese Yuan
    "CZK": "Kč",   # Czech Koruna
    "DKK": "kr",   # Danish Krone
    "EUR": "€",    # Euro
    "GBP": "£",    # British Pound
    "HKD": "HK$",  # Hong Kong Dollar
    "HUF": "Ft",   # Hungarian Forint
    "IDR": "Rp",   # Indonesian Rupiah
    "ILS": "₪",    # Israeli Shekel
    "INR": "₹",    # Indian Rupee
    "JPY": "¥",    # Japanese Yen
    "KRW": "₩",    # South Korean Won
    "MXN": "Mex$", # Mexican Peso
    "MYR": "RM",   # Malaysian Ringgit
    "NOK": "kr",   # Norwegian Krone
    "NZD": "NZ$",  # New Zealand Dollar
    "PHP": "₱",    # Philippine Peso
    "PLN": "zł",   # Polish Zloty
    "RON": "lei",  # Romanian Leu
    "RUB": "₽",    # Russian Ruble
    "SEK": "kr",   # Swedish Krona
    "SGD": "S$",   # Singapore Dollar
    "THB": "฿",    # Thai Baht
    "TRY": "₺",    # Turkish Lira
    "USD": "$",    # US Dollar
    "ZAR": "R",    # South African Rand
}
