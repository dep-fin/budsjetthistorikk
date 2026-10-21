[CmdletBinding(SupportsShouldProcess)]
param(
    [ValidateSet('Inspect', 'Install')][string]$Mode = 'Inspect',
    [Parameter(Mandatory)][string]$ExpectedHost,
    [Parameter(Mandatory)][string]$TaskName,
    [Parameter(Mandatory)][string]$ConfigPath,
    [Parameter(Mandatory)][string]$PythonPath,
    [Parameter(Mandatory)][string]$WorkingDirectory,
    [Parameter(Mandatory)][string]$Account,
    [Parameter(Mandatory)][string]$TaskXmlPath,
    [datetime]$StartDate = (Get-Date),
    [pscredential]$Credential,
    [switch]$BackgroundAccessVerified
)

$ErrorActionPreference = 'Stop'
# Kun eksplisitt angitt varig Windows-vert. Ingen remoting, konto-/credentialopprettelse.
if ($env:COMPUTERNAME -ne $ExpectedHost) { throw 'Dette er ikke avtalt driftsvert.' }
if ((Get-TimeZone).Id -ne 'W. Europe Standard Time') {
    throw 'Verten må bruke norsk lokaltid: W. Europe Standard Time. Endres ikke av dette skriptet.'
}
$TaskConfigPath = (Resolve-Path -LiteralPath $ConfigPath).Path
$TaskPythonPath = (Resolve-Path -LiteralPath $PythonPath).Path
$TaskWorkingDirectory = (Resolve-Path -LiteralPath $WorkingDirectory).Path
$TaskConfig = Get-Content -LiteralPath $TaskConfigPath -Raw | ConvertFrom-Json
foreach ($TaskDataPath in @($TaskConfig.database, $TaskConfig.output_directory)) {
    if ($TaskDataPath -notmatch '^[a-zA-Z]:\\' -or $TaskDataPath.StartsWith('\\')) {
        throw 'Driftslageret må være en eksplisitt lokal diskbane, ikke UNC/nettverkslager.'
    }
}
if ($Mode -eq 'Inspect') {
    # Lesing kan kreve lokal CIM-/Task Scheduler-tilgang. En feil er ikke bevis på fravær.
    Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State
    Get-ScheduledTaskInfo -TaskName $TaskName | Select-Object LastRunTime, LastTaskResult, NextRunTime
    Export-ScheduledTask -TaskName $TaskName
    return
}
if (-not $BackgroundAccessVerified -or -not $Credential) {
    throw 'Install krever lokalt bekreftet bakgrunnstilgang og eksisterende kontos Credential.'
}
if ($Credential.UserName -ne $Account) { throw 'Credential må gjelde den avtalte driftskontoen.' }
if (Test-Path -LiteralPath $TaskXmlPath) { throw 'Bruk et nytt XML-filnavn for gjennomgang.' }
Push-Location -LiteralPath $TaskWorkingDirectory
try {
    & $TaskPythonPath -m drift --config $TaskConfigPath --task-xml $TaskXmlPath `
        --python $TaskPythonPath --working-directory $TaskWorkingDirectory `
        --account $Account --start-date $StartDate.ToString('yyyy-MM-dd')
    if ($LASTEXITCODE -ne 0) { throw 'Task XML kunne ikke genereres.' }
} finally { Pop-Location }
# Register uten -Force: en eksisterende jobb erstattes aldri. Ingen passord logges/lagres i fil.
if ($PSCmdlet.ShouldProcess("$ExpectedHost/$TaskName", 'Registrer gjennomgått daglig oppgave')) {
    $TaskXml = Get-Content -LiteralPath $TaskXmlPath -Raw
    Register-ScheduledTask -TaskName $TaskName -Xml $TaskXml -User $Account `
        -Password $Credential.GetNetworkCredential().Password | Select-Object TaskName, State
}
