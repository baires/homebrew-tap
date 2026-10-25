# Homebrew tap for yz

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
