# coding=utf-8
from __future__ import with_statement
import sys, os, re, unittest, stxt_parser
def export_table(file, name):
  # make doctree
  d = stxt_parser.parser.read(file)
  table = d.find_by_name(name)
  print f_csv(table).decode('utf8').encode('cp950')

def f_csv(table):
  csv = ''
  if table.children:
    for row in table.children:
      first = True
      for col in row.children:
        if first:
          csv += col.value.encode('utf8')
          first = False
        else:
          csv += ', '+ col.value.encode('utf8')
      csv += '\n' 
  csv = csv[0:len(csv)-1]
  return csv

if __name__ == '__main__':
  usage = "USAGE:" + os.path.basename(__file__) + " filename table_name"
  try:
    export_table(sys.argv[1], sys.argv[2])
  except IndexError:
    print usage