Attribute VB_Name = "NewMacros"
Sub �~�ȦҮ֪���s��()
Attribute �~�ȦҮ֪���s��.VB_ProcData.VB_Invoke_Func = "Normal.NewMacros.����s��"
'
' ����s�� ����
'
'
    Dim i As Integer
    i = 0
    Selection.MoveStart
    Do
      With Selection.Find
        i = i + 1
        .ClearFormatting
        .Forward = True
        .Text = "�]����[1-9]{1,2}�^"
        .MatchWildcards = True
        .Format = False
        .MatchCase = False
        .MatchWholeWord = False
        .MatchByte = False
        .MatchSoundsLike = False
        .MatchWildcards = True
        .Execute
        If .Found Then
            If Selection.Text = "�]����99�^" Then
                i = 1
            End If
            Selection.Text = "�]����" & CStr(i) & "�^"
            Selection.Move wdCharacter, 1
        End If
        
      End With
    Loop While Selection.Find.Found
    
     
    
End Sub
