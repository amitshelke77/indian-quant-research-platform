from backend.services.market_data_service import MarketDataService

service = MarketDataService()

data = service.download_symbol("RELIANCE")

print("Columns:")
print(data.columns.tolist())

print("\nRows:")
print(len(data))