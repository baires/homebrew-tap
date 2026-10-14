class Yz < Formula
  desc "Instant file sharing via Cloudflare R2"
  homepage "https://github.com/baires/yz"
  license "Apache-2.0"

  on_macos do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.4.0/yz_v0.4.0_darwin_arm64"
      sha256 "dab72e0a1cdd61b58fa96599d047dc18fbb53660499f972aba9b22103416ed1d"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.4.0/yz_v0.4.0_darwin_amd64"
      sha256 "7dd99ee6b429dc168a31155cab4a34729138e8f2354ec2fc718055708a5a1005"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/baires/yz/releases/download/v0.4.0/yz_v0.4.0_linux_arm64"
      sha256 "b047f2154fe43be69c5c3dd208a577e2d2e84dd8c644242ee9fcaee7bf6a701d"
    end

    on_intel do
      url "https://github.com/baires/yz/releases/download/v0.4.0/yz_v0.4.0_linux_amd64"
      sha256 "de212d86bc3499b511b327630c185cad82b757a8a30049b2c466391f5b5da278"
    end
  end

  def install
    bin.install Dir["yz_*"].first => "yz"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/yz version")
  end
end
