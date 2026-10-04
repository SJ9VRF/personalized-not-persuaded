# Git History

The project release originally existed as a verified snapshot without a public commit history. I do **not** backfill or fabricate earlier commits.

A real local Git history begins with:

> `import verified project snapshot`

Evidence-layer work is committed incrementally from that point forward. The release includes:

- `artifacts/evidence/git/git-log.txt` — human-readable commit log;
- `artifacts/evidence/git/personalized-not-persuaded-history.bundle` — a Git bundle that preserves the actual local commit graph;
- `artifacts/evidence/git/README.md` — instructions and the commit-metadata boundary.

The local commits use author name **Aura Yavary** and a non-routable `.invalid` email address only because Git requires an email field. The bundle does not imply a public GitHub history or any pre-existing commit chronology.
