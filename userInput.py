from datetime import datetime
import logging
import requests

class UserCancelledOperation(Exception):
    """Exception raised when a user cancels an input operation."""

def getChartType():
    print("\nChart Types:")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    chart_type_input = input("\nEnter the chart type you want (1, 2): ")

    while chart_type_input not in ['1', '2']:
        print("\nError: Invalid selection. Please choose 1 for Bar or 2 for Line.")
        chart_type_input = input("\nEnter your choice (1, 2): ")
    
    return 'bar' if chart_type_input == '1' else 'line'

def parseDate(date_string):
    #arse a string into a datetime object
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        print("\nError: Invalid date format. Please use YYYY-MM-DD.")
        return None

def getValidDate(prompt):
    #prompt the user to enter a date until a valid date is provided
    while True:
        try:
            date_input = input(prompt)
            date = parseDate(date_input)
            if date:
                return date
        except KeyboardInterrupt:
            logging.warning("\nUser cancelled operation.")
            raise UserCancelledOperation()

def getStartDate():
    #prompt user for a valid start date.
    # logging.info("Please enter the start date.")
    return getValidDate("\nEnter the start date (YYYY-MM-DD): ")

def getEndDate(startDate):
    #prompt user for a valid end date, ensuring it's not before the start date.
    endDate = getValidDate("Enter the end date (YYYY-MM-DD): ")
    while endDate < startDate:
        print("\nError: End date cannot be before the start date. Please enter a valid end date.")
        endDate = getValidDate("\nEnter the end date (YYYY-MM-DD): ")
    return endDate

def getStockSymbol():
    while True:
        symbol = input("\nEnter the stock symbol you are looking for: ").strip().upper()
        # Check if the symbol is 5 characters
        if not symbol.isalpha() or len(symbol) > 5:
            print("\nError: Invalid stock symbol. Please enter a valid symbol consisting of up to 5 uppercase alphabetic characters.")
        else:
            
            apikey = "V6BVQP0SPVJAVA6X"
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={apikey}"

            response = requests.get(url)
            data = response.json()

            # checks to see if symbol exists in api data
            if "bestMatches" in data:
                matches = [entry["1. symbol"] for entry in data["bestMatches"]]
                if symbol in matches:
                    return symbol
                else:
                    print(f"\nError: No matching stock symbol found for '{symbol}'. Please try again or enter a different symbol.")
            # temporary for error checking (e.g. 25 daily max requests reached)
            logging.error("API Response Content: %s", response.content)