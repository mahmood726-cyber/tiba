# Tiba — install local pre-push hook that runs the Cochrane-trademark guard.
# Run from repo root: powershell -ExecutionPolicy Bypass -File scripts\install_pre_push_hook.ps1

$ErrorActionPreference = "Stop"
$repoRoot = git rev-parse --show-toplevel
$hookPath = Join-Path $repoRoot ".git\hooks\pre-push"

$hookBody = @'
#!/usr/bin/env sh
# Tiba pre-push: Cochrane-trademark guard.
# Bypass: SKIP_TIBA_GUARD=1 git push  (logs to .git/tiba-bypass.log)
if [ "$SKIP_TIBA_GUARD" = "1" ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)  bypassed by user" >> "$(git rev-parse --git-dir)/tiba-bypass.log"
  exit 0
fi
exec python "$(git rev-parse --show-toplevel)/scripts/pre_push_cochrane_guard.py"
'@

# Use no-BOM UTF-8 encoding: PowerShell 5.1 -Encoding utf8 produces BOM which
# breaks sh script execution. [System.Text.UTF8Encoding]::new($false) is BOM-free.
[System.IO.File]::WriteAllText($hookPath, $hookBody, [System.Text.UTF8Encoding]::new($false))
Write-Output "Installed pre-push hook at $hookPath"
