import requests
from bs4 import BeautifulSoup
import urllib.parse
from robots_txt import fetch_disallowed_paths, fetch_robots_txt
from fnmatch import fnmatch


def crawl(url: str):

    #we need to first normalize the url
    disallowed_paths = []
    url_robots_txt = fetch_robots_txt(url) # get the robots_txt file
    
    if url_robots_txt: #if a robots.txt file is found
        disallowed_paths = fetch_disallowed_paths(url_robots_txt) #get all the paths that are disallowed from the rul

    
    parsed_url = urllib.parse.urlparse(url) # parse the url

    if not can_parse(url, disallowed_paths):
        return


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
    valid_links = [] #this is where we are going to store all of our valid links
    
    # print(f"The title for {url} is {url_title}")
    # print(f"The text for {url} is {url_text}")
    
    for i in range(len(url_all_links)): #print all links within the 
        # print(f"{link}\n")

        if not is_valid_url(url_all_links[i]):
            continue

    
        if url_all_links[i].startswith('/'): #if the given link is a relative link
            full_link = url_hostname + url_all_links[i] #reconstruct the full link
            if can_parse(full_link, disallowed_paths):
                valid_links.append(full_link)

        else: #otherwise it it probably a different hostname 
            valid_links.append(url_all_links[i])


    
    print(f"The urls found inside {url} are: \n")
    for link in valid_links:
        print(f"{link}\n")

    


def can_parse(link, disallowed_paths): #function to check whether we can parse a given link

    parsed_link = urllib.parse.urlparse(link)
    link_path  = parsed_link.path

    for path in disallowed_paths:
        if fnmatch(link_path, path): #the the paths match
            return False
        
    return True



def is_valid_url(url: str):

    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)




crawl('https://github.com/ashishpatel26/500-AI-Machine-learning-Deep-learning-Computer-vision-NLP-Projects-with-code?tab=readme-ov-file')
    



