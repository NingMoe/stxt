# coding=utf-8
from spark import *
from tree import Node

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __cmp__(self, o):
		    return cmp(self.type, o)

    def __str__(self):
        print self.value.decode('utf8')
        return "%s" % (self.type)

class Lexer(GenericScanner):
    "Tokenize words, punctuation and markup"
    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    #def t_whitespace(self, s):
    #    r" [ \t\r]+ "
    #    self.rv.append(Token('whitespace', ' '))
    #    pass

    def t_emptyline(self, s):
        r"\s*\n"
        self.rv.append(Token('emptyline', ' '))

    def t_titlesep(self, s):
        r"[-]+\n"
        self.rv.append(Token('titlesep', s))

    def t_docattr(self, s):
        r"[^:\n]+[:][^:\n]+\n"
        self.rv.append(Token('docattr', s.strip()))

    def t_secnumber(self, s):
        r"(\d\.)+"
        self.rv.append(Token('secnumber', s))

    def t_line(self, s):
        r"[^-\d\s][^\n]+\n"
        self.rv.append(Token('line', s.strip()))

class Parser(GenericParser):
    def __init__(self, start='doc'):
        GenericParser.__init__(self, start)

    def p_doc(self, args):
        ' doc ::= title docattrs emptyline sects'
        doc = Node(type="doc", title=args[0])
        attrs = {}
        for a in args[1]:
            a = a.value.split(':')
            attrs[a[0]]=a[1]
        doc.attrs = attrs
        for s in args[3]:
            doc.append(s)
        return doc

    def p_title(self, args):
        ' title ::= line titlesep emptyline'
        return args[0].value

    def p_init_list(self, args):
        '''docattrs ::= docattr
           sects ::= sect
           paras ::= para
        '''
        return [args[0]]

    def p_lists(self, args):
        '''docattrs ::= docattrs docattr
           sects ::= sects sect
           paras ::= paras emptyline para
        '''
        args[0].append(args[1])
        return args[0]
 
    def p_sect_0(self, args):
        ''' sect ::= secnumber line emptyline
            sect ::= secnumber emptyline
        '''
        sect = Node(type='sect')
        sect.secnumber = args[0]
        if len(args) == 3:
            sect.append(Node(type='para', value = args[1].value))
        return sect

    def p_sect(self, args):
        ''' sect ::= secnumber line emptyline paras emptyline
            sect ::= secnumber emptyline paras emptyline
        '''
        sect = Node(type='sect')
        sect.secnumber = args[0]
        if len(args) == 5:
            sect.append(Node(type='para', value = args[1].value))
            ps = args[3]
        else:
            ps = args[2]

        for p in ps:
            sect.append(Node(type='para', value = p.value))
        return sect

    def p_para_0(self, args):
        ''' para ::= line
        '''
        return Node('para', args[0].value.strip())

    def p_para(self, args):
        ''' para ::= para line
        '''
        args[0].value += args[1].value
        return args[0]

if __name__ == '__main__':
    from optparse import OptionParser
    usage = u"usage: %prog SOURCE [options]"
    oparser = OptionParser(usage, version="%prog 1.1")
    oparser.add_option("-d", "--debug", action="store_true", 
                       dest="debug", default=False,
                       help=u"除錯模式")

    (options, args) = oparser.parse_args()

    if len(args) < 1:
        oparser.error("Must supply the SOURCE file!")

    src = args[0]
    with open(src) as f:
        tokens = legal.Lexer().tokenize(f.read())