import requests
import logging

def getStockData(symbol, timeSeriesFunction, apikey, output_size="full"):
    # Add outputsize parameter for both intraday and other series
    base_url = "https://www.alphavantage.co/query"
    if "TIME_SERIES_INTRADAY" in timeSeriesFunction:
        # For intraday, include interval from the function
        url = f"{base_url}?function={timeSeriesFunction}&apikey={apikey}&outputsize=full"
    else:
        # For daily, weekly, and monthly, no interval needed
        url = f"{base_url}?function={timeSeriesFunction}&symbol={symbol}&apikey={apikey}&outputsize=full"

    logging.info(f"Fetching stock data for: {symbol} using URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        # Look for the relevant time series data in the response
        time_series_key = next((key for key in data if "Time Series" in key), None)
        if not time_series_key:
            logging.error("Time Series data not found in API response.")
            return None

        # Process and return the time series data
        return {date: {metric: float(value) for metric, value in metrics.items()}
                for date, metrics in data[time_series_key].items()}
    except requests.RequestException as e:
        logging.error(f"HTTP request error: {e}")
    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")

    return None