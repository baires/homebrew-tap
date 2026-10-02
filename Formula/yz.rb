class Yz < Formula
  desc "Instant file sharing via Cloudflare R2"
  homepage "https://github.com/baires/yz"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.1.1/yz_v0.1.1_darwin_arm64"
      sha256 "5b60d31aee268d700d8e4d2798ac5a7ff672b1c237196b2ece4d52b8c89f7d40"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.1.1/yz_v0.1.1_darwin_amd64"
      sha256 "7d120c66743f74ecbdd907ec74466628f7a699c66392dc0ac9220311f57078c9"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.1.1/yz_v0.1.1_linux_arm64"
      sha256 "92ad17b45b95d5c7e7a9de8b59d53e0b1fc0928ab208493f65e10d6be79a4747"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.1.1/yz_v0.1.1_linux_amd64"
      sha256 "2f9f53c664a7dacc499cf688676a6b5de8e78d56c47fd075a36dae29f6777cc6"
    end
  end

  def install
    bin.install Dir["yz_*"].first => "yz"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/yz version")
  end
end
