"""Update the formula from a complete yz GitHub release.

Set YZ_TAG to a stable tag (v1.2.3) to use that release. When it is unset,
the latest stable release is used. The formula file is replaced only after
every asset and checksum is present, so a partial release leaves it untouched.
"""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

FORMULA = Path("Formula/yz.rb")
TAG_RE = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+")
SHA_RE = re.compile(r"[0-9a-f]{64}")
PLATFORMS = ("darwin", "linux")
ARCHES = ("arm64", "amd64")


def fail(message):
    raise SystemExit(message)


def fetch(url):
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        fail("GH_TOKEN is required")
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "baires-homebrew-tap",
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        fail(f"GitHub request failed ({error.code}) for {url}")


def asset_name(tag, os_name, arch):
    return f"yz_{tag}_{os_name}_{arch}"


def release_api_url(tag):
    if tag:
        return f"https://api.github.com/repos/baires/yz/releases/tags/{tag}"
    return "https://api.github.com/repos/baires/yz/releases/latest"


def parse_checksums(text):
    hashes = {}
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        if len(parts) < 2 or not SHA_RE.fullmatch(parts[0]):
            fail("checksums.txt is incomplete or malformed")
        hashes[parts[1]] = parts[0]
    return hashes


def binary_names(tag):
    return [asset_name(tag, os_name, arch) for os_name in PLATFORMS for arch in ARCHES]


def require_assets(release, tag):
    assets = {asset["name"]: asset for asset in release.get("assets") or []}
    names = binary_names(tag)
    missing = []
    for name in ["checksums.txt", *names]:
        asset = assets.get(name)
        if asset is None or asset.get("state") != "uploaded" or not asset.get("size"):
            missing.append(name)
    if missing:
        fail("Release assets are incomplete: " + ", ".join(missing))
    return assets, names


def formula_text(tag, assets, hashes):
    lines = [
        "class Yz < Formula",
        '  desc "Instant file sharing via Cloudflare R2"',
        '  homepage "https://github.com/baires/yz"',
        '  license "Apache-2.0"',
        "",
    ]
    for os_name, block in [("darwin", "macos"), ("linux", "linux")]:
        lines += [f"  on_{block} do"]
        for arch, condition in [("arm64", "arm"), ("amd64", "intel")]:
            name = asset_name(tag, os_name, arch)
            digest = hashes.get(name, "")
            if not SHA_RE.fullmatch(digest):
                fail("Release assets are incomplete: missing checksum for " + name)
            url = assets[name].get("browser_download_url") or ""
            expected = f"https://github.com/baires/yz/releases/download/{tag}/{name}"
            if url != expected:
                fail("Unexpected asset URL")
            lines += [
                f"    on_{condition} do",
                f'      url "{url}"',
                f'      sha256 "{digest}"',
                "    end",
            ]
            if arch == "arm64":
                lines += [""]
        lines += ["  end", ""]
    lines += [
        "  def install",
        '    bin.install Dir["yz_*"].first => "yz"',
        "  end",
        "",
        "  test do",
        '    assert_match version.to_s, shell_output("#{bin}/yz version")',
        "  end",
        "end",
    ]
    return "\n".join(lines) + "\n"


def write_formula(content):
    temporary = FORMULA.with_suffix(".rb.tmp")
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, FORMULA)
    finally:
        if temporary.exists():
            temporary.unlink()


def requested_tag():
    tag = os.environ.get("YZ_TAG", "").strip()
    if tag.startswith("refs/tags/"):
        tag = tag[len("refs/tags/") :]
    if tag and not TAG_RE.fullmatch(tag):
        fail("Expected a stable semantic version")
    return tag


def main():
    requested = requested_tag()
    try:
        release = json.loads(fetch(release_api_url(requested)))
    except json.JSONDecodeError:
        fail("GitHub release response was not valid JSON")
    tag = release.get("tag_name") or ""
    if requested and tag != requested:
        fail("Release tag does not match the requested tag")
    if not TAG_RE.fullmatch(tag):
        fail("Expected a stable semantic version")
    assets, names = require_assets(release, tag)
    try:
        checksums = fetch(assets["checksums.txt"]["browser_download_url"]).decode()
    except UnicodeDecodeError:
        fail("checksums.txt is incomplete or malformed")
    hashes = parse_checksums(checksums)
    missing = [name for name in names if not SHA_RE.fullmatch(hashes.get(name, ""))]
    if missing:
        fail("Release assets are incomplete: missing checksum for " + ", ".join(missing))
    content = formula_text(tag, assets, hashes)
    write_formula(content)
    print(f"Updating formula for {tag}", flush=True)


if __name__ == "__main__":
    main()
