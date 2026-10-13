# Tutora AI - Screenshot processor and Slideshow SVG builder
Add-Type -AssemblyName System.Drawing

$ErrorActionPreference = "Stop"

$workspaceRoot = "z:\Recordly-main"
$publicRoot = "z:\Recordly-main\tutora-ai-public"
$srcDir = Join-Path $workspaceRoot "public\Screenshost"
$shotsDir = Join-Path $publicRoot "assets\screenshots"
$animDir = Join-Path $publicRoot "assets\animations"

if (-not (Test-Path $shotsDir)) { New-Item -ItemType Directory -Path $shotsDir -Force | Out-Null }
if (-not (Test-Path $animDir)) { New-Item -ItemType Directory -Path $animDir -Force | Out-Null }

$slidesConfig = @(
    @{
        File = "01-dashboard.png"
        Src = "Screenshot (676).png"
        Title = "Studio Dashboard"
        Icon = [char]::ConvertFromUtf32(0x1F4CA)
        Subtitle = "Recordings, drafts & narration pipelines in one clean workspace"
    },
    @{
        File = "02-capture-launcher.png"
        Src = "Screenshot (677).png"
        Title = "Floating Capture Launcher"
        Icon = [char]::ConvertFromUtf32(0x1F680)
        Subtitle = "Precision window, area select, mic audio and webcam toggles"
    },
    @{
        File = "03-ai-models-hub.png"
        Src = "Screenshot (678).png"
        Title = "Universal AI Model Hub"
        Icon = [char]::ConvertFromUtf32(0x26A1)
        Subtitle = "Bring Your Own Key: Gemini, Groq, OpenRouter, OpenAI, Claude with failover"
    },
    @{
        File = "04-multitrack-editor.png"
        Src = "Screenshot (679).png"
        Title = "Multi-Track Video Timeline"
        Icon = [char]::ConvertFromUtf32(0x1F3AC)
        Subtitle = "Screen, mic voiceover, webcam bubble, and dynamic keynote intro/outro"
    },
    @{
        File = "05-ai-tutorial-studio.png"
        Src = "Screenshot (680).png"
        Title = "AI Tutorial Studio"
        Icon = [char]::ConvertFromUtf32(0x1F399)
        Subtitle = "Step-by-step narration powered by embedded Kokoro + Resona neural TTS"
    },
    @{
        File = "06-cursor-physics.png"
        Src = "Screenshot (681).png"
        Title = "Cursor Polish & Spring Physics"
        Icon = [char]::ConvertFromUtf32(0x1F3AF)
        Subtitle = "Smoothed paths, click shockwaves, bounce effects, and 4.0x size scale"
    },
    @{
        File = "07-camera-frame-styling.png"
        Src = "Screenshot (682).png"
        Title = "Camera & Canvas Styling"
        Icon = [char]::ConvertFromUtf32(0x1F5BC)
        Subtitle = "16:9 / 9:16 / 1:1 aspect ratios, outer canvas padding and rounded corners"
    },
    @{
        File = "08-webcam-bubble.png"
        Src = "Screenshot (683).png"
        Title = "Dynamic Webcam Bubble"
        Icon = [char]::ConvertFromUtf32(0x1F4F9)
        Subtitle = "Zoom-reactive facecam bubble in circle or pill layout that never hides UI"
    },
    @{
        File = "09-auto-captions.png"
        Src = "Screenshot (684).png"
        Title = "Animated Captions & Subtitles"
        Icon = [char]::ConvertFromUtf32(0x1F4AC)
        Subtitle = "Fade, Slide, Bounce, and Pop word-level subtitles with token styles"
    },
    @{
        File = "10-export-settings.png"
        Src = "Screenshot (685).png"
        Title = "Production Export Studio"
        Icon = [char]::ConvertFromUtf32(0x2699)
        Subtitle = "Crisp 4K/1080p, 60fps rendering, hardware NVENC encoding, and MP4/WebM"
    }
)

Write-Host "1. Copying real screenshots..."
foreach ($s in $slidesConfig) {
    $srcPath = Join-Path $srcDir $s.Src
    $dstPath = Join-Path $shotsDir $s.File
    Copy-Item $srcPath $dstPath -Force
    Write-Host "   Copied: $($s.Src) -> $($s.File)"
}

