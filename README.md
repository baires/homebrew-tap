# Homebrew tap

Formulae for tools published by [baires](https://github.com/baires).

## dynocap

```sh
brew install baires/tap/dynocap
```

On Homebrew 6 that command trusts this formula. To use the short name
`dynocap` for a later upgrade, run `brew trust --formula baires/tap/dynocap`.

Apple Silicon and macOS Ventura or newer. The formula downloads the versioned
release archive, checks its SHA-256, and re-signs the CLI on your Mac. Intel
is refused. There is no bottle.

A dynocap GitHub Release sends a `dynocap-release` repository dispatch, which
updates `Formula/dynocap.rb` and pushes the change to `main`. The workflow can
also be run manually. The versioned archive and its `.sha256` file must both
be present; otherwise the run fails.

The formula checked in before the first release points at `v0.0.0` so the
install name exists. The first stable release replaces that URL and checksum.

## yz

Install:

```sh
brew install baires/tap/yz
```

Supports macOS and Linux on Intel and ARM64. Downloads the upstream
release binary and verifies its SHA-256 checksum.

A yz GitHub Release sends a `yz-release` repository dispatch, which
updates `Formula/yz.rb` and pushes the change to `main` immediately.
The hourly check is the backup, and the workflow can still be run
manually. All four assets and valid checksums must be present;
otherwise the run fails and a later check retries.
