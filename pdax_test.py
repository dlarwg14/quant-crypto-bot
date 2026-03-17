import requests
pdax_url = "https://api.pdex.ph/v1/market/tickers"
response = requests.get(pdax_url)
print(response.json())