# Also maintain backward-compatible legacy filenames
Copy-Item (Join-Path $shotsDir "01-dashboard.png") (Join-Path $shotsDir "dashboard.png") -Force
Copy-Item (Join-Path $shotsDir "03-ai-models-hub.png") (Join-Path $shotsDir "ai-models-settings.png") -Force
Copy-Item (Join-Path $shotsDir "04-multitrack-editor.png") (Join-Path $shotsDir "editor-keynote-intro.png") -Force
Copy-Item (Join-Path $shotsDir "05-ai-tutorial-studio.png") (Join-Path $shotsDir "ai-tutorial-studio.png") -Force
Copy-Item (Join-Path $shotsDir "06-cursor-physics.png") (Join-Path $shotsDir "cursor-polish-physics.png") -Force
Copy-Item (Join-Path $shotsDir "08-webcam-bubble.png") (Join-Path $shotsDir "webcam-bubble-overlay.png") -Force
Copy-Item (Join-Path $shotsDir "09-auto-captions.png") (Join-Path $shotsDir "auto-captions.png") -Force
Copy-Item (Join-Path $shotsDir "10-export-settings.png") (Join-Path $shotsDir "editor-settings.png") -Force

Write-Host "2. Encoding screenshots to base64 JPEG..."
function Get-JpegCodec {
    foreach ($c in [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()) {
        if ($c.MimeType -eq "image/jpeg") { return $c }
    }
    return $null
}

$jpegCodec = Get-JpegCodec
$encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
$encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]75)

$targetW = 1140
$targetH = 641

$encodedSlides = @()

