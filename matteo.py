# -*- coding: utf-8 -*-
# NOTE: Above line important for Chinese-character support

import argparse, sqlite3
        
def search_csv_query(dbpath,query):
    # Import dictionary
    dict = {}
    with open(dbpath,'r') as dict_f:
        for row in dict_f:
            assert(len(row.split('\t')) == 2)
            key = row.split('\t')[0].decode('utf-8')
            dict[key] = row.split('\t')[-1].replace('\n','').decode('utf-8')
    # Find matches for the query in the keys
    match_keys = [key for key,value in dict.items() if query.lower() in key.lower() or query.lower() in value.lower()]
    if not match_keys:
        raise Exception("Could not find a match for your query")
    print 'Found %d matching entries in the dictionary for your query' % (len(match_keys))
    return match_keys

def save_csv_matches(match_keys,query):
    # Writing your matching dict entries to file
    with open('search_results.csv','ab') as res_f:
        for match_key in match_keys:
            res_f.write('----------------------------------------\n')
            res_f.write('    Query: %s\n' % (query))
            res_f.write('----------------------------------------\n')
            res_f.write(match_key.encode('utf-8') + '\t' + dict[match_key].encode('utf-8') + '\n')
    print 'Your search results for "%s" have been saved to search_results.csv' % (query)    
    
def search_sqlite_query(dbpath,query):
    # Connect to SQLite DB
    conn_db = sqlite3.connect(dbpath)
    cursor = conn_db.cursor()
    # SELECT matches for query
    search_str = "SELECT * FROM dictionary WHERE Term LIKE '%" + query + "%'"
    cursor.execute(search_str)
    
    # Fetch data one by one
    match_entries = []
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        match_entries.append(row)
    print 'Found %d matching entries in the dictionary for your query' % (len(match_entries))
    return match_entries
    
def save_sqlite_matches(match_entries,query):
    # Writing your matching SQLite entries to file
    with open('search_results.csv','ab') as res_f:
        res_f.write('----------------------------------------\n')
        res_f.write('    Query: %s\n' % (query))
        res_f.write('----------------------------------------\n')        
        for match_entry in match_entries:
            res_f.write(match_entry[1].encode('utf-8') + '\t' + match_entry[2].encode('utf-8') + '\n')
    print 'Your search results for "%s" have been saved to search_results.csv' % (query)
    
def split_queries(text):
    return text.split(',')
    
def write_res_headers(fpath,dict_name):
    with open(fpath,'ab') as res_f:
        res_f.write('\n================================================================================\n')
        res_f.write((u'DICTIONARY: '+dict_name+'\n').encode('utf8'))
        res_f.write(u'English term\t中文翻譯\n'.encode('utf8'))
        res_f.write('================================================================================\n')

if __name__ == "__main__":
    # Boilerplate of MATTEO
    parser = argparse.ArgumentParser(description='Welcome to Matteo 1.2! '\
                                                 'Matteo will read in an English Catholic term and retrieve the Chinese definition for you in a text file.')
    parser.add_argument('-q', '--query', help='Type in a comma-separated list of the requested English terms (replace spaces with underscores)')
    args = parser.parse_args()
    queries = split_queries(args.query)
    
    # Clear out the results file
    open('search_results.csv','wb')
    
    # Obtaining matches
    db_type = 0 # 0: SQLite, 1: CSV
    sqlite_dicts = [r'db\en_zh_cath_dict.db',r'db\en_zh_cath_dict_reordered.db']
    csv_dicts = [r'dict\en_zh_cath_dict.csv',r'dict\en_zh_cath_dict_reordered.csv']
    dict_names = [u'《天主教英漢袖珍辭典》',u'《天主教英漢袖珍辭典》 (comma-reordered)']
    # Determine dicts
    if db_type == 0:
        dicts = sqlite_dicts
    elif db_type == 1:
        dicts = csv_dicts
    
    # Get results
    dict_i = 0
    # - Iterate through dictionaries
    for dict in dicts:
        # -- Write dictionary result headers
        write_res_headers('search_results.csv',dict_names[dict_i])
        # -- Iterate through queries
        for query in queries:
            if db_type == 0:
                # Get matches and save
                match_entries = search_sqlite_query(sqlite_dicts[dict_i],query)
                if match_entries:
                    save_sqlite_matches(match_entries,query)
            elif db_type == 1:
                # Get matches and save
                match_keys = search_csv_query(csv_dicts[dict_i],query)
                if match_keys:
                    save_csv_matches(match_keys,query)
        dict_i += 1