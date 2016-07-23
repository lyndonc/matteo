import sqlite3

def dict_to_sqlite(dict,is_reordered):
    # Connect to SQLite DB
    if is_reordered:
        db_path = r'C:\Users\lyndonc\Documents\Hobby Projects\Matteo\v3\db\saint_names_girl.db'
    else:
        db_path = r'C:\Users\lyndonc\Documents\Hobby Projects\Matteo\v3\db\saint_names_girl.db'
    conn_db = sqlite3.connect(db_path)
    cursor = conn_db.cursor()
    
    # Fill up SQLite DB
    # - Deleting pre-existing "dictionary" table
    cursor.execute("DROP TABLE IF EXISTS dictionary")
    # - Creating "dictionary" table
    cursor.execute("CREATE TABLE dictionary (Id INT, Term TEXT, Translation TEXT)")
    # - Inserting data into "dictionary" table
    term_i = 0
    for key,value in dict.items():
        term_i += 1
        insert_str = "INSERT INTO dictionary VALUES (?,?,?)"
        print term_i
        params = (term_i, key, value)
        try:
            cursor.execute(insert_str,params)
        except:
            print key.encode('utf-8')
            print value.encode('utf-8')
            print "PROBLEM!!!"
            break
    # - Committing changes to the SQLite DB
    conn_db.commit()

def main():
    # Import dictionary
    dict = {}
    is_reordered = 0    # 0: use non-reordered dict, 1: use reordered dict
    num_delim = 2
    if is_reordered:
        dict_path = r'C:\Users\lyndonc\Documents\Hobby Projects\Matteo\v3\dict\saint_names_girl.csv'
    else:
        dict_path = r'C:\Users\lyndonc\Documents\Hobby Projects\Matteo\v3\dict\saint_names_girl.csv'
    with open(dict_path,'r') as dict_f:
        for row in dict_f:
            print row
            assert(len(row.split('\t')) == num_delim)
            key = row.split('\t')[0].decode('utf-8')
            dict[key] = row.split('\t')[-1].replace('\n','').decode('utf-8')
    dict_to_sqlite(dict,is_reordered)
    
if __name__ == '__main__':
    main()
