Attribute VB_Name = "NewMacros"
Type RenameDef
    OldName As String
    NewName As String
End Type

Sub ���ɦҮ֮榡()
    Dim anchor As Range
    Set anchor = Selection.Range
    Call �A������
    Call ���D�ǩ�
    Call ����۰ʼи��ζ���
    anchor.Select
End Sub

Sub �A������()
    Selection.Find.ClearFormatting
    With Selection.Find
        .Text = "�u*�v"
        .Forward = True
        .Wrap = wdFindContinue
        .Format = True
        .MatchWildcards = True
    End With
    Selection.HomeKey Unit:=wdStory
    Selection.Find.Execute
    Do While Selection.Find.Found
      Selection.Font.Bold = True
      Selection.Find.Execute
    Loop
End Sub

Sub �������ǩ�()
    With Selection.Find
        .Text = "�](����[0-9]{1,}*)�^"
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        .MatchWildcards = True
    End With
    
    Selection.HomeKey Unit:=wdStory
    Selection.Find.Execute
    Do While Selection.Find.Found
        Selection.Font.Bold = True
        Selection.Font.Shading.Texture = wdTexture10Percent
        Selection.Find.Execute
    Loop
    
End Sub

Sub ����۰ʼи��ζ���ǩ�()
    Dim seq As Integer
    seq = 1
    With Selection.Find
        .Text = "�](����[0-9]{1,}*)�^"
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        .MatchWildcards = True
    End With
    
    Selection.HomeKey Unit:=wdStory
    Selection.Find.Execute
    Do While Selection.Find.Found
        Selection.Font.Bold = True
        Selection.Font.Shading.Texture = wdTexture10Percent
        Selection.Text = "�]����" + CStr(seq) + "�^"
        seq = seq + 1
        Selection.Find.Execute
    Loop
    
End Sub

Sub ���D�ǩ�()
' ����2 ����
' �������s�� 2013/1/7�A���s�� �i²�W��
'
    Selection.Find.ClearFormatting
    With Selection.Find
        .Text = "[�@�G�T�|�����C�K�E�Q]�B"
        .Forward = True
        .Wrap = wdFindStop
        .Format = True
        .MatchWildcards = True
    End With
    
    Selection.HomeKey Unit:=wdStory
    Selection.Find.Execute
    Do While Selection.Find.Found
      Selection.Paragraphs(1).Shading.BackgroundPatternColor = wdColorGray15
      Selection.Font.Bold = False
      Selection.Find.Execute
    Loop
    
End Sub

Sub ��w��󭫩R�W()
Attribute ��w��󭫩R�W.VB_Description = "�������s�� 2013/1/16�A���s�� �i²�W��"
Attribute ��w��󭫩R�W.VB_ProcData.VB_Invoke_Func = "Normal.NewMacros.��w��󭫩R�W"
    Dim renames(2) As RenameDef
    renames(1).OldName = "�i�������Ρj"
    renames(1).NewName = "�Ὤ���a��|�ȧ�"
    renames(2).OldName = "�����N�X"
    renames(2).NewName = "HLTB"
    
    For i = 1 To 2
        Dim r As RenameDef
        r = renames(i)
        Selection.Find.ClearFormatting
        Selection.Find.Replacement.ClearFormatting
        With Selection.Find
            .Text = r.OldName
            .Replacement.Text = r.NewName
            .Forward = True
        End With
        Selection.Find.Execute Replace:=wdReplaceAll
    Next i

End Sub
