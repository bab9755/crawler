import urllib.parse
import requests

def fetch_robots_txt(url: str):

    parsed_url = urllib.parse.urlparse(url)

    url_robots_txt = fetch_robots_txt(url) # get the robots_txt file

    disallowed_paths = fetch_disallowed_paths(url_robots_txt) #get all the paths that are disallowed from the rul

    # print(f"the netloc is {parsed_url.netloc}")

    robots_txt_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    robots_response = requests.get(robots_txt_url)

    if robots_response.status_code == 200: #return the robots.txt file if found
        # print(f"The generated robots.txt is: \n{robots_response.text}")

        return robots_response.text

    else: #return an empty string if we go not find 
        print(f"Could not find robots.txt for {url}\n")
        return ''



def fetch_disallowed_paths(robots_txt: str):

    disallowed_paths = []

    lines = robots_txt.splitlines()

    # print(lines)

    for line in lines:

        # print(f'Line: {line}')
        # line = line.strip() #get rid of spaces
        if line.startswith('Disallow:'): #thats not we know we got our disallowed paths
            # print("Found a relevant line")
            path = line.split(":", 1)[1].strip()
            if path:
                disallowed_paths.append(path)

    return disallowed_paths



    
    


robots_txt = fetch_robots_txt('https://www.youtube.com/')

disallowed = fetch_disallowed_paths(robots_txt)

for path in disallowed:
    print(path)