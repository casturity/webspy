import requests
import hashlib
import sqlite3
from bs4 import BeautifulSoup, Comment

def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove extra whitespaces
    content = ' '.join(soup.stripped_strings)

    return content

def hash_content(content):
    hasher = hashlib.sha256()
    hasher.update(content.encode('utf-8'))
    return hasher.hexdigest()

def store_hash(conn, url, hash_value):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO website_hashes (url, hash) VALUES (?, ?)", (url, hash_value))
    conn.commit()

def get_stored_hash(conn, url):
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM website_hashes WHERE url = ?", (url,))
    result = cursor.fetchone()
    return result[0] if result else None

def print_menu():
    print("""
    Options:
    1. List current URLs being tracked
    2. Enter a new URL to monitor
    3. Remove URL from tracked list
    4. Rerun all tracked websites for changes
    5. Quit
    """)

def check_website_changes(conn, url):
    try:
        current_html_content = get_html_content(url)
        current_hash = hash_content(current_html_content)

        stored_hash = get_stored_hash(conn, url)

        if stored_hash is None:
            print(f'This is the first run for {url}. Storing the hash of the current content.')
            store_hash(conn, url, current_hash)
        elif current_hash == stored_hash:
            print(f'No changes detected on {url} since the last run.')
        else:
            print(f'Changes detected on {url} since the last run.')
            store_hash(conn, url, current_hash)
    except requests.exceptions.RequestException:
        print('Error checking URL: ' + url)

def main():
    print(r"""
 __          ________ ____   _____ _______     __
 \ \        / /  ____|  _ \ / ____|  __ \ \   / /
  \ \  /\  / /| |__  | |_) | (___ | |__) \ \_/ / 
   \ \/  \/ / |  __| |  _ < \___ \|  ___/ \   /  
    \  /\  /  | |____| |_) |____) | |      | |   
     \/  \/   |______|____/|_____/|_|      |_|   
                                                 
    
    Welcome to WebSpy - a simple webpage change detector
    Author: @casturity
    Website: https://casturity.com
    """)

    conn = sqlite3.connect('website_hashes.db')
    conn.execute('CREATE TABLE IF NOT EXISTS website_hashes (url TEXT PRIMARY KEY, hash TEXT)')

    while True:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM website_hashes")
        urls = [item[0] for item in cursor.fetchall()]

        print_menu()
        option = input('Please select an option (1-5): ')
        
        if option == '5':
            break
        elif option == '1':
            if urls:
                print("Currently tracked URLs:")
                for i, url in enumerate(urls, start=1):
                    print(f'{i}. {url}')
                input('Press any key to go back to the menu.')
            else:
                print("No URLs are currently being tracked.")
        elif option == '2':
            url = input('Enter the URL of the website you want to monitor (or "b" to go back): ')
            if url.lower() == 'b' or url.strip() == '':
                continue
            check_website_changes(conn, url)
        elif option == '3':
            if urls:
                print("Currently tracked URLs:")
                for i, url in enumerate(urls, start=1):
                    print(f'{i}. {url}')
                index = input('Enter the index of the website you want to stop tracking (or "b" to go back): ')
                if index.lower() == 'b' or index.strip() == '':
                    continue
                try:
                    index = int(index) - 1
                except ValueError:
                    print('Invalid index. Please select a valid index.')
                    continue
                if 0 <= index < len(urls):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM website_hashes WHERE url=?", (urls[index],))
                    conn.commit()
                    print(f'{urls[index]} has been removed from the tracked list.')
                else:
                    print('Invalid index. Please select a valid index.')
            else:
                print("No URLs are currently being tracked.")
        elif option == '4':
            for url in urls:
                check_website_changes(conn, url)
            input('Press any key to go back to the menu.')
        else:
            print('Invalid option. Please enter a number between 1 and 5.')

    conn.close()

if __name__ == '__main__':
    main()
