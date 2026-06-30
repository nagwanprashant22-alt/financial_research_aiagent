import re
import yfinance as yf


COMMON_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "nvidia": "NVDA",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "meta": "META",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amd": "AMD",
    "netflix": "NFLX",
}


def get_ticker(query: str) -> str:
    query_lower = query.lower()

    for company, ticker in COMMON_TICKERS.items():
        if company in query_lower:
            return ticker

    possible_tickers = re.findall(r"\b[A-Z]{1,5}\b", query)

    if possible_tickers:
        return possible_tickers[0]

    try:
        search = yf.Search(query, max_results=1)
        quotes = search.quotes

        if quotes:
            return quotes[0]["symbol"]

    except Exception:
        pass

    return query.upper()


def get_two_tickers(query: str):
    query_lower = query.lower()
    found = []

    for company, ticker in COMMON_TICKERS.items():
        if company in query_lower and ticker not in found:
            found.append(ticker)

    possible_tickers = re.findall(r"\b[A-Z]{1,5}\b", query)

    for ticker in possible_tickers:
        if ticker not in found:
            found.append(ticker)

    if len(found) >= 2:
        return found[0], found[1]

    if len(found) == 1:
        return found[0], "MSFT"

    return "AAPL", "MSFT"