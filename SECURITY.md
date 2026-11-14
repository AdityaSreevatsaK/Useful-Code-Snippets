# Security policy

## Reporting vulnerabilities

Please report sensitive security concerns privately through the repository's
GitHub security-advisory reporting feature if it is enabled, or contact the
repository owner privately. Do not post secrets, exploit payloads, private
files, or vulnerability details in public issues.

## Credentials and history

No API credentials or encryption keys belong in Git or in the public
Hugging Face Space metadata. Use GitHub Actions secrets or trusted runtime
secret storage. A previously public Fernet-style `secret.key` was deleted
from the current branch, but remains in Git history.

If that key was used, assume compromise. Locate the affected encrypted data,
arrange a new key in a private secret store, and re-encrypt the data. Do not
delete the old key prematurely if it is needed to recover data.

A complete history rewrite is disruptive to every clone, fork and the Space's
Git mirror. Coordinate it separately, with explicit approval and a recovery
plan. Even after rewriting, credentials should always be rotated.

## Controls

Privileged server-side tools require `ENABLE_LOCAL_OPERATIONS=1` and must
never be enabled on the publicly accessible Space. ZIP uploads are bounded
and validated. All uploaded data is untrusted and conversion utilities should
run with resource and network isolation. See
[security and testing notes](docs/SECURITY_AND_TESTING.md).
