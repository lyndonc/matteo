import argparse, urllib2
from bs4 import BeautifulSoup
import re

def remove_trailing_space(text):
    if text[-1] == ' ':
        return text[0:-1]
    else:
        return text

def remove_trailing_newline(text):
    if text[-2:] == ' \n':
        return text[0:-2]
    return text

def is_key(elem):
    try:
        if '<p' in str(elem) and 'class="green1"' in str(elem):
            return True
        return False
    except:
        return False

def search_query(query):
    # Decipher underscores as spaces
    query = query.replace('_',' ')
    # Access website through BeautifulSoup
    home_url = 'http://stteresa.catholic.org.hk/catechumenate/dictionary/'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    initial_letter = query[0].lower()
    query_url = home_url + initial_letter + '.htm'
    print query_url
    request = urllib2.Request(query_url, headers=hdr)
    soup = BeautifulSoup(urllib2.urlopen(request).read().decode('big5', 'ignore'),'html.parser')
    # Search for matching dictionary entries
    key_elems = soup.findAll('p',{'class' : 'green1'})[0:-1]
    open_bracket = '\xc2\xa1]'
    close_bracket = '\xc2\xa1^'
    dict = {}
    for key_elem in key_elems:
        # Find key (English term)
        key = remove_trailing_space(key_elem.contents[0].encode('utf8')).replace(open_bracket,'(').replace(close_bracket,')')
        # Find value
        # 1. Get primary definition
        this_elem = key_elem.next_sibling
        prim_def = this_elem.encode('utf8')
        # 2. Get explanation(s)
        i = 0
        explanation = ''
        while not is_key(this_elem):
            if not this_elem:
                break
            if i == 0:
                explanation = this_elem
            else:
                explanation += this_elem
            i += 1
            this_elem = this_elem.next_sibling
        # 3. Add the term, definition, and explanation to the dictionary
        dict[key] = (prim_def,remove_trailing_newline(explanation.encode('utf8')))

    # Writing your matching dict entries to file
    with open('search_results.csv','wb') as res_f:
        for key,value in dict.iteritems():
            if query in key:
                res_f.write(key + '\t' + value[0] + '\t' + value[1] + '\n')
def split_queries(text):
    return text.split(',')

if __name__ == "__main__":
    # Boilerplate of MATTEO
    parser = argparse.ArgumentParser(description='Welcome to Matteo 1.0! '\
                                                 'Matteo will read in an English Catholic term and retrieve the Chinese definition for you in a text file.')
    parser.add_argument('-q', '--query', help='Type in a comma-separated list of the requested English terms (replace spaces with underscores)')
    args = parser.parse_args()
    queries = split_queries(args.query)

    for query in queries:
        search_query(query)
