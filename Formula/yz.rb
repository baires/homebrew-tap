class Yz < Formula
  desc "Instant file sharing via Cloudflare R2"
  homepage "https://github.com/baires/yz"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.5.0/yz_v0.5.0_darwin_arm64"
      sha256 "145a2b044ffa7b122d11c8ee85cf145d65661ab3e806c6d3f34f19c15559d2b2"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.5.0/yz_v0.5.0_darwin_amd64"
      sha256 "a3f44c15c192afd56c32a65e7239224f17031408a4b6a2b947666e5388ab076d"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.5.0/yz_v0.5.0_linux_arm64"
      sha256 "42a462931cfa227bf301b30650f63203543f2178e3818c258182e56def3566c7"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.5.0/yz_v0.5.0_linux_amd64"
      sha256 "d6c9d933955823b3874634b82de3e1809a10347edbc8c4f6e21cb33bf6c0a3a8"
    end
  end

  def install
    bin.install Dir["yz_*"].first => "yz"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/yz version")
  end
end
