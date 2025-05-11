 [Setup]
AppName=M3 Scoreboard
AppVersion=1.5
DefaultDirName={pf}\M3 Scoreboard
DefaultGroupName=M3 Scoreboard
OutputBaseFilename=M3_Scoreboard_Installer_V1.5
OutputDir=output
Compression=lzma
SolidCompression=yes
SetupIconFile=app_icon.ico
UninstallDisplayIcon={app}\M3_Scoreboard.exe
ArchitecturesInstallIn64BitMode=x64

[Files]
; Include the main EXE and all required files
Source: "dist\M3 Scoreboard.exe"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\M3 Scoreboard"; Filename: "{app}\M3_Scoreboard.exe"
Name: "{group}\Uninstall M3 Scoreboard"; Filename: "{uninstallexe}"
Name: "{userdesktop}\M3 Scoreboard"; Filename: "{app}\M3_Scoreboard.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\M3_Scoreboard.exe"; Description: "Launch M3 Scoreboard"; Flags: nowait postinstall skipifsilent
