param(
    [string]$Repository = 'ziki0621/cantonese-lm-eye-tracking'
)

$ErrorActionPreference = 'Stop'
$releaseRoot = $PSScriptRoot
if ($Repository -notmatch '^ziki0621/[a-zA-Z0-9_.-]+$') {
    throw 'Choose a repository name under ziki0621.'
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'Install GitHub CLI from https://cli.github.com/ first.'
}
& gh auth status --hostname github.com
if ($LASTEXITCODE -ne 0) {
    throw 'Complete gh auth login -h github.com, then run this script again. Do not place credentials in this repository.'
}
if (-not (Test-Path -LiteralPath (Join-Path $releaseRoot '.git'))) {
    throw 'The prepared local Git repository is missing.'
}
$changes = & git -c "safe.directory=$releaseRoot" -C $releaseRoot status --porcelain
if ($LASTEXITCODE -ne 0 -or $changes) {
    throw 'Review and commit local changes before publishing.'
}
$remoteUrl = & git -c "safe.directory=$releaseRoot" -C $releaseRoot config --get remote.origin.url
if ($LASTEXITCODE -eq 0 -and $remoteUrl) {
    if ($remoteUrl -notin @("https://github.com/$Repository.git", "https://github.com/$Repository", "git@github.com:$Repository.git")) {
        throw 'The existing origin does not match the requested destination.'
    }
} else {
    & gh repo create $Repository --public `
        --description 'PACLIC 2026: Cantonese language models, information-theoretic metrics, and MCFIX eye-tracking prediction.'
    if ($LASTEXITCODE -ne 0) {
        throw 'The remote repository could not be created. No files have been uploaded.'
    }
    & git -c "safe.directory=$releaseRoot" -C $releaseRoot remote add origin "https://github.com/$Repository.git"
    if ($LASTEXITCODE -ne 0) {
        throw 'The repository was created, but origin could not be configured.'
    }
}
& git -c "safe.directory=$releaseRoot" -C $releaseRoot push -u origin main
if ($LASTEXITCODE -ne 0) {
    throw 'GitHub publication did not complete. Inspect the command output before retrying.'
}
& gh repo view $Repository --json nameWithOwner,url,visibility
if ($LASTEXITCODE -ne 0) {
    throw 'Unable to verify the remote repository.'
}
