' Dim WshShell, expirationDate, currentDate

' expirationDate = DateAdd("d", 2, "08/25/2024")

' currentDate = Date

' If currentDate > expirationDate Then
'    MsgBox "Issue in launching program."
'    WScript.Quit
' End If

' Set WshShell = CreateObject("WScript.Shell")
' WshShell.Run "pythonw C:\Users\ASUS\OneDrive\Desktop\stone_crusher_project\main.py", 0
' Set WshShell = Nothing


Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw C:\Users\ASUS\OneDrive\Desktop\stone_crusher_project\main.py", 0
Set WshShell = Nothing