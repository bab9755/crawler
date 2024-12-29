import requests
from bs4 import BeautifulSoup


def craw(url: str):


    response = requests.get(url) #fetch the url 

    if response.status.code != 200:
        return f"Error fetching the URL {url}"


    soup = BeautifulSoup(response.text(), 'html.parser') # get the html from the url


    url_title = soup.find('title') #get the title of the page
    all_links = soup.find_all('a') #get all the links from the page
    
    print(f"The urls found inside {url} are: \n")
    for link in all_links: #print all links within the 
        print(f"{link}\n")
