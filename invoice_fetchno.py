#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import string
import sqlite3

def fetch_number(id):
    prefix = 'http://www.ppmof.gov.tw/invoice_detail.asp?file_id='
    url = prefix + id
    request = urllib2.urlopen(url)
    content = request.read()
    content = filter(lambda x: x in string.printable, content)
    match = re.findall(r'>\d+<', content)
    return [re.findall(r'\d+', m)[0] for m in match]


if __name__ == "__main__":
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('SELECT * FROM mdetails WHERE status=\'standby\'')
    for year, month, status, id in c.fetchall():
        print 'Processing ' + year + '-' + month
        numbers = fetch_number(id)
        i = 0
        while i < len(numbers):
            if len(numbers[i]) == 8:
                c.execute('INSERT INTO numbers VALUES (?,?,?,?)',
                    (year, month, 'special', numbers[i]))
                print 'Special prize: ' + numbers[i]
            elif len(numbers[i]) == 5:
                c.execute('INSERT INTO numbers VALUES (?,?,?,?)',
                    (year, month, 'normal', numbers[i] + numbers[i+1]))
                print 'Normal prize: ' + numbers[i] + numbers[i+1]
                i += 1
            elif len(numbers[i]) == 3:
                c.execute('INSERT INTO numbers VALUES (?,?,?,?)',
                    (year, month, 'wildcard', numbers[i]))
                print 'Wildcard: ' + numbers[i]
            i += 1
        c.execute('UPDATE mdetails SET status=\'done\' WHERE year=? AND month=?',
            (year, month))
    conn.commit()
    conn.close()
