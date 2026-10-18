' ==============================================================================
' FLUX VPN — Lançador Silencioso para Windows
' Evita abertura de janela preta do Prompt de Comando (CMD)
' ==============================================================================

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

strCurDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
strBatPath = strCurDir & "\Iniciar FLUX VPN (Windows).bat"

' Executa em modo oculto (0 = oculto, False = não bloqueante)
objShell.Run "cmd.exe /c """ & strBatPath & """", 0, False
