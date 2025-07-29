import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

def clean_german_text(text):
    """Normalize German special characters and clean whitespace"""
    if not text:
        return text
    # Normalize unicode (e.g., ä -> a)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Replace common German abbreviations
    replacements = {
        'str.': 'strasse',
        'Str.': 'Strasse',
        'wg.': 'wegen',
        'bzw.': 'beziehungsweise'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return ' '.join(text.split())

# Fetch the webpage with proper headers for German content
url = "https://www.wbg-schweiz.ch/information/wohnbaugenossenschaften_schweiz/mitglieder/genossenschaften"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'de, en-US;q=0.9, en;q=0.8'
}

try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Ensure proper encoding for German text
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = []
    accordion = soup.find('div', class_='accordion')
    
    if accordion:
        items = accordion.find_all(['h3', 'div'], recursive=False)
        
        current_name = None
        for item in items:
            if item.name == 'h3':
                current_name = clean_german_text(item.get_text(strip=True))
            elif item.name == 'div' and current_name:
                # Process address information
                address_lines = []
                link = None
                
                for content in item.contents:
                    if content.name == 'a':
                        link = content.get('href', '').strip()
                        if link.startswith('http://'):
                            link = link[7:]
                        elif link.startswith('https://'):
                            link = link[8:]
                        break
                    if content.string and content.string.strip():
                        address_lines.append(clean_german_text(content.string))
                
                address = ', '.join(address_lines)
                
                if current_name and (address or link):
                    data.append({
                        'Name (Name)': current_name,
                        'Adresse (Address)': address,
                        'Website (Webseite)': link if link else 'N/A'
                    })
                current_name = None
    
    # Create DataFrame with bilingual headers
    df = pd.DataFrame(data)
    
    # Save to CSV with UTF-8 encoding for German characters
    df.to_csv('wohnbaugenossenschaften_schweiz.csv', index=False, encoding='utf-8-sig')
    print("Daten erfolgreich gespeichert in 'wohnbaugenossenschaften_schweiz.csv'")
    
    # Print sample
    print("\nBeispieldaten:")
    print(df.head().to_string(index=False))
    
except requests.exceptions.RequestException as e:
    print(f"Fehler beim Abrufen der Webseite: {e}")
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")