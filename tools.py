from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# yfinance_news_tool.py
import yfinance as yf
# from newspaper import Article

import yfinance as yf
from langchain.tools import tool
from datetime import datetime, timedelta

def format_large_number(number):
    try:
        number = float(number)
        if number >= 1_000_000_000_000:
            return f"₹{number/1_000_000_000_000:.2f}T"
        elif number >= 1_000_000_000:
            return f"₹{number/1_000_000_000:.2f}B"
        elif number >= 1_000_000:
            return f"₹{number/1_000_000:.2f}M"
        else:
            return f"₹{number:,.2f}"
    except:
        return "N/A"


@tool
def get_stock_info(ticker: str) -> str:
    """
    Get detailed stock info for a given ticker symbol (e.g., AAPL, TSLA).
    Includes current stats, recent historical data, and trend.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Basic current stats
        name = info.get("longName", ticker)
        price = info.get("regularMarketPrice", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        eps = info.get("trailingEps", "N/A")

        # Get last 5 days of closing prices
        today = datetime.today()
        start_date = today - timedelta(days=7)
        history = stock.history(start=start_date.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))

        close_prices = history['Close'].dropna().tail(5)
        trend = "📉 Falling" if close_prices[-1] < close_prices[0] else "📈 Rising"

        price_trend = "\n".join([f"{date.strftime('%b %d')}: ${price:.2f}" for date, price in close_prices.items()])

        return (
            f"### 📊 {name} ({ticker.upper()})\n\n"
            f"**💵 Current Stats:**\n"
            f"- **Price:** ${price:.2f}\n"
            f"- **Market Cap:** {format_large_number(market_cap)}\n"
            f"- **P/E Ratio:** {pe_ratio}\n"
            f"- **EPS:** {eps}\n\n"
            f"**📈 Recent Closing Prices (Last 5 Days):**\n"
            f"{price_trend}\n\n"
            f"**📉 Trend Analysis:** {trend}\n"
        )

    except Exception as e:
        return f"❌ Failed to fetch data for {ticker}: {e}"


# # summarize_tool.py
# @tool
# def summarize_news_url(url: str) -> str:
#     """Download and summarize a news article from a URL."""
#     article = Article(url)
#     article.download()
#     article.parse()
#     article.nlp()

#     return (
#         f"📰 **{article.title}**\n"
#         f"**Authors**: {', '.join(article.authors)}\n"
#         f"**Summary**: {article.summary}"
#     )

# from langchain.tools import tool
# from langchain_community.tools import DuckDuckGoSearchRun

# @tool
# def search_stock(stock_ticker: str) -> str:
#     """
#     Search the web for stock-related and financial information using DuckDuckGo.
#     Useful for finding recent news, financials, company analysis, and market data
#     related to a given stock ticker (e.g., AAPL, TSLA).
#     """
#     try:
#         search = DuckDuckGoSearchRun()
#         query = f"{stock_ticker} company info, financials, earnings, latest news"
#         results = search.run(query)

#         if not results:
#             return f"🔍 No search results found for {stock_ticker}."

#         return f"🔎 Search results for **{stock_ticker}**:\n{results}"
    
#     except Exception as e:
#         return f"❌ Error while searching for {stock_ticker}: {e}"

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

@tool
def search_stock(stock_ticker: str) -> str:
    """
    Search Wikipedia for a given company or stock ticker.
    Returns a detailed explanation of the company.
    Tell thing like about past, recent major news and controversies.
    """
    # Wikipedia wrapper configuration
    wiki = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=800)
    )

    # Capitalize input to match Wikipedia titles (optional)
    query = stock_ticker.strip().title()

    # Run the search
    result = wiki.run(query)

    # Fallback if nothing found
    if not result or "may refer to" in result.lower():
        return f"Sorry, I couldn't find reliable information about '{stock_ticker}' on Wikipedia."
