; ==============================================================================
; FLUX VPN — Script Oficial de Compilação do Instalador Windows (.EXE)
; Padrão Ouro da Indústria para Windows (Inno Setup Compiler)
; Cria instalador profissional com assistente, ícone na Área de Trabalho e Desinstalador
; ==============================================================================

#define MyAppName "FLUX VPN"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "FLUX Open Source Team"
#define MyAppURL "https://github.com/cadubezerrapro/fluxvpn"
#define MyAppExeName "FLUX-VPN.vbs"
#define MyAppIconName "fluxvpn.ico"

[Setup]
AppId={{9F82A4D1-5C3E-4B7A-9D2E-7E1A4F8B0C3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\dist
OutputBaseFilename=FLUX-VPN-Windows-Setup
SetupIconFile=..\dist\windows\fluxvpn.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\windows\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "wscript.exe"; Parameters: """{app}\{#MyAppExeName}"""; IconFilename: "{app}\{#MyAppIconName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "wscript.exe"; Parameters: """{app}\{#MyAppExeName}"""; IconFilename: "{app}\{#MyAppIconName}"; Tasks: desktopicon

[Run]
Filename: "wscript.exe"; Parameters: """{app}\{#MyAppExeName}"""; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: postinstall nowait skipifsilent
