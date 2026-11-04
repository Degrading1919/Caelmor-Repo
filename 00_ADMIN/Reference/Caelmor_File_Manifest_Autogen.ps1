# Read-only tracked-file inventory for the designated Caelmor checkout.
# The curated File Manifest remains the placement guide.

$CheckoutRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$TrackedRoot = git -C $CheckoutRoot rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ((Resolve-Path -LiteralPath $TrackedRoot).Path -ne $CheckoutRoot) {
    throw 'Run this script from the Caelmor repository.'
}

git -C $CheckoutRoot -c core.quotePath=false ls-files --cached
exit $LASTEXITCODE