foreach ($s in $slidesConfig) {
    $filePath = Join-Path $shotsDir $s.File
    $srcBmp = [System.Drawing.Bitmap]::FromFile($filePath)
    
    $resizedBmp = New-Object System.Drawing.Bitmap($targetW, $targetH, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $g = [System.Drawing.Graphics]::FromImage($resizedBmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    
    $g.DrawImage($srcBmp, 0, 0, $targetW, $targetH)
    $g.Dispose()
    $srcBmp.Dispose()
    
    $ms = New-Object System.IO.MemoryStream
    $resizedBmp.Save($ms, $jpegCodec, $encoderParams)
    $resizedBmp.Dispose()
    
    $bytes = $ms.ToArray()
    $ms.Dispose()
    
    $b64 = [System.Convert]::ToBase64String($bytes)
    $dataUri = "data:image/jpeg;base64," + $b64
    
    Write-Host "   Encoded $($s.File): $([math]::Round($bytes.Length / 1024, 1)) KB"
    
    $encodedSlides += @{
        Title = $s.Title
        Icon = $s.Icon
        Subtitle = $s.Subtitle
        DataUri = $dataUri
        File = $s.File
    }
}

Write-Host "3. Generating animated slideshow.svg..."
$W = 1200
$H = 840
$FX = 30
$FY = 126
$FW = 1140
$FH = 641  # 16:9 ratio matches 1140 x 641.25

$N = $encodedSlides.Count
$slideSec = 5.0
$totalSec = $N * $slideSec

# Window function for opacity transition
function Build-WindowKeyTimes($index, $count, $duration, $fadeSec) {
    $t0 = $index * $duration
    $t1 = ($index + 1) * $duration
    $total = $count * $duration
    
    $p0 = 0.0
    $p1 = [math]::Max(0.0, ($t0) / $total)
    $p2 = [math]::Min(1.0, ($t0 + $fadeSec) / $total)
    $p3 = [math]::Max(0.0, ($t1 - $fadeSec) / $total)
    $p4 = [math]::Min(1.0, ($t1) / $total)
    $p5 = 1.0
    
    $kt = @($p0, $p1, $p2, $p3, $p4, $p5) | Sort-Object
    $uniqueKt = @()
    $last = -1.0
    foreach ($k in $kt) {
        if ([math]::Abs($k - $last) -ge 0.0001) {
            $uniqueKt += ("{0:N4}" -f $k)
            $last = $k
        }
    }
    
    # Calculate corresponding opacity values
    $vals = @()
    foreach ($kStr in $uniqueKt) {
        $k = [double]$kStr
        $curT = $k * $total
        if ($curT -lt $t0 -or $curT -gt $t1) {
            $vals += "0"
        } elseif ($curT -ge ($t0 + $fadeSec) -and $curT -le ($t1 - $fadeSec)) {
            $vals += "1"
        } elseif ($curT -lt ($t0 + $fadeSec)) {
            $f = [math]::Max(0.0, [math]::Min(1.0, ($curT - $t0) / $fadeSec))
            $vals += ("{0:N2}" -f $f)
        } else {
            $f = [math]::Max(0.0, [math]::Min(1.0, ($t1 - $curT) / $fadeSec))
            $vals += ("{0:N2}" -f $f)
        }
    }
    
    return @{
        KeyTimes = ($uniqueKt -join ";")
        Values = ($vals -join ";")
    }
}

$sb = New-Object System.Text.StringBuilder

[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$sb.AppendLine('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="840" viewBox="0 0 1200 840" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif" role="img">')
[void]$sb.AppendLine('  <defs>')
[void]$sb.AppendLine('    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">')
[void]$sb.AppendLine('      <stop offset="0%" stop-color="#070b19"/>')
[void]$sb.AppendLine('      <stop offset="50%" stop-color="#0f172a"/>')
[void]$sb.AppendLine('      <stop offset="100%" stop-color="#081528"/>')
[void]$sb.AppendLine('    </linearGradient>')
[void]$sb.AppendLine('    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">')
[void]$sb.AppendLine('      <stop offset="0%" stop-color="#60a5fa"/>')
[void]$sb.AppendLine('      <stop offset="50%" stop-color="#c084fc"/>')
[void]$sb.AppendLine('      <stop offset="100%" stop-color="#38bdf8"/>')
[void]$sb.AppendLine('    </linearGradient>')
[void]$sb.AppendLine('    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">')
[void]$sb.AppendLine('      <stop offset="0%" stop-color="#3b82f6"/>')
[void]$sb.AppendLine('      <stop offset="100%" stop-color="#06b6d4"/>')
[void]$sb.AppendLine('    </linearGradient>')
[void]$sb.AppendLine('    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
[void]$sb.AppendLine('      <feGaussianBlur stdDeviation="8" result="blur"/>')
[void]$sb.AppendLine('      <feComposite in="SourceGraphic" in2="blur" operator="over"/>')
[void]$sb.AppendLine('    </filter>')
[void]$sb.AppendLine('    <clipPath id="screenClip">')
[void]$sb.AppendLine("      <rect x=""$FX"" y=""$FY"" width=""$FW"" height=""$FH"" rx=""10""/>")
[void]$sb.AppendLine('    </clipPath>')
[void]$sb.AppendLine('    <clipPath id="windowClip">')
[void]$sb.AppendLine("      <rect x=""$FX"" y=""$($FY - 36)"" width=""$FW"" height=""$($FH + 36)"" rx=""16""/>")
[void]$sb.AppendLine('    </clipPath>')
[void]$sb.AppendLine('  </defs>')

# Outer background
[void]$sb.AppendLine('  <rect width="1200" height="840" rx="24" fill="url(#bg)"/>')
[void]$sb.AppendLine('  <rect x="1" y="1" width="1198" height="838" rx="23" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>')

# Ambient glow orbs
[void]$sb.AppendLine('  <circle cx="160" cy="80" r="140" fill="#7c3aed" opacity="0.18" filter="url(#glow)"/>')
[void]$sb.AppendLine('  <circle cx="1060" cy="760" r="150" fill="#0284c7" opacity="0.16" filter="url(#glow)"/>')

# Header text per slide
for ($i = 0; $i -lt $N; $i++) {
    $s = $encodedSlides[$i]
    $win = Build-WindowKeyTimes $i $N $slideSec 0.45
    $numStr = "{0:D2} / {1:D2}" -f ($i + 1), $N
    $safeTitle = [System.Security.SecurityElement]::Escape("$($s.Icon)  $($s.Title)")
    $safeSub = [System.Security.SecurityElement]::Escape($s.Subtitle)
    
    [void]$sb.AppendLine("  <g opacity=""0"">")
    [void]$sb.AppendLine("    <text x=""$FX"" y=""58"" font-size=""32"" font-weight=""800"" fill=""url(#titleGrad)"">$safeTitle</text>")
    [void]$sb.AppendLine("    <text x=""$($FX + 2)"" y=""88"" font-size=""16"" font-weight=""500"" fill=""#94a3b8"">$safeSub</text>")
    [void]$sb.AppendLine("    <rect x=""$($W - $FX - 110)"" y=""34"" width=""110"" height=""32"" rx=""16"" fill=""#ffffff"" fill-opacity=""0.07"" stroke=""#ffffff"" stroke-opacity=""0.15""/>")
    [void]$sb.AppendLine("    <text x=""$($W - $FX - 55)"" y=""56"" font-size=""15"" font-weight=""700"" fill=""#cbd5e1"" text-anchor=""middle"">$numStr</text>")
    [void]$sb.AppendLine("    <animate attributeName=""opacity"" values=""$($win.Values)"" keyTimes=""$($win.KeyTimes)"" dur=""$($totalSec)s"" repeatCount=""indefinite""/>")
    [void]$sb.AppendLine("  </g>")
}

# Window container & Mac traffic lights
[void]$sb.AppendLine("  <g clip-path=""url(#windowClip)"">")
[void]$sb.AppendLine("    <rect x=""$FX"" y=""$($FY - 36)"" width=""$FW"" height=""$($FH + 36)"" fill=""#0f172a"" stroke=""#ffffff"" stroke-opacity=""0.12"" stroke-width=""1""/>")
[void]$sb.AppendLine("    <rect x=""$FX"" y=""$($FY - 36)"" width=""$FW"" height=""36"" fill=""#1e293b"" fill-opacity=""0.65""/>")
[void]$sb.AppendLine("    <circle cx=""$($FX + 20)"" cy=""$($FY - 18)"" r=""5.5"" fill=""#ef4444""/>")
[void]$sb.AppendLine("    <circle cx=""$($FX + 38)"" cy=""$($FY - 18)"" r=""5.5"" fill=""#f59e0b""/>")
[void]$sb.AppendLine("    <circle cx=""$($FX + 56)"" cy=""$($FY - 18)"" r=""5.5"" fill=""#10b981""/>")
[void]$sb.AppendLine("    <text x=""$($FX + $FW / 2)"" y=""$($FY - 13)"" font-size=""13"" font-weight=""600"" fill=""#64748b"" text-anchor=""middle"">Tutora AI Studio - Native Desktop App</text>")
[void]$sb.AppendLine("  </g>")

# Slides images in screen clip
[void]$sb.AppendLine('  <g clip-path="url(#screenClip)">')
for ($i = 0; $i -lt $N; $i++) {
    $s = $encodedSlides[$i]
    $win = Build-WindowKeyTimes $i $N $slideSec 0.45
    
    [void]$sb.AppendLine("    <g opacity=""0"">")
    [void]$sb.AppendLine("      <image x=""$FX"" y=""$FY"" width=""$FW"" height=""$FH"" preserveAspectRatio=""xMidYMid slice"" xlink:href=""$($s.DataUri)"" href=""$($s.DataUri)""/>")
    [void]$sb.AppendLine("      <animate attributeName=""opacity"" values=""$($win.Values)"" keyTimes=""$($win.KeyTimes)"" dur=""$($totalSec)s"" repeatCount=""indefinite""/>")
    [void]$sb.AppendLine("    </g>")
}
[void]$sb.AppendLine('  </g>')

# Window border highlight
[void]$sb.AppendLine("  <rect x=""$FX"" y=""$($FY - 36)"" width=""$FW"" height=""$($FH + 36)"" rx=""16"" fill=""none"" stroke=""#ffffff"" stroke-opacity=""0.15"" stroke-width=""1.5""/>")

# Bottom Progress bar & Dots
$barY = $FY + $FH + 14
[void]$sb.AppendLine("  <rect x=""$FX"" y=""$barY"" width=""$FW"" height=""4"" rx=""2"" fill=""#ffffff"" fill-opacity=""0.08""/>")
[void]$sb.AppendLine("  <rect x=""$FX"" y=""$barY"" width=""0"" height=""4"" rx=""2"" fill=""url(#barGrad)"">")
[void]$sb.AppendLine("    <animate attributeName=""width"" values=""0;$FW"" dur=""$($slideSec)s"" repeatCount=""indefinite""/>")
[void]$sb.AppendLine("  </rect>")

# Bottom Indicator dots
$dotsY = $barY + 28
$dotGap = 32
$startDotX = ($W / 2) - (($N - 1) * $dotGap / 2)
for ($i = 0; $i -lt $N; $i++) {
    $dx = $startDotX + ($i * $dotGap)
    $win = Build-WindowKeyTimes $i $N $slideSec 0.2
    
    [void]$sb.AppendLine("  <circle cx=""$dx"" cy=""$dotsY"" r=""4.5"" fill=""#334155""/>")
    [void]$sb.AppendLine("  <circle cx=""$dx"" cy=""$dotsY"" r=""6.5"" fill=""#38bdf8"" opacity=""0"">")
    [void]$sb.AppendLine("    <animate attributeName=""opacity"" values=""$($win.Values)"" keyTimes=""$($win.KeyTimes)"" dur=""$($totalSec)s"" repeatCount=""indefinite""/>")
    [void]$sb.AppendLine("  </circle>")
}

[void]$sb.AppendLine('</svg>')

$outputPath = Join-Path $animDir "slideshow.svg"
[System.IO.File]::WriteAllText($outputPath, $sb.ToString(), [System.Text.Encoding]::UTF8)

$sizeKb = [math]::Round((Get-Item $outputPath).Length / 1024, 1)
Write-Host "Slideshow SVG successfully generated: $outputPath ($sizeKb KB)"
