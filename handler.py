
from lxml import etree
from xml.etree import ElementTree as ET
import sqlite3
import re

def browse_handler(self, path, qs):
    if 'u' not in qs or 'y' not in qs or 'm' not in qs: return
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records WHERE user = ? AND year = ? AND month = ?',
        (qs['u'][0], qs['y'][0], qs['m'][0]))
    #print c.fetchall()
    self.send_response(200)
    self.send_header("Content-type", "text/xml")
    self.end_headers()
    # create a XML tree
    root = etree.Element('records')
    for r in c.fetchall():
        child = etree.Element('record')
        etree.SubElement(child, 'user').text = r[0]
        etree.SubElement(child, 'year').text = r[1]
        etree.SubElement(child, 'month').text = r[2]
        etree.SubElement(child, 'number').text = r[3]
        etree.SubElement(child, 'memo').text = r[4]
        root.append(child)
    # finally write it to client
    self.wfile.write(etree.tostring(root, pretty_print = True, xml_declaration = True, encoding = 'utf-8'))
    conn.close()

def months_handler(self, path, qs):
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('SELECT * FROM months')
    self.send_response(200)
    self.send_header("Content-type", "text/xml")
    self.end_headers()
    root = etree.Element('months')
    for m in c.fetchall():
        child = etree.Element('m')
        child.text = m[0] + '-' + m[1]
        #etree.SubElement(child, 'year').text = m[0]
        #etree.SubElement(child, 'month').text = m[1]
        root.append(child)
    self.wfile.write(etree.tostring(root, pretty_print = True, xml_declaration = True, encoding = 'utf-8'))
    #self.wfile.write(etree.tostring(root))
    conn.close()

def addnew_handler(self):
    varLen = int(self.headers['Content-Length'])
    postVars = self.rfile.read(varLen)
    try:
        tree = ET.fromstring(postVars)
        user = tree.find('user').text
        year = tree.find('year').text
        month = tree.find('month').text
        number = tree.find('number').text
        memo = tree.find('memo').text
        print '|'.join(map(str, [user, year, month, number, memo]))
    except ET.ParseError:
        print 'ParseError'
        return
    try:
        if not re.compile('^\w+$').match(str(user)):
            raise ValueError('user')
        if not re.compile('^\d{2,}$').match(str(year)):
            raise ValueError('year')
        if not re.compile('^\d{4}$').match(str(month)):
            raise ValueError('month')
        if not re.compile('^\d{8}$').match(str(number)):
            raise ValueError('number')
        # do we need to check memo?
    except ValueError:
        print 'ValueError'
        return
    conn = sqlite3.connect('records.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records WHERE user=? AND year=? AND month=? AND number=?', 
        (user, year, month, number))
    if len(c.fetchall()) == 0:
        c.execute('INSERT INTO records VALUES (?,?,?,?,?)',
            (user, year, month, number, memo))
        response = 'Inserted'
    else:
        c.execute('UPDATE records SET memo=? WHERE user=? AND year=? AND month=? AND number=?',
            (memo, user, year, month, number))
        response = 'Updated'
    conn.commit()
    conn.close()
    self.send_response(200)
    self.end_headers()
    self.wfile.write(response)
    conn.close()
