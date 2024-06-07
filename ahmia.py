import subprocess, requests, os
from html.parser import HTMLParser
from colorama import init, Fore
from pyfiglet import Figlet

init(autoreset=True)

class AhmiaHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_title = None
        self.current_link = None
        self.in_result = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'li' and attrs.get('class') == 'result':
            self.in_result = True
        elif self.in_result:
            if tag == 'h4':
                self.current_title = ''
            elif tag == 'a':
                self.current_link = attrs.get('href', '')

    def handle_data(self, data):
        if self.current_title is not None:
            self.current_title += data.strip()

    def handle_endtag(self, tag):
        if tag == 'h4' and self.in_result:
            self.in_result = False
            if self.current_link and self.current_link.startswith('/search/redirect?'):
                start_idx = self.current_link.find('redirect_url=') + len('redirect_url=')
                onion_link = self.current_link[start_idx:]
                self.results.append((self.current_title, onion_link, self.current_link))
            self.current_title = self.current_link = None

def clear_screen(title=None):
    os.system('clear' if os.name == 'posix' else 'cls')
    if title and os.name != 'posix':
        print(f"\033]0;{title}\007", end='')

def print_ahmia_title():
    print(Fore.LIGHTCYAN_EX + Figlet(font='standard').renderText("BREAD ENGINE") + Fore.RESET)

def display_results(query, results, page, results_per_page=5):
    clear_screen("BREAD ENGINE")
    print_ahmia_title()
    if query:
        print(Fore.LIGHTYELLOW_EX + f"Searched: {query}")
    else:
        print(Fore.LIGHTYELLOW_EX + "No results found for the search.")
    print()
    start_index = page * results_per_page
    end_index = start_index + results_per_page
    for i, (title, onion_link, direct_link) in enumerate(results[start_index:end_index], start=start_index + 1):
        print(Fore.LIGHTGREEN_EX + f"Title {i}: {title}")
        print(Fore.LIGHTMAGENTA_EX + f"Onion Link: {onion_link}")
        print(Fore.LIGHTCYAN_EX + f"Direct Link: {direct_link}" + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "="*102)

def search_ahmia(query, history):
    base_url = "https://ahmia.fi/search/"
    search_url = f"{base_url}?q={query}"
    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            parser = AhmiaHTMLParser()
            parser.feed(response.text)
            history.append(query)  # Add query to history on successful search
            return parser.results
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    search_history = []  # List to store search history
    
    while True:
        clear_screen("BREAD ENGINE")
        print(Fore.BLUE + f"                    ================")
        print(Fore.BLUE + f"                    Created by Cr0mb")
        print(Fore.BLUE + f"                    ================")
        print_ahmia_title()

        # Display search history
        if search_history:
            print(Fore.LIGHTYELLOW_EX + "Search History:")
            for idx, item in enumerate(search_history, 1):
                print(f"{idx}. {item}")
        
        search_query = input(Fore.LIGHTYELLOW_EX + "Enter your search query (type 'exit' to quit): ").lower()
        if search_query == 'exit':
            break
        results = search_ahmia(search_query, search_history)
        if not results:
            continue
        
        current_page = 0
        results_per_page = 10

        while True:
            display_results(search_query, results, current_page, results_per_page)
            navigation = input(Fore.LIGHTYELLOW_EX + "Enter 'n' for next page, 'p' for previous page, 's' to search again, or 'exit' to quit: ").lower()
            if navigation == 'n':
                if (current_page + 1) * results_per_page < len(results):
                    current_page += 1
            elif navigation == 'p':
                if current_page > 0:
                    current_page -= 1
            elif navigation == 's':
                break
            elif navigation == 'exit':
                exit()
