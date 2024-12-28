const {JSDOM} = require("jsdom");

//keep in mind that this is only for crawling a single url at the beginning
async function crawlPage(baseUrl, currentUrl, pages) {
    const baseUrlObj = new URL(baseUrl);
    const currentUrlObj = new URL(currentUrl);

    if(baseUrlObj.hostname != currentUrlObj.hostname){ //since we care about a single host, if we hit a host that is not the same as the base then we return
        return pages; // this means we are done crawling a certain web page
    }

    const normalizedCurrentUrl = normalizeURL(currentUrl);
    if(pages[normalizedCurrentUrl] > 0){ //if we have already seen the page we increment its count and return our pages dict
        pages[normalizedCurrentUrl]++;
        return pages; //pages is a dictionary
    }

    pages[normalizedCurrentUrl] = 1; //otherwise we initialize it to 1
    console.log(`actively crawling page ${currentUrl}`);

    try {
        const response = await fetch(currentUrl);
 
        //when getting the response we want to make sure that 1) the status code is less than 400 and 2) the content type is text/html
        if (response.status > 399) { //if we get some sort of status 400 code we return
            console.log(`Error fetching ${currentUrl} with status code ${response.status}`);
            return pages;
        }

        const contentType = response.headers.get("content-type");
        console.log(`Fetching ${currentUrl} with content type ${contentType}`);

        if (!contentType.includes("text/html")) { //if the current page is not an html page we do not need it and we can return
            console.log(`Non HTML response, content type: ${contentType} on page ${currentUrl}`);
            return pages;
        }

        const htmlBody = await response.text(); //get the html from the current page

        const nextUrls = getURLsfromHTML(htmlBody, baseUrl);

        for (const nextUrl of nextUrls) {
            pages = await crawlPage(baseUrl, nextUrl, pages);
        }
    } catch (error) {
        console.log(`Error crawling ${currentUrl} ${error}`);
    }

    return pages;

}

function getURLsfromHTML(htmlBody, baseUrl) {

    const urls = [];

    const dom = new JSDOM(htmlBody); //convert the html body to the right object type
    const linkElements = dom.window.document.querySelectorAll('a'); //get all the link elements

    for (const linkElement of linkElements) {

        if (linkElement.href.slice(0, 1) === '/') {

            try {
                const urlObj = new URL(`${baseUrl}${linkElement.href}`); //this is the case where a path is relative eg /about
                urls.push(urlObj.href);
            } catch (error) {
                console.log(`Error parsing URL ${linkElement.href}`);
            }
            
        } else {

            try {
                const urlObj = new URL(linkElement.href); //this is when a path is absolute ex https://www.google.com
                urls.push(urlObj.href);
            } catch (error) {
                console.log (`Error parsing URL ${linkElement.href}`);
            }
        }
    }

    return urls;
}

function normalizeURL(urlString){ 
    const urlObj = new URL(urlString);
    console.log(`the url host is ${urlObj.host} and the path is ${urlObj.pathname}`);
    const hostPath = `${urlObj.host}${urlObj.pathname}`;
    console.log(`The host path of ${urlString} is ${hostPath}`);
    if (hostPath.length > 0 && hostPath.slice(-1) !== '/'){
        return hostPath.slice(0, -1);
    }

    return hostPath;
}





module.exports = {
    normalizeURL,
    getURLsfromHTML,
    crawlPage
};