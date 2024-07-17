# News Searcher

News Searcher is a Python application that allows users to search for news articles using the NewsAPI. It provides a command-line interface for searching news based on various criteria such as keywords, language, category, and date range.

## Features

- Search news articles by keyword, language, category, and date range
- Display search results with title, source, date, and URL
- Export search results to CSV file
- Interactive command-line interface

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/news-searcher.git
   cd news-searcher
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from [NewsAPI](https://newsapi.org/)

4. Create a `config.py` file in the project root and add your API key:
   ```python
   API_KEY = "your_api_key_here"
   ```

## Usage

Run the script using Python:

```
python news_searcher.py
```

Follow the prompts to enter your search criteria:
- Search term
- Language (en for English, es for Spanish)
- Category (business, entertainment, general, health, science, sports, technology)
- Date range
- Number of results

The application will display the search results and offer the option to export them to a CSV file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.