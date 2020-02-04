
import re
from urllib.parse import urlparse
import requests
from lxml import etree as et
from bs4 import BeautifulSoup


def scraper(url, resp):
      
    defragment = url.split('#')[0]
    #print(defragment)
    links = extract_next_links(defragment, resp)
    #for i in links:
        #print(i)
    validlinks = [link for link in links if is_valid(link)]
    return validlinks

 
def extract_next_links(url, resp):
    # Implementation requred.
    soup = BeautifulSoup(resp.text, features="lxml")
    text = soup.get_text()
    for line in text.splitlines():
        print(line.strip())

    #print(soup.get_text()) 


 
    return [link.get('href') for link in soup.find_all('a')]

def is_valid(url):
    # domain patterns that are valid
    generalHN = r".*((\.ics\.uci\.edu)|(\.cs\.uci\.edu)|(\.informatics\.uci\.edu)|(\.stat\.uci\.edu))$"
    specHN = r".*today\.uci\.edu$"
    specPath = r"^\/department\/information_computer_sciences\/.*"
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif not re.match(generalHN, parsed.netloc):
            return False
        elif not re.match(specHN, parsed.netloc) and re.match(specPath, parsed.path):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


if __name__ == "__main__":
    resp = requests.get("http://www.ics.uci.edu#aaa")
    #print(resp.text)
    #newresp = Response(cbor.loads(resp.content))
    scraper("http://www.ics.uci.edu#aaa", resp)
    







