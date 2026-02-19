import requests
import time

BASE_URL = "https://api.coingecko.com/api/v3"

def get_price(coin_id, vs_currency="usd"):
    url = f"{BASE_URL}/simple/price"
    params = {"ids": coin_id, "vs_currencies": vs_currency}
    response = requests.get(url, params=params)
    return response.json()

def main():
    print("📊 Crypto Price Monitor (CoinGecko Free API)")
    coin = input("Enter coin (example: bitcoin, ethereum): ").lower()

    while True:
        try:
            data = get_price(coin)
            price = data.get(coin, {}).get("usd", "N/A")
            print(f"{coin.upper()} price: ${price}")
            time.sleep(5)  # refresh every 5 sec
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print("Error:", e)
            break

if __name__ == "__main__":
    main()
