# Pushing this to GitHub

The repository is already initialised and committed locally. Nothing here is
pushed yet — this session's GitHub token is scoped to pre-attached repositories
and cannot create new ones.

## Create the repo and push

With the GitHub CLI:

```bash
gh repo create phr0zt/t1d-info --public --source=. --remote=origin --push
```

Or, if you prefer to create it in the browser first (github.com/new → `t1d-info`,
no README, no .gitignore, no licence):

```bash
git remote add origin git@github.com:phr0zt/t1d-info.git
git branch -M main
git push -u origin main
```

Use `https://github.com/phr0zt/t1d-info.git` instead of the SSH URL if you
authenticate over HTTPS.

## Rebuilding a deck from this repo

Each folder under `decks/` is already in the exact layout the Slides artifact type
expects. To republish one, point the artifact at that folder as the root and send
`project/deck.json` plus every file under `project/slides/`.

To merge decks into a new archive, prefix each slide id (and the matching
`<section id="...">`) so ids stay unique, then concatenate the `order` arrays with a
blank divider between each deck — that is exactly how `06-portable-archive` was built.
