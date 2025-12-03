$csvPath = "data/tools.csv"
$contentPath = "content"

# Import CSV with UTF8 encoding
$tools = Import-Csv -Path $csvPath -Delimiter "," -Encoding UTF8

foreach ($tool in $tools) {
    $categorySlug = $tool.category.ToLower()
    $targetDir = Join-Path $contentPath $categorySlug
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }

    $filePath = Join-Path $targetDir ($tool.slug + ".md")
    
    # Prepare Frontmatter
    $title = $tool.name -replace '"', '\"'
    $description = $tool.description_short -replace '"', '\"'
    
    # Handle special case for tl;dv in cons/pros to avoid splitting
    $pros = $tool.pros.Replace('tl;dv', 'tl__dv').Replace(';', '<br>').Replace('tl__dv', 'tl;dv')
    $cons = $tool.cons.Replace('tl;dv', 'tl__dv').Replace(';', '<br>').Replace('tl__dv', 'tl;dv')

    # Safe characters for headers to avoid encoding issues in PS5.1
    $headerWhat = "O que $([char]0x00E9)?"      # é
    $headerPrice = "Pre$([char]0x00E7)o"        # ç
    $headerPros = "Pr$([char]0x00F3)s e Contras" # ó

    $frontmatter = @"
---
title: "$title"
date: $(Get-Date -Format "yyyy-MM-dd")
draft: false
description: "$description"
tags: ["$($tool.category)", "IA", "Software"]
categories: ["$($tool.category)"]
author: "Geode Team"
cover:
    image: ""
    alt: "$title logo"
    caption: ""
    relative: false
---

# $title

**Veredito:** $($tool.verdict)

## $headerWhat
$($tool.description_short)

## $headerPrice
**Modelo:** $($tool.price_model)

## $headerPros
| Pr$([char]0x00F3)s | Contras |
| :--- | :--- |
| $pros | $cons |

## Para quem $([char]0x00E9) indicado?
$($tool.verdict)

[Visitar Site Oficial]($($tool.website_url))
"@

    # Write file with UTF8 encoding
    $frontmatter | Set-Content -Path $filePath -Encoding UTF8
    Write-Host "Generated: $filePath"
}
