# Repository instructions

## Commit authorship

For owner-directed work, new commits must use
`Boris Abuzov <ai.sec.boris@gmail.com>` (GitHub identity: `boris-ai-sec`).

Automated implementation tools are tools, not repository contributors by
default. Unless the repository owner explicitly requests otherwise, do not use
an automated implementation tool as commit author, committer where controllable,
co-author, bot co-author, or attribution trailer. Do not add automated-tool
attribution trailers.

Before committing, verify:

```sh
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

After committing, verify `git show -s --format=fuller HEAD` and inspect commit
trailers before push or merge.

Do not rewrite existing history merely to normalize authorship or change or
erase attribution belonging to another human contributor. Preserve published
tags, releases, historical evidence, provenance records, and checksum manifests.
