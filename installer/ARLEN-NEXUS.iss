#define MyAppName "ARLEN NEXUS"
#define MyAppVersion "0.7.0"
#define MyAppPublisher "Jubaer Hossain"
#define MyAppExeName "ARLEN NEXUS.exe"

[Setup]
AppId={{D29129A2-FA24-4A80-9C55-4F7F0A3E52C1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\ARLEN NEXUS
DefaultGroupName=ARLEN NEXUS
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\installer-output
OutputBaseFilename=ARLEN-NEXUS-Setup-v0.7
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\\assets\\arlen-nexus.ico
SetupLogging=yes
UninstallDisplayName=ARLEN NEXUS
CloseApplications=yes
RestartApplications=no
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
VersionInfoVersion=0.7.0.0
VersionInfoCompany=Jubaer Hossain
VersionInfoDescription=ARLEN NEXUS Offline-First Personal Intelligence Environment
VersionInfoProductName=ARLEN NEXUS
VersionInfoProductVersion=0.7.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\ARLEN NEXUS Portable\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ARLEN NEXUS"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\ARLEN NEXUS"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch ARLEN NEXUS"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
