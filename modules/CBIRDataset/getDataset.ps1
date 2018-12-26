function get-7z([String]$7zdes)
{
    $src = 'https://www.7-zip.org/a/7z1805'

    if ($( [Environment]::Is64BitOperatingSystem ))
    {
        #"64-bit"
        $src = $src + "-x64.exe"
    }
    else
    {
        #"32-bit"
        $src = $src + ".exe"
    }
    Write-Host $src


    Invoke-WebRequest -uri $src -OutFile $7zdes -UseBasicParsing -TimeoutSec 600
    Unblock-File $7zdes
    if ($( Test-Path $7zdes ))
    {
        Write-Host "Done"
    }
    else
    {
        Write-Host "7zip Dowmload Failed"
        Write-Host "Exiting"
        exit 0
    }
}

function Test-7z
{
    $7zdes = "$env:temp\7z.exe"
    Trap
    {
        Write-Host "No 7z.exe found"
        Write-Host "Try to download 7z"
        get-7z($7zdes)
        continue
    }
    $7zdes = $( Get-Command 7z.exe -ErrorAction Stop ).Source
    return $7zdes
}

workflow parallelDownload($datasets)
{
    foreach -parallel ($uri in $datasets)
    {
        $des = $PWD.Path + "\" + $uri.split("/")[-1]
        Invoke-WebRequest -Uri $uri -TimeoutSec 600 -UseBasicParsing -OutFile $des
    }
}


function main
{
    Write-Host "Looking for 7z.exe"  -ForegroundColor Red
    $7zdes = Test-7z
    Write-Host "7zip at:"$7zdes -ForegroundColor Yellow

    Write-Host "Starting downloading datasets" -ForegroundColor Red
    $datasets = "http://www-db.stanford.edu/~wangz/image.vary.jpg.tar",
    "http://wang.ist.psu.edu/~jwang/test1.tar"

    parallelDownload($datasets)
    Unblock-File ./*.tar

    Write-Host "Extracting" -ForegroundColor Red
    cmd /c $7zdes x ./*.tar

    Write-Host "Done" -ForegroundColor Red
}

main




