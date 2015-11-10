import argparse, urllib2
from bs4 import BeautifulSoup


import re
def get_encoding(soup):
    encod = soup.meta.get('charset')
    if encod == None:
        encod = soup.meta.get('content-type')
        if encod == None:
            content = soup.meta.get('content')
            match = re.search('charset=(.*)', content)
            if match:
                encod = match.group(1)
            else:
                raise ValueError('unable to find encoding')
    return encod


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
    home_url = 'http://stteresa.catholic.org.hk/catechumenate/dictionary/'
    initial_letter = query[0].lower()
    query_url = home_url + initial_letter + '.htm'
    soup = BeautifulSoup(urllib2.urlopen(query_url).read().decode('big5', 'ignore'),'html.parser')
    # soup = BeautifulSoup(.read(), from_encoding="UTF-8")#"html.parser")
    # print get_encoding(soup)
    # exit()
    key_elems = soup.findAll('p',{'class' : 'green1'})[0:-1]
    open_bracket = '\xc2\xa1]'
    close_bracket = '\xc2\xa1^'
    dict = {}
    for key_elem in key_elems:
        # Find key
        key = remove_trailing_space(key_elem.contents[0].encode('utf8')).replace(open_bracket,'(').replace(close_bracket,')')
        # Find value
        this_elem = key_elem.next_sibling
        i = 0
        while not is_key(this_elem):
            if not this_elem:
                break
            if i == 0:
                dict[key] = this_elem
            else:
                dict[key] += this_elem
            i += 1
            this_elem = this_elem.next_sibling
        dict[key] = (remove_trailing_newline(dict[key].encode('utf8')))

    # Getting your matching dict entries
    with open('search_results.csv','wb') as res_f:
        for key,value in dict.iteritems():
            if query in key:
                res_f.write(key + ':' + value + '\n')
def split_queries(text):
    return text.split(',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome to Matteo 1.0! '\
                                                 'Matteo will read in an English Catholic term and retrieve the Chinese definition for you in a text file.')
    parser.add_argument('-q', '--query', help='Type in a comma-separated list of the requested English terms')
    args = parser.parse_args()
    queries = split_queries(args.query)

    for query in queries:
        search_query(query)
