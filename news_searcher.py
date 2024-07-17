import requests
import sys
import csv
from datetime import datetime, timedelta
from config import API_KEY

BASE_URL = "https://newsapi.org/v2/everything"
TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"

CATEGORIES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

def check_api_key():
    params = {
        "apiKey": API_KEY,
        "q": "test",
        "language": "en",
        "pageSize": 1
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            print("API connection successful!")
            return True
        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your API key and try again.")
        else:
            print(f"Error: Unable to connect to the API. Status code: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to connect to the API. {str(e)}")
        return False

def search_news(term=None, language=None, category=None, from_date=None, to_date=None, num_results=5):
    """
    Perform a news search based on the provided filters.
    
    :param term: Search term (optional)
    :param language: Language code (optional)
    :param category: News category (optional)
    :param from_date: Start date for article search (optional)
    :param to_date: End date for article search (optional)
    :param num_results: Number of results to return (default: 5)
    :return: List of article dictionaries or None if error
    """

    # Determine which endpoint to use
    if category:
        url = TOP_HEADLINES_URL
    else:
        url = BASE_URL

    params = {
        "apiKey": API_KEY,
        "pageSize": num_results
    }

    if term:
        params["q"] = term
    if language:
        params["language"] = language
    if category:
        params["category"] = category
    if from_date:
        params["from"] = from_date.isoformat()
    if to_date:
        params["to"] = to_date.isoformat()
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            
            if not articles:
                print("No results found for the given parameters.")
                return
            
            print(f"\nTop {len(articles)} results:")
            if term:
                print(f"Search term: {term}")
            if language:
                print(f"Language: {language}")
            if category:
                print(f"Category: {category}")
            if from_date and to_date:
                print(f"Date range: {from_date.date()} to {to_date.date()}")
            print()
            
            for idx, article in enumerate(articles, 1):
                print(f"{idx}. {article['title']}")
                print(f"   Source: {article['source']['name']}")
                print(f"   Date: {article['publishedAt'][:10]}")
                print(f"   URL: {article['url']}")
                print()
            
            return articles
        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your API key and try again.")
        elif response.status_code == 429:
            print("Error: Too many requests. You've exceeded your API request limit.")
        else:
            print(f"Error: Unable to fetch news. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to connect to the API. {str(e)}")

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD or leave blank to skip.")

def main():
    if API_KEY == "your_api_key_here":
        print("Error: Please replace 'your_api_key_here' in config.py with your actual NewsAPI key.")
        return

    if not check_api_key():
        print("Exiting due to API connection issues.")
        return

    while True:
        print("\nNews Search")
        print("Enter search parameters (press Enter to skip):")
        
        term = input("Search term: ").strip()
        
        language = input("Language (en for English, es for Spanish): ").strip().lower()
        if language and language not in ['en', 'es']:
            print("Invalid language. Using default.")
            language = None
        
        print("Available categories:", ", ".join(CATEGORIES))
        category = input("Category: ").strip().lower()
        if category and category not in CATEGORIES:
            print("Invalid category. Ignoring category filter.")
            category = None
        
        from_date = get_date_input("From date (YYYY-MM-DD, optional): ")
        to_date = get_date_input("To date (YYYY-MM-DD, optional): ")
        
        if from_date and to_date and from_date > to_date:
            print("Error: From date must be before or equal to To date. Ignoring date filter.")
            from_date = to_date = None
        
        while True:
            try:
                num_results = input("Number of results (1-100, default 5): ").strip()
                if not num_results:
                    num_results = 5
                else:
                    num_results = int(num_results)
                if 1 <= num_results <= 100:
                    break
                else:
                    print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        articles = search_news(term, language, category, from_date, to_date, num_results)
        
        if articles:
            export_option = input("Do you want to export the results to CSV? (y/n): ").lower()
            if export_option == 'y':
                filename = input("Enter the filename for the CSV (default: news_results.csv): ").strip()
                if not filename:
                    filename = "news_results.csv"
                if not filename.endswith('.csv'):
                    filename += '.csv'
                export_to_csv(articles, filename)
        
        if input("Search again? (y/n): ").lower() != 'y':
            break

    print("Thank you for using the News Searcher!")

def export_to_csv(articles, filename):
    """
    Export the given articles to a CSV file.
    
    :param articles: List of article dictionaries
    :param filename: Name of the CSV file to create
    """
    if not articles:
        print("No articles to export.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Source", "Date", "URL"])
        writer.writeheader()
        for article in articles:
            writer.writerow({
                "Title": article['title'],
                "Source": article['source']['name'],
                "Date": article['publishedAt'][:10],
                "URL": article['url']
            })
    print(f"Results exported to {filename}")

if __name__ == "__main__":
    main()