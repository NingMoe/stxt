# coding=utf8 
import sys, yacc, unittest
from stxt_lexer import *
# Parser 
def p_book(p):
  '''book : sect1          
          | book sect1
          | content
          | book content'''
  if len(p) == 2:
    p[0] = DocTreeNode('book', '')
    p[0].append(p[1])
  else:
    p[1].append(p[2])
    p[0] = p[1]
#def p_error_sect2(p):
#  r'book : error sect2'
#  print 'sect2 cannot be directly embeded in book.'
def p_sect1(p):
  '''sect1 : HEAD1 content1s'''
  p[0] = p[1]
  for c in p[2]:
    p[0].append(c) 
def p_content1s(p):
  '''content1s : sect2
               | content
               | content1s sect2
               | content1s content'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_sect2(p):
  'sect2 : HEAD2 content2s'
  p[0] = p[1]
  for c in p[2]:
    p[0].append(c) 

def p_sect2title(p):
  'sect2 : HEAD2 EMPTYLINE'
  p[0] = p[1]

def p_content2s(p):
  '''content2s : sect3
               | content
               | content2s sect3
               | content2s content'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_sect3(p):
  r'sect3 : HEAD3 content3s'
  p[0] = p[1]
  for c in p[2]:
    p[0].append(c) 

def p_content3s(p):
  '''content3s : content
               | content3s content'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[1].append(p[2])
    p[0] = p[1]
def p_content(p):
  '''content : para
             | para EMPTYLINE
             | code
             | code EMPTYLINE
             | table
             | table EMPTYLINE
             | image
             | image EMPTYLINE
             | list
             | list EMPTYLINE
             | footnotes EMPTYLINE
  '''
  p[0] = p[1]
def p_dlisthead(p):
  '''dlisthead : DL
               | DL l2para
  '''
  p[0] = p[1]
  if len(p) == 3 and p[2]:
    l2p = p[0].children[0]
    l2p.value = l2p.value + p[2].value
def p_listhead(p):
  '''listhead : LI
              | OL
              | dlisthead
              | LI l2para
              | OL l2para
  '''
  p[0] = p[1]
  if len(p) == 3 and p[2]:
    p[0].value += p[2].value
def p_listitem(p):
  '''listitem : listhead
              | listitem EMPTYLINE
              | listitem EMPTYLINE l2para
  '''
  p[0] = p[1]
  if len(p) == 4 and p[3]:
    #for l2para in p[2]:
    #p[0].append(l2para)
    p[0].append(p[3])
def p_list(p):
  '''list : listitem
          | list listitem
  '''
  if len(p) == 2:
    if p[1].type == 'listitem':
      p[0] = DocTreeNode('list', '')
    elif p[1].type == 'olistitem':
      p[0] = DocTreeNode('olist', '')
    elif p[1].type == 'dlistitem':
      p[0] = DocTreeNode('dlist', '')
    p[0].append(p[1])
  else:
    p[0] = p[1].append(p[2])

def p_code(p):
  r'code : CODEHEAD CODEBLOCK'
  p[0] = p[1]
  p[0].value = p[2]

def p_image(p):
  r'image : IMAGEHEAD'
  p[0] = p[1]

def p_para(p):
  '''para : LINE
          | para LINE
  '''
  if len(p) == 2:
    p[0] = DocTreeNode('para', p[1])
  else:
    if isinstance(p[1], str):
      p[1] = DocTreeNode('para', p[1])
    p[1].value +=  p[2]
    p[0] = p[1]

def p_l2para(p):
  '''l2para : L2LINE
            | l2para L2LINE
  '''
  if len(p) == 2:
    p[0] = DocTreeNode('l2para', p[1])
  else:
    p[1].value += p[2]
    p[0] = p[1]
#def p_l2paras(p): # nested 2 level paragraph
#  '''l2paras : l2para
#             | l2para EMPTYLINE
#             | l2paras l2para EMPTYLINE
#  '''
#  if len(p) in (2, 3):
#    p[0] = [p[1]]
#  elif len(p) == 4:
#    p[1].append(p[2])
#    p[0] = p[1]
def p_table(p): # nested 2 level paragraph
  '''table : TABLEHEAD TABLEBLOCK'''
  #p[1].value = p[2]
  if type(p[2]) == str:
    p[1].value = p[2]
    p[0] = p[1]
  else:
    p[2].title = p[1].title
    p[2].name = p[1].name
    p[0] = p[2]

def p_footnotes(p):
  '''footnotes : FOOTNOTE
               | footnotes FOOTNOTE'''
  if len(p) == 2:
    p[0] = DocTreeNode('footnotes', '')
    p[0].append(p[1])
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_error(t):
  print ("Parse Error:\n%s" \
          % str(t)).decode('utf8').encode('cp950')

parser = yacc.yacc()

class UnitTest(unittest.TestCase):
  def testIMAGEHEAD(self):
    case = 'image[name].this is a image title'
    book = parser.parse(case)
    self.assertEqual(book.type, 'book')
    self.assertEqual(book.children[0].type, 'image')
    self.assertEqual(book.children[0].name, 'name')
    self.assertEqual(book.children[0].title, 'this is a image title')

    # imagehead must having name block
    #case = 'image.this is a image title'
    #lexer.input(case)
    #tok = lexer.token()
    #self.assertEqual(tok.type, 'IMAGEHEAD')
    #self.assertEqual(tok.value.name, None)
    #self.assertEqual(tok.value.title, 'this is a image title')

  def testTable(self):
    testcase = '''table.交易
時間 交易A       交易B
==== =========== ===========
t1   A.read(p)    
t2   A.update(p)  
t3               B.read(p)   
t4               B.update(p)
==== =========== ===========
'''
    book = parser.parse(testcase)
    self.assertEqual(book.type, 'book')
    d = book.children[0]
    self.assertEqual('table', d.type)
    self.assertEqual('交易', d.title)
    header = d.children[0]
    self.assertEqual('tr', header.type)
    th1 = header.children[0]
    self.assertEqual('th', th1.type)
    self.assertEqual(u'時間', th1.value)
    th2 = header.children[1]
    self.assertEqual(u'交易A', th2.value)
    
    r2 = d.children[1]
    self.assertEqual('tr', r2.type)
    td1 = r2.children[0]
    self.assertEqual('td', td1.type)
    self.assertEqual('t1', td1.value)
    td2 = r2.children[1]
    self.assertEqual('A.read(p)', td2.value)

  def testTableSubparserError(self):
    testcase = '''table.交易
時間 交易A       交易B
==== =========== ===========ddd
t1   A.read(p)    
t2   A.update(p)  
t3               B.read(p)   
t4               B.update(p)
==== =========== ===========
'''
    book = parser.parse(testcase)
    self.assertEqual(book.type, 'book')
    d = book.children[0]
    self.assertEqual('table', d.type)
    self.assertEqual('交易', d.title)

    block = '''時間 交易A       交易B
==== =========== ===========ddd
t1   A.read(p)    
t2   A.update(p)  
t3               B.read(p)   
t4               B.update(p)
==== =========== ===========
'''
    self.assertEqual(block, d.value)

if __name__ == '__main__':
  unittest.main()
  # Give the lexer some input
  #lexer.writetab('lextab')
  #lexer.read(r"d:\stxt\doc\net\x_25.stx")
  # Tokenize
  #while True:
  #  tok = lexer.token()
  #  if not tok: break      # No more input
  #  print str(tok).decode('utf8').encode('cp950')
  #d = parser.read(r"d:\stxt\doc\net\atm.stx", debug=1)
  #d = parser.read(r"d:\stxt\doc\net\net.stx", debug=1)
  #d = parser.read(r"d:\stxt\doc\net\ipsec.stx", debug=1)
  #d = parser.read(r"d:\stxt\doc\db\db.stx", debug=1)
  #d.print_type_tree(7)
  #for c in d.dfs():
  #  print c.type