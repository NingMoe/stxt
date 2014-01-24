# coding=utf-8
import sys, os, re, win32com
from win32com.client import Dispatch, constants, DispatchEx
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from spark import GenericASTTraversal

wdHeaderFooterPrimary = 1

wdAlignPageNumberLeft = 0
wdAlignPageNumberCenter = 1
wdAlignPageNumberRight = 2
wdAlignPageNumberInside = 3
wdAlignPageNumberOutside = 4

wdReplaceAll = 2

class MSWordOut(GenericASTTraversal):
    def __init__(self, ast):
        GenericASTTraversal.__init__(self, ast)
        msword = DispatchEx('Word.Application')
        msword.Visible = 1	# 1表示要顯示畫面，若為0則不顯示畫面。

        self.word = msword
        self.doc  = msword.Documents.Add() # 開啟一個新的文件。
        pageSetup = self.doc.PageSetup
        pageSetup.TopMargin = 64
        pageSetup.BottomMargin = 64


        #With ActiveDocument.Sections(1).Footers(wdHeaderFooterPrimary)
        # .PageNumbers.Add PageNumberAlignment:=wdAlignPageNumberRight
        #End With

        section = self.doc.Sections(1)

        
        self.range	= self.doc.Range()
        # 設定字型為標楷體
        self.range.Font.Name = u"標楷體".encode('cp950')  
        self.range.Font.Size = 14
        self.range.ParagraphFormat.LineSpacingRule = 4 
        self.range.ParagraphFormat.LineSpacing = 22 
        #import pdb; pdb.set_trace()
        #self.range.paragraphs.LineSpacingRule = 4 #constants.WdLineSpaceExactly
        #self.range.LineSpacing = 22
        self.preorder()
        ti = 1 # title line number
        # Format Title
        if ast.title:
            para = self.doc.Paragraphs.First
            para.Format.Alignment = 1 # center
            para.Range.Font.Size = 18
            para.Range.Font.Bold = 1
            if ast.title.count('\n') == 1:
                para = self.doc.Paragraphs(2)
                para.Format.Alignment = 1 # center
                para.Range.Select()
                msword.Selection.Font.Size = 18
                msword.Selection.Font.Bold = 1
                ti = 2
        try:
            history = ast.attrs[u'訂定'] + u'函訂定'
            para = self.doc.Paragraphs(ti + 1)
            para.Format.Alignment = 2 # center
            para.Range.Select()
            msword.Selection.Font.Size = 10

        except KeyError, k:
            pass
        except AttributeError, k:
            pass
        
        
        #import pdb; pdb.set_trace()
        content = self.doc.Content
        content.Find.ClearFormatting()
        content.Find.MatchWildcards=True
        content.Find.Text = u"「*」".encode('cp950')

        content.Find.Execute()

        while content.Find.Found:
            content.Find.parent.Font.Bold = True
            content.Find.Execute()
        footer = self.word.ActiveDocument.Sections(1).Footers(1)
        footer.PageNumbers.Add()

        footer = section.Footers(wdHeaderFooterPrimary)
        footer.PageNumbers.Add(wdAlignPageNumberCenter)

    def n_doc(self, node):
        para = self.doc.Paragraphs.Last
        para.Style.Font.Size = 12
        para.Style.Font.Bold = 0
        if node.title:
            para.Range.InsertAfter(node.title)
            try:
                history = node.attrs[u'訂定'] + u'函訂定'
                self.doc.Paragraphs.Add() 
                para.Range.InsertAfter(history)
            except KeyError, k:
                pass
            except AttributeError, k:
                pass

    def n_sect(self, node):
        #import pdb;pdb.set_trace()
        self.doc.Paragraphs.Add() 
        para = self.doc.Paragraphs.Last
        #para.Format.LeftIndent = 24 * (node.height)
        if node.height == 1:
            para.Format.LeftIndent = 20
            para.Format.FirstLineIndent = -20
            para.Range.Font.Bold = 1
        elif node.height == 2:
            para.Format.LeftIndent = 42 
            para.Format.FirstLineIndent = -35
            para.Range.Font.Bold = 1
        elif node.height == 3:
            para.Format.LeftIndent = 64
            para.Format.FirstLineIndent = -16
            para.Range.Font.Bold = 0
        elif node.height == 4:
            para.Format.LeftIndent = 84
            para.Format.FirstLineIndent = -16
        elif node.height == 5:
            para.Format.LeftIndent = 108
            para.Format.FirstLineIndent = -16
        elif node.height == 6:
            para.Format.LeftIndent = 128
            para.Format.FirstLineIndent = -16
        elif node.height == 7:
            para.Format.LeftIndent = 148
            para.Format.FirstLineIndent = -16

        para.Range.InsertAfter(self.sect_num(node))
        #if node.height > 1 and node.order == 0:
        #elif node.height > 1 and \
        #     node.sibling(node.order-1).type == 'para' :
        #    para.Indent()

    def n_para(self, node):
        para = self.doc.Paragraphs.Last
        if node.order != 0:
            self.doc.Paragraphs.Add()
            para = self.doc.Paragraphs.Last
            para.Format.FirstLineIndent = 0
            self.range.ParagraphFormat.LineSpacingRule = 4 
            self.range.ParagraphFormat.LineSpacing = 22 

        para.Range.InsertAfter(node.value)

        if node.order != 0:
            para.Range.Font.Bold = 0
        elif node.order == 0 and len(node.value) > 25:
            para.Range.Font.Bold = 0
        
    def sect_num(self, node):
        cbd = [u'零',u'壹',u'貳',u'參',u'肆',u'伍',u'陸',u'柒',
               u'捌',u'玖',u'拾',u'拾壹', u'拾貳',
               u'拾參',u'拾肆',u'拾伍',u'拾陸','柒','捌','玖','拾']
        cd = [u'零',u'一',u'二',u'三',u'四',u'五',u'六',u'七',
              u'八',u'九',u'十', u'十一',u'十二',u'十三',u'十四',
              u'十五',u'十六',u'十七',u'十九',u'二十'
              u'二十一',u'二十二',u'二十三',u'二十四',u'二十五',u'二十六',
              '二十七','二十八','二十九', '三十', 
              '三十一','三十二','三十三','三十四','三十五','三十六',
              '三十七','三十八','三十九'
             ]
        n = int(node.numbers[-1])
        if node.level == 1:
            return cd[n].encode('big5') + '.'
        elif node.level == 2:
            return '(' + cd[n].encode('big5') + ')' + ' '
        elif node.level == 3:
            return str(n) + '.'
        elif node.level == 4:
            return '(' + str(n) + ')' + ' '
        elif node.level == 5:
            return chr(64+n) + '.' + ' '
        else:
            return str(n) + '.'
