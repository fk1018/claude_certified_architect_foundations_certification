<#
    Daily launcher. Run from the repo root.

        .\study.ps1                 # Architect - Foundations menu
        .\study.ps1 ccdvf           # Developer - Foundations
        .\study.ps1 ccafc exam short start short-practice-exam-3 --feedback immediate
#>
param(
    [Parameter(Position = 0)] [string] $Track = 'ccafc',
    [Parameter(Position = 1, ValueFromRemainingArguments = $true)] [string[]] $Rest
)

if ($Track -notin @('ccafc', 'ccdvf', 'ccarp')) {
    Write-Host "Unknown track '$Track'. Use ccafc, ccdvf, or ccarp." -ForegroundColor Red
    exit 1
}

$engine = if ($env:STUDY_ENGINE) { $env:STUDY_ENGINE }
          elseif (Get-Command docker -ErrorAction SilentlyContinue) { 'docker' }
          else { 'podman' }

Set-Location $PSScriptRoot

# 2>&1 | Out-Null, not *> $null: Windows PowerShell 5.1 surfaces native stderr as an
# ErrorRecord, and "image not known" here is an expected result, not a failure.
& $engine image inspect claude-cert-study 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Building the image (first run only, a few minutes)...' -ForegroundColor Cyan
    & $engine build -f cli/Dockerfile -t claude-cert-study .
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

& $engine run --rm -it -v "$($PWD.Path):/app" -w /app --entrypoint $Track claude-cert-study @Rest
