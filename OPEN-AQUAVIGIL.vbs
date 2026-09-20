Set shell = CreateObject("WScript.Shell")
Set files = CreateObject("Scripting.FileSystemObject")
folder = files.GetParentFolderName(WScript.ScriptFullName)
MsgBox "AquaVigil is starting. Docker Desktop may take up to three minutes on the first launch. The browser will open automatically.", 64, "AquaVigil"
command = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & folder & "\start-aquavigil.ps1"""
exitCode = shell.Run(command, 0, True)
If exitCode <> 0 Then
  MsgBox "AquaVigil could not start. Open START-AQUAVIGIL.cmd once to see the detailed error.", 16, "AquaVigil"
End If
