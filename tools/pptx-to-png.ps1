param($src,$outdir)
$pp = New-Object -ComObject PowerPoint.Application
$p = $pp.Presentations.Open($src, $true, $false, $false)
$i=1
foreach($s in $p.Slides){ $s.Export((Join-Path $outdir ("s{0:D2}.png" -f $i)), "PNG", 960, 540); $i++ }
$p.Close(); $pp.Quit()
