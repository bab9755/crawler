import requests
from bs4 import BeautifulSoup
import urllib.parse
from robots_txt import fetch_disallowed_paths, fetch_robots_txt


def crawl(url: str):

    #we need to first normalize the url
    disallowed_paths = []
    url_robots_txt = fetch_robots_txt(url) # get the robots_txt file
    
    if url_robots_txt: #if a robots.txt file is found
        disallowed_paths = fetch_disallowed_paths(url_robots_txt) #get all the paths that are disallowed from the rul

    parsed_url = urllib.parse.urlparse(url) # parse the url


    #get the hostname and the path
    url_hostname = parsed_url.hostname
    url_path = parsed_url.path
    response = requests.get(url) #fetch the url 

    print(f"The response is: {response} and it's type is {type(response)}")

    if response.status_code != 200:
        return f"Error fetching the URL {url}"

    url_text = response.text
    soup = BeautifulSoup(response.text, 'html.parser') # get the html from the url

    url_title = soup.find('title').text #get the title of the page
    a_tags = soup.find_all('a') #get all the links from the page
    url_all_links = [tag.get('href') for tag in a_tags]
    
    # print(f"The title for {url} is {url_title}")
    # print(f"The text for {url} is {url_text}")
    print(f"The urls found inside {url} are: \n")
    for i in range(len(url_all_links)): #print all links within the 
        # print(f"{link}\n")

        if url_all_links[i].startswith('/'): #if the given link is a relative link
            url_all_links[i]




crawl('https://github.com/ashishpatel26/500-AI-Machine-learning-Deep-learning-Computer-vision-NLP-Projects-with-code?tab=readme-ov-file')
    



