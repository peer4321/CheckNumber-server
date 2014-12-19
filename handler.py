
from lxml import etree
import sqlite3

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
    c.close()

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
    c.close()

