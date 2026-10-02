"""Update the formula from the latest complete yz GitHub release."""
import json
import os
import re
import urllib.request
from pathlib import Path

def fetch(url):
    request = urllib.request.Request(url, headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request) as response:
        return response.read()

release = json.loads(fetch("https://api.github.com/repos/baires/yz/releases/latest"))
tag = release["tag_name"]
if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
    raise ValueError("Expected a stable semantic version")
assets = {asset["name"]: asset for asset in release["assets"]}
checksums = fetch(assets["checksums.txt"]["browser_download_url"]).decode()
hashes = {line.split()[1]: line.split()[0] for line in checksums.splitlines()}
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
        name = f"yz_{tag}_{os_name}_{arch}"
        digest = hashes[name]
        if not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("Invalid SHA-256")
        url = assets[name]["browser_download_url"]
        if url != f"https://github.com/baires/yz/releases/download/{tag}/{name}":
            raise ValueError("Unexpected asset URL")
        lines += [f"    on_{condition} do", f'      url "{url}"', f'      sha256 "{digest}"', "    end"]
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
Path("Formula/yz.rb").write_text("\n".join(lines) + "\n")
