import requests
from bs4 import BeautifulSoup
import re

def scrape_and_filter_rss():
    url = "https://sso.agc.gov.sg/What's-New/New-Legislation/RSS"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        cpf_entries = []
        finance_entries = []
        
        for item in items:
            description = item.description.get_text()
            if "Central Provident Fund" in description:
                title = item.title.get_text()
                link = item.link.get_text()
                pub_date = item.pubDate.get_text() if item.pubDate else "No date"
                
                # Clean up description by removing HTML tags
                clean_description = re.sub(r'<.*?>', '', description)
                clean_description = re.sub(r'<.*?>', '', clean_description)
                
                cpf_entries.append({
                    'title': title,
                    'link': link,
                    'date': pub_date,
                    'description': clean_description
                })
            
            # Check for finance-related terms
            finance_terms = ["accounting", "duties", "capital"]
            if any(term.lower() in description.lower() for term in finance_terms):
                title = item.title.get_text()
                link = item.link.get_text()
                pub_date = item.pubDate.get_text() if item.pubDate else "No date"
                
                clean_description = re.sub(r'<.*?>', '', description)
                clean_description = re.sub(r'<.*?>', '', clean_description)
                
                finance_entries.append({
                    'title': title,
                    'link': link,
                    'date': pub_date,
                    'description': clean_description
                })
        
        if cpf_entries:
            with open('cpf_legislation.md', 'w', encoding='utf-8') as md_file:
                md_file.write("# Central Provident Fund Related Legislation\n\n")
                for entry in cpf_entries:
                    md_file.write(f"## {entry['title']}\n")
                    md_file.write(f"**Published Date:** {entry['date']}\n\n")
                    md_file.write(f"{entry['description']}\n\n")
                    md_file.write(f"[Read more]({entry['link']})\n\n")
            print("Markdown file created: cpf_legislation.md")
        else:
            print("No entries found containing 'Central Provident Fund'")
            
        if finance_entries:
            with open('finance.md', 'w', encoding='utf-8') as md_file:
                md_file.write("# Finance Related Legislation\n\n")
                for entry in finance_entries:
                    md_file.write(f"## {entry['title']}\n")
                    md_file.write(f"**Published Date:** {entry['date']}\n\n")
                    md_file.write(f"{entry['description']}\n\n")
                    md_file.write(f"[Read more]({entry['link']})\n\n")
            print("Markdown file created: finance.md")
        else:
            print("No finance-related entries found")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")

if __name__ == "__main__":
    scrape_and_filter_rss()
