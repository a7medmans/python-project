; Inno Setup Script for PDFPageRemover
; يحتاج تثبيت Inno Setup من: https://jrsoftware.org/isdl.php

#define MyAppName "PDFPageRemover"
#define MyAppVersion "1.0"
#define MyAppPublisher "PDFPageRemover"
#define MyAppExeName "PDFPageRemover.exe"
#define MyAppDescription "أداة متقدمة لمعالجة ملفات PDF - حذف، دمج، استخراج، تدوير الصفحات والمزيد"

[Setup]
; معلومات التطبيق الأساسية
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
AppDescription={#MyAppDescription}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppDescription}
VersionInfoCopyright=Copyright (C) 2025

; إعدادات التثبيت
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer_output
OutputBaseFilename=PDFPageRemover_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=no
DisableReadyPage=no
DisableFinishedPage=no
DisableWelcomePage=no

; معلومات إضافية
MinVersion=6.1
WizardImageFile=
WizardSmallImageFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startmenu"; Description: "إضافة إلى قائمة Start"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "dist\PDFPageRemover.exe"; DestDir: "{app}"; Flags: ignoreversion
; يمكن إضافة ملفات إضافية هنا
; Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "أداة معالجة ملفات PDF"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; Comment: "إلغاء تثبيت {#MyAppName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "أداة معالجة ملفات PDF"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; Comment: "أداة معالجة ملفات PDF"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; Check: not WizardIsComponentSelected('desktopicon')

[Registry]
; إضافة معلومات في السجل (اختياري)
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[Code]
procedure InitializeWizard;
begin
  // تخصيص نصوص الواجهة
  WizardForm.WelcomeLabel1.Caption := 'مرحباً بك في برنامج ' + ExpandConstant('{#MyAppName}');
  WizardForm.WelcomeLabel2.Caption := 'سيقوم هذا المعالج بتثبيت ' + ExpandConstant('{#MyAppName}') + ' على جهازك.' + #13#10 + #13#10 + ExpandConstant('{#MyAppDescription}');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // يمكن إضافة إجراءات إضافية بعد التثبيت هنا
  end;
end;
