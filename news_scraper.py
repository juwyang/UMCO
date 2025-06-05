import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.nasdaq.com/publishers/barchart"
MAX_PAGES = 5 # As requested, scrape up to 1000 pages

# Headers to mimic a browser visit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_page_content(page_number):
    """Fetches the HTML content of a specific page."""
    try:
        if page_number == 1:
            page_url = BASE_URL
        else:
            page_url = f"{BASE_URL}/page/{page_number}"
        
        print(f"Fetching list page: {page_url}")
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_url}: {e}")
        return None

def fetch_article_details(article_url):
    """Fetches and parses the summary and publication time from an individual article page."""
    try:
        print(f"Fetching details for: {article_url}")
        response = requests.get(article_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        article_soup = BeautifulSoup(response.text, 'html.parser')

        summary = "N/A"
        time_published = "N/A"

        # Extract summary from <meta name="description"> tag
        meta_description_tag = article_soup.find('meta', attrs={'name': 'description'})
        if meta_description_tag and meta_description_tag.get('content'):
            summary = meta_description_tag.get('content').strip()

        # Extract publication time from ld+json script
        ld_json_scripts = article_soup.find_all('script', type='application/ld+json')
        for script_tag in ld_json_scripts:
            try:
                json_data = json.loads(script_tag.string)
                # The data might be a single object or a list under "@graph"
                if '@graph' in json_data and isinstance(json_data['@graph'], list):
                    for item in json_data['@graph']:
                        if isinstance(item, dict) and item.get('@type') == 'NewsArticle' and 'datePublished' in item:
                            time_published = item['datePublished']
                            break # Found in @graph
                elif isinstance(json_data, dict) and json_data.get('@type') == 'NewsArticle' and 'datePublished' in json_data:
                    time_published = json_data['datePublished']
                    break # Found in single object
                if time_published != "N/A":
                    break # Stop if found
            except json.JSONDecodeError:
                print(f"Warning: Could not parse ld+json content from {article_url}")
            except Exception as e_json:
                print(f"Warning: Error processing ld+json from {article_url}: {e_json}")

        # Fallback for summary if meta description is not found or empty
        if summary == "N/A" or not summary:
            article_body = article_soup.find('div', class_=['article-body', 'body__content', 'article__content-container', 'prose'])
            if article_body:
                paragraphs = article_body.find_all('p', limit=2) # Get first two paragraphs
                summary_parts = [p.get_text(strip=True) for p in paragraphs]
                summary = " ".join(summary_parts)
            if not summary: # Further fallback
                main_content_tags = article_soup.find(['main', 'article', 'div.body'])
                if main_content_tags:
                    first_p_in_main = main_content_tags.find('p')
                    if first_p_in_main:
                        summary = first_p_in_main.get_text(strip=True)
        
        # Fallback for time if not found in ld+json
        if time_published == "N/A":
            time_meta_tag = article_soup.find('meta', property='article:published_time')
            if time_meta_tag and time_meta_tag.get('content'):
                time_published = time_meta_tag.get('content')
            else:
                time_div_tag = article_soup.find('div', class_=['article__timestamp', 'timestamp', 'date'])
                if time_div_tag:
                    time_published = time_div_tag.get_text(strip=True)
                else:
                    time_span_tag = article_soup.find('span', class_=['dateline', 'timestamp', 'article__date', 'posted-on'])
                    if time_span_tag:
                        time_published = time_span_tag.get_text(strip=True)

        return summary, time_published
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article details from {article_url}: {e}")
        return "N/A", "N/A"
    except Exception as e:
        print(f"Error parsing article details from {article_url}: {e}")
        return "N/A", "N/A"

def parse_articles_from_page(html_content):
    """Parses articles from the HTML content of a page."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    articles_data = []

    # --- IMPORTANT --- 
    # The selectors below are GUESSES. These will LIKELY NEED ADJUSTMENT
    # after inspecting the actual HTML structure of nasdaq.com/publishers/barchart.
    
    # Common pattern: articles are often list items or divs with a specific class
    # Example: <article class="news-item"> or <div class="story-card">
    article_elements = soup.find_all('div', class_='content-feed__card') # Placeholder selector
    if not article_elements:
        # Fallback: try another common pattern if the first fails
        article_elements = soup.find_all('li', class_='article-preview') # Another placeholder
    if not article_elements:
        # One more common pattern for news listings
        article_elements = soup.find_all('article')

    for article_el in article_elements:
        title = "N/A"
        url = "N/A"
        time_published = "N/A"
        summary = "N/A"

        # Title and URL are often within an <a> tag, possibly inside an <h2> or <h3>
        # Example: <a href="..."><h2>Title</h2></a>
        title_tag = article_el.find('a', class_='content-feed__card-title-link') # Placeholder
        if title_tag and title_tag.get_text(strip=True):
            title = title_tag.get_text(strip=True)
            url_candidate = title_tag.get('href')
            if url_candidate:
                # Ensure URL is absolute
                if url_candidate.startswith('/'):
                    url = f"https://www.nasdaq.com{url_candidate}"
                else:
                    url = url_candidate
        else: # Fallback for title
            h_tag = article_el.find(['h2', 'h3', 'h4']) # Common heading tags
            if h_tag and h_tag.find('a'):
                title = h_tag.find('a').get_text(strip=True)
                url_candidate = h_tag.find('a').get('href')
                if url_candidate:
                    if url_candidate.startswith('/'):
                        url = f"https://www.nasdaq.com{url_candidate}"
                    else:
                        url = url_candidate
            elif h_tag:
                 title = h_tag.get_text(strip=True)

        # Time published might be in a <time> tag or a <span> with a specific class
        # Example: <time datetime="2023-10-26T10:00:00Z">October 26, 2023</time>
        # Example: <span class="timestamp">...</span>
        time_tag = article_el.find('time', class_='content-feed__card-timestamp') # Placeholder
        if time_tag and time_tag.get_text(strip=True):
            time_published = time_tag.get_text(strip=True)
        else: # Fallback for time
            span_time = article_el.find('span', class_='timestamp') # Placeholder
            if span_time:
                time_published = span_time.get_text(strip=True)

        # For summary and time_published, we will fetch them from the article's page
        # So, we initialize them as N/A here and populate later if URL is valid.
        
        if title != "N/A" and url != "N/A":
            articles_data.append({
                'title': title,
                'url': url,
                'time_published': "N/A", # Will be fetched later
                'summary': "N/A" # Will be fetched later
            })

    return articles_data

def main():
    all_articles = []
    print(f"Starting to scrape news from {BASE_URL}...")

    for page_num in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page_num}...")
        html = fetch_page_content(page_num)
        
        if not html:
            print(f"Failed to fetch page {page_num} or page is empty. Moving to next.")
            # Optional: break here if pages are sequential and one fails, 
            # or continue if gaps are expected.
            # For now, let's try to continue for a few more pages before giving up
            if page_num > 5 and not any(all_articles):
                 print("Failed to fetch initial pages, stopping.")
                 break
            time.sleep(1) # Wait a bit before trying next page
            continue

        articles_on_page = parse_articles_from_page(html)
        
        if not articles_on_page and page_num > 1:
            # If a page after the first one returns no articles, 
            # it might mean we've reached the end of available pages.
            print(f"No articles found on page {page_num}. Assuming end of content.")
            break 
        
        for article_info in articles_on_page:
            if article_info['url'] != "N/A":
                # Fetch summary and potentially a more precise time from the article's own page
                summary_detail, time_published_detail = fetch_article_details(article_info['url'])
                article_info['summary'] = summary_detail
                
                # Update time_published if the detail page provides a more precise one 
                # or if it wasn't found on the list page.
                if time_published_detail != "N/A":
                    # Prefer detail page time if it's not 'N/A' and either list page time was 'N/A' or list page time is relative (e.g., 'X hours ago')
                    if article_info['time_published'] == "N/A" or "ago" in article_info['time_published'].lower() or not any(char.isdigit() for char in article_info['time_published']):
                        article_info['time_published'] = time_published_detail
                    # If both are available and list page time is not relative, keep list page time (often more consistent for listings)
                    # This logic can be refined based on observed data quality from both sources.

                all_articles.append(article_info)
                print(f"  Processed: {article_info['title']}; Time: {article_info['time_published']}; Summary: {article_info['summary'][:50]}...")
                time.sleep(0.5) # Small delay between fetching individual articles
            else:
                # If URL is N/A for some reason, add it with N/A for details
                all_articles.append(article_info)

        print(f"Processed {len(articles_on_page)} article links from page {page_num}. Total articles with details: {len(all_articles)}")
        
        # Respectful delay between requests for list pages
        time.sleep(1) # 1-second delay

    print(f"\nScraping finished. Total articles found: {len(all_articles)}")

    # Output the data as JSON
    if all_articles:
        output_file = 'nasdaq_barchart_news.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {output_file}")
    else:
        print("No articles were scraped.")

if __name__ == "__main__":
    main()