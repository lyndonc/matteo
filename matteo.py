# -*- coding: utf-8 -*-
# NOTE: Above line important for Chinese-character support

import argparse
        
def search_query(dict,query):
    # Find matches for the query in the keys
    match_keys = [key for key,value in dict.items() if query.lower() in key.lower() or query.lower() in value.lower()]
    if not match_keys:
        raise Exception("Could not find a match for your query")
    print 'Found %d matching entries in the dictionary for your query' % (len(match_keys))
    # Writing your matching dict entries to file
    with open('search_results.csv','wb') as res_f:
        res_f.write(u'English term\t中文翻譯\n'.encode('utf8'))
        res_f.write('========================================\n')
        for match_key in match_keys:
            res_f.write(match_key + '\t' + dict[match_key].encode('utf-8') + '\n')
    print 'Your results have been saved to search_results.csv'
    
def split_queries(text):
    return text.split(',')

if __name__ == "__main__":
    # Boilerplate of MATTEO
    parser = argparse.ArgumentParser(description='Welcome to Matteo 1.0! '\
                                                 'Matteo will read in an English Catholic term and retrieve the Chinese definition for you in a text file.')
    parser.add_argument('-q', '--query', help='Type in a comma-separated list of the requested English terms (replace spaces with underscores)')
    args = parser.parse_args()
    queries = split_queries(args.query)
    
    # Import dictionary
    dict = {}
    dict_path = r'dict\en_zh_cath_dict.csv'
    with open(dict_path,'r') as dict_f:
        for row in dict_f:
            assert(len(row.split('\t')) == 2)
            key = row.split('\t')[0]
            dict[key] = row.split('\t')[-1].replace('\n','').decode('utf-8')

    for query in queries:
        search_query(dict,query)
