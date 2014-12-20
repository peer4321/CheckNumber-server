#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import string
import sqlite3

def fetch_detail_url(limit=0):
    prefix = 'http://www.ppmof.gov.tw/invoice.asp?Page=&invoiceMainPage='
    page = 0
    result = []
    while True:
        if page > 5:
            print 'Abort'
            return ''
        url = prefix + str(page)
        print 'url = ' + url
        request = urllib2.urlopen(url)
        content = request.read()
        print 'response length =', len(content)
        content = filter(lambda x: x in string.printable, content)
        #regex = "\\d+[\\D]+\\d+[\\D]+\\d+[\\D]+\">[\\w\\s=#-:%;<>(.?\'\"]+file_id=\\d+"
        regex = r'\d+[\D]+\d+[\D]+\d+[\D]+\">[\w\s=#-:%%;<>(.?\'\"]+file_id=\d+'
        match = re.findall(regex, content)
        tmp = [re.findall(r'\d+', m) for m in match]
        tmp = [m[0:3]+[m[-1]] for m in tmp]
        if len(tmp) == 0:
            break
        result.extend(tmp)
        if limit != 0 and len(result) >= limit:
            break
        page += 1
    return result

if __name__ == "__main__":
    details = fetch_detail_url()
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    for detail in details:
        year = detail[0]
        month = "%02d%02d" % (int(detail[1]), int(detail[2]))
        id = detail[3]
        c.execute('SELECT * FROM mdetails WHERE year=? AND month=?',
            (year, month))
        if len(c.fetchall()) != 0: continue
        c.execute('INSERT INTO mdetails VALUES (?,?,?,?)',
            (year, month, 'standby', id))
    conn.commit()
    conn.close()


