import subprocess
import requests
from html.parser import HTMLParser
from colorama import init, Fore
from pyfiglet import Figlet
import os

def clear_screen(title=None):
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
        if title:
            print(f"\033]0;{title}\007", end='')

def print_ahmia_title():
    f = Figlet(font='standard')
    print(Fore.LIGHTCYAN_EX + f.renderText("BREAD  ENGINE") + Fore.RESET)

class AhmiaHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_title = None
        self.current_link = None
        self.current_onion_link = None
        self.in_result = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li' and ('class', 'result') in attrs:
            self.in_result = True
        elif self.in_result and tag == 'h4':
            self.current_title = ''
        elif self.in_result and tag == 'a':
            self.current_link = dict(attrs).get('href', '')
        elif self.in_result and tag == 'cite':
            self.current_onion_link = ''

    def handle_data(self, data):
        if self.current_title is not None:
            self.current_title += data.strip()
        elif self.current_onion_link is not None:
            self.current_onion_link += data.strip()

    def handle_endtag(self, tag):
        if tag == 'h4':
            self.in_result = False
            print(Fore.LIGHTYELLOW_EX + f"Title: {self.current_title}")
            print(f"Onion Link: {self.current_onion_link}")
            print(f"Direct Link: {self.current_link}" + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + f"=======================================================================================================")
            self.current_title = None
            self.current_link = None
            self.current_onion_link = None

def search_ahmia(query):
    base_url = "https://ahmia.fi/search/"
    search_url = f"{base_url}?q={query}"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            parser = AhmiaHTMLParser()
            parser.feed(response.text)
            input("\n\n\nPress Enter to search again.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        clear_screen("BREAD ENGINE")
        print(Fore.BLUE + f"================")
        print(Fore.BLUE + f"Created by Cr0mb")
        print(Fore.BLUE + f"================")
        print_ahmia_title()
        search_query = input(Fore.LIGHTYELLOW_EX + f"Enter your search query (type 'exit' to quit): ")
        if search_query.lower() == 'exit':
            break
        search_ahmia(search_query)
