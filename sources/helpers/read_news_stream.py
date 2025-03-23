
def read_news_stream(file_path):
    """Generator for streaming and processing news articles."""
    current_news = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # If line is not empty, add to current news
                current_news.append(line)
            elif current_news:  # If empty line and there's accumulated news
                yield " ".join(current_news)
                current_news = []
        # Yield the last news item if it exists
        if current_news:
            yield " ".join(current_news)