$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$outDir = Join-Path $root "assets\portraits"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$headers = @{
  "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  "Accept" = "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
  "Referer" = "https://www.fandom.com/"
}

$portraits = @(
  @{
    Id = "scp-018"
    Urls = @(
      "https://static.wikia.nocookie.net/scp-db/images/7/74/SCP-018.jpg/revision/latest?cb=20241026201314",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-018.jpg"
    )
  },
  @{
    Id = "scp-127"
    Urls = @(
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-127.png",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP127.png",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-127.jpg",
      "https://files.scpfoundation.net/local--files/scp-127/scp-127_1.png",
      "https://static.wikia.nocookie.net/non-aliencreatures/images/6/6a/SCP127.png/revision/latest?cb=20220913095443",
      "https://non-aliencreatures.fandom.com/wiki/Special:FilePath/SCP127.png"
    )
  },
  @{
    Id = "scp-207"
    Urls = @(
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-207.png",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-207.jpg",
      "https://files.scpfoundation.net/local--files/scp-207/SCP207.jpg",
      "https://static.wikia.nocookie.net/scp/images/5/58/SCP-207.png/revision/latest?cb=20140307213958",
      "https://scp.fandom.com/es/wiki/Special:FilePath/SCP-207.png"
    )
  },
  @{
    Id = "scp-244"
    Urls = @(
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-244.png",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-244.gif",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-244.jpg",
      "https://static.wikia.nocookie.net/scp/images/0/08/SCP-244.gif/revision/latest?cb=20210928064940&path-prefix=es",
      "https://scp.fandom.com/es/wiki/Special:FilePath/SCP-244.gif"
    )
  },
  @{
    Id = "scp-268"
    Urls = @(
      "https://static.wikia.nocookie.net/scp-db/images/0/0c/SCP-268.jpg/revision/latest?cb=20230724013743",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-268.jpg"
    )
  },
  @{
    Id = "scp-1576"
    Urls = @(
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-1576.png",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-1576.jpg",
      "https://scp-db.fandom.com/wiki/Special:FilePath/Vinyl_Records_by_cmac71-d42zh85.jpg",
      "https://files.scpfoundation.net/local--files/scp-1576/1576.jpg",
      "https://static.wikia.nocookie.net/fundacao-scp/images/2/22/Vinyl_Records_by_cmac71-d42zh85_%281%29.jpg/revision/latest?cb=20200815024149&path-prefix=pt-br",
      "https://fundacao-scp.fandom.com/pt/wiki/Special:FilePath/Vinyl_Records_by_cmac71-d42zh85_(1).jpg"
    )
  },
  @{
    Id = "scp-1853"
    Urls = @(
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-1853.jpg",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-1853.png",
      "https://files.scpfoundation.net/local--files/scp-1853/exp0003-new.png",
      "https://static.wikia.nocookie.net/scp/images/2/26/SCP-1853.jpg/revision/latest?cb=20200913152705",
      "https://scp.fandom.com/es/wiki/Special:FilePath/SCP-1853.jpg"
    )
  },
  @{
    Id = "scp-2176"
    Urls = @(
      "https://static.wikia.nocookie.net/scp-db/images/a/a7/SCP-2176.png/revision/latest?cb=20221206045025",
      "https://scp-db.fandom.com/wiki/Special:FilePath/SCP-2176.png"
    )
  }
)

foreach ($portrait in $portraits) {
  $target = Join-Path $outDir "$($portrait.Id).png"
  $temp = "$target.download"
  Write-Host "Downloading $($portrait.Id) ..."
  $downloaded = $false
  foreach ($url in $portrait.Urls) {
    try {
      Invoke-WebRequest -Uri $url -Headers $headers -MaximumRedirection 8 -OutFile $temp
      if ((Get-Item $temp).Length -ge 1024) {
        $downloaded = $true
        break
      }
    } catch {
      if (Test-Path $temp) {
        Remove-Item $temp -Force
      }
    }
  }

  if (-not $downloaded) {
    if (Test-Path $temp) {
      Remove-Item $temp -Force
    }
    Write-Warning "Could not download $($portrait.Id) from any known Fandom source."
    continue
  }

  Move-Item -Force $temp $target
}

Write-Host "Done. Portraits saved to $outDir"
