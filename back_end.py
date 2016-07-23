# -*- coding: utf-8 -*-
# NOTE: Above line important for Chinese-character support

import sqlite3
from dict_info import dict_directory
from crit_info import crit_directory
    
def search_sqlite_query(dbpath,query,crit,search_str):
    # Connect to SQLite DB
    conn_db = sqlite3.connect(dbpath)
    cursor = conn_db.cursor()
    # SELECT matches for query for each search criterion
    match_entries = []
    cursor.execute(search_str.replace('<placeholder>',query))
    
    # Fetch data one by one
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        match_entries.append(row)
    print 'Found %d matching entries in the dictionary at %s for your query %s for your search criterion %s' % (len(match_entries),dbpath,query,crit)
    return match_entries
    
def fmt_sqlite_matches(match_entries,res_html,query):
    # Writing your matching SQLite entries to result html
    for match_entry in match_entries:
        res_html += """\
                <tr>
                    <td valign="top" bgcolor="#99C68E">%s</td>
                    <td valign="top">%s</td>
                </tr>
        """ % (match_entry[1].encode('utf8'),match_entry[2].encode('utf8'))
    res_html += """\
        </table>
    </div>
    """
    return res_html
    
def write_res_headers(res_html,dict_name_en,dict_name_zh,num_matches):
    res_header_html_p1 = u"""\
    <div class="dict_result" style="border: 1px solid gray; position:relative; float:top; top:10px">
        <table cellpadding="0" cellspacing="0" width="95%" align="center" >
            <tr bgcolor="#B6B6B4">
                <header align="center">
                    <h4><big>"""
    res_html += res_header_html_p1.encode('utf-8')
    res_html += dict_name_en
    res_header_html_p2 = u"""</big></h4>
                    <h4><big>"""
    res_html += res_header_html_p2.encode('utf-8')
    res_html += dict_name_zh.encode('utf-8')
    res_header_html_p3 = u"""</big></h4>
                    Found """
    res_html += res_header_html_p3.encode('utf-8')
    res_html += str(num_matches)
    res_header_html_p4 = u""" matching entry/entries in the dictionary for your query<br>
                </header>
            </tr>
            <tr>
                <td width="20%" bgcolor="#4AA02C"><b>English</b></td>
                <td width="*%" bgcolor="#4AA02C"><b>中文</b></td>
            </tr>
    """
    res_html += res_header_html_p4.encode('utf-8')
    return res_html
    
def run_matteo(query,req_dicts,req_crits):      # NOTE: MATTEO 2 will support only one query at a time AND only SQLite searching
    # Retrieve requested dictionaries from user
    # - If only one dictionary requested
    assert(type(req_dicts) in [unicode,list])
    if type(req_dicts) == unicode:
        req_dicts = [req_dicts]
    # - Assert crits not empty
    assert(type(req_crits) in [unicode,list])
    if type(req_crits) == unicode:
        req_crits = [req_crits]
    if not req_crits:
        return 'Error: No search criteria selected. Press BACK to re-enter.'
    # Display the search bar
    homepage_html_path = 'html\\home_dyn.html'
    res_html = open(homepage_html_path,'r').read()
    # - Add indication of searched query
    query_reminder_html = """\
    <div>
        <footer class="big_footer" style="position:relative; top:10px"><big>Search Results for '%s'</big></footer>
    </div>
    """ % (query.encode('utf-8'))
    res_html += query_reminder_html
    old_res_html = res_html
    # Get results
    # - Iterate through dictionaries
    for dict_i,(dict_name_en,dict_name_zh,dict_path) in dict_directory.items():
        # -- Ignore if dictionary not requested
        if dict_name_en not in req_dicts:
            continue
        # -- Get matches and save
        match_entries = []
        for dict_i,(crit_name,search_str) in crit_directory.items():
            # --- Ignore if criterion not supported
            if crit_name not in req_crits:
                continue
            match_entries += search_sqlite_query(dict_path,query,crit_name,search_str)
        # -- Write dictionary result headers
        res_html = write_res_headers(res_html,dict_name_en,dict_name_zh,len(match_entries))
        if match_entries:
            res_html = fmt_sqlite_matches(match_entries,res_html,query)
        dict_i += 1
    # Add a no results notice if no results found
    if res_html == old_res_html:
        res_html += """\
        <footer bgcolor="white" color="black" align="center" style="position:relative; top:10px">No dictionary selected!</footer>
        """
    # Else, end the table
    else:
        table_footer = """\
            </table>
        </div>
        """
        res_html += table_footer
    # Add footer
    footer_html_path = 'html\\footer_dyn.html'
    foot_html = open(footer_html_path,'r').read()
    res_html += foot_html
    return res_html
        
if __name__ == "__main__":
    run_matteo('Pope')