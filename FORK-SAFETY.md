# Restricted owner fork

Base reviewed: `9268bf91cb64955bbb1de649d74b828ae7ba925e`.

## Changes

- Import is disabled: all four import helpers fail with exit 78 without filesystem or network operations. The skill no longer contains the import workflow.
- Reprint is disabled: its previous workflow, including interpolation of research data into Python code, is removed.
- Global skill updates in the main skill preflight are disabled so they cannot restore the upstream skills through that path.

The two disabled skills match the local blockers used by the owner in Claude and Codex. The shell blockers require only a POSIX shell.

## Limits

This is a restricted development branch, not a release or full installation approval. Other upstream installers and update paths have not been hardened. Do not follow upstream installation commands to install this branch. Instruction-level restrictions are not an OS sandbox. Manually running an upstream copy or replacing the blockers bypasses these restrictions.

Still open from the earlier audit: unrestricted documentation fetch/redirects, external OpenAPI references, publication scrubbing concerns, and incomplete dependency review. This change does not fix or dismiss those findings. Full installation requires further work and a new audit.

## Verification

Run `python3 tests/test_disabled_owner_skills.py`. The test executes only the newly written fail-closed helpers, never upstream import code. It checks refusal and preservation of files for valid names, traversal, absolute paths, symlink names, empty input, and injection-like input. Go tests are outside this shell/documentation change and have not been run.
