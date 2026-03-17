import ccxt

# ✅ BYBIT (PH OK) + KUCOIN (PH OK)
exchanges = [
    {'name': 'bybit', 'symbol': 'BTC/USDT'},
    {'name': 'kucoin', 'symbol': 'BTC-USDT'}, 
    {'name': 'okx', 'symbol': 'BTC/USDT'}
]

for ex in exchanges:
    try:
        exchange = getattr(ccxt, ex['name'])()
        ticker = exchange.fetch_ticker(ex['symbol'])
        print(f"✅ {ex['name'].upper()}: ${ticker['last']:.0f} ({ticker['percentage']:.2f}%)")
    except Exception as e:
        print(f"❌ {ex['name'].upper()}: {str(e)[:50]}")
