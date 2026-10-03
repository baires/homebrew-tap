class Yz < Formula
  desc "Instant file sharing via Cloudflare R2"
  homepage "https://github.com/baires/yz"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.3.0/yz_v0.3.0_darwin_arm64"
      sha256 "8bb67b6faf2157bbbdfb23e07dd726390d5b7ded78e7c277f0352b2862940752"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.3.0/yz_v0.3.0_darwin_amd64"
      sha256 "f294ded3e8edf122d42a92251982b3f4fe2d4dd0e9895925ca55d8b5e3fba9d3"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.3.0/yz_v0.3.0_linux_arm64"
      sha256 "8561d7fa4d10950b34718ebebd5220b51a66ee10de231ad0d10ea85dbec4ac12"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.3.0/yz_v0.3.0_linux_amd64"
      sha256 "6bd55f2876c2bcff977da77b1935c8650a72bcdcf34fc05f880e3dd28d313110"
    end
  end

  def install
    bin.install Dir["yz_*"].first => "yz"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/yz version")
  end
end
