# Read-only local OCR of reproducible embedded JPEGs; no HTTP or product import.
param([string]$ImageDirectory, [string]$OutputPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStreamWithContentType, Windows.Storage.Streams, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.IsGenericMethod -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
} | Select-Object -First 1
function Wait-WinRt($Operation, [Type]$ResultType) {
    $task = $asTask.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    try { $task.Wait() } catch { throw $_.Exception.ToString() }
    return $task.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$rows = @()
foreach ($imageFile in (Get-ChildItem -LiteralPath $ImageDirectory -Filter '*.jpg' | Sort-Object Name)) {
    $file = Wait-WinRt ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imageFile.FullName)) ([Windows.Storage.StorageFile])
    $stream = Wait-WinRt ($file.OpenReadAsync()) ([Windows.Storage.Streams.IRandomAccessStreamWithContentType])
    try {
        $decoder = Wait-WinRt ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Wait-WinRt ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        try {
            $result = Wait-WinRt ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
            $lines = @($result.Lines | ForEach-Object {
                @{text=$_.Text; words=@($_.Words | ForEach-Object {
                    @{text=$_.Text; x=$_.BoundingRect.X; y=$_.BoundingRect.Y; width=$_.BoundingRect.Width; height=$_.BoundingRect.Height}
                })}
            })
            $rows += @{image=$imageFile.Name; width=$bitmap.PixelWidth; height=$bitmap.PixelHeight; text=$result.Text; lines=$lines}
        } finally { $bitmap.Dispose() }
    } finally { $stream.Dispose() }
}
$data = @{
    schema='c06-derived-ocr-1'; engine='Windows.Media.Ocr'; language=$engine.RecognizerLanguage.LanguageTag
    os_version=[Environment]::OSVersion.VersionString; observed_utc=[DateTime]::UtcNow.ToString('o')
    representation='Machine OCR of embedded PDF JPEGs. Derived navigation aid, not exact original text; en-US recognizer can misread Norwegian and numbers. Original images/PDF remain authoritative.'
    pages=$rows
}
[IO.File]::WriteAllText($OutputPath, ($data | ConvertTo-Json -Depth 12), (New-Object Text.UTF8Encoding($false)))
Write-Output ('OCR pages: ' + $rows.Count)
