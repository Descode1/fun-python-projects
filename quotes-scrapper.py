import bs4, requests

base_url = 'https://quotes.toscrape.com'
page_url = '/page/1'

with open("quotes.txt", 'w', encoding='utf-8') as textObj:
    while page_url:
        
        res = requests.get(base_url + page_url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        quotes = soup.select('.quote')

        for q in quotes:
            text = q.find('span', class_='text').get_text()
            author = q.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in q.find_all('a', class_='tag')]
            textObj.write(f"Quote: {text}\n")
            textObj.write(f"Author: {author}\n")
            textObj.write(f"Tags: {', '.join(tags)}\n")
            textObj.write("-" * 50 + "\n")
        
        next_btn = soup.select_one("li.next a")
        if next_btn:
            page_url = next_btn['href']
        else:
            page_url = None
  