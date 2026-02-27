$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $document = $word.Documents.Open('H:\IcloudDrive\iCloudDrive\Documents\Ola Lawal New Resume LA.docx')
    $document.SaveAs('H:\IcloudDrive\iCloudDrive\Documents\Ola_Lawal_Resume_Extracted.txt', 2)
    $document.Close()
} finally {
    $word.Quit()
}
Get-Content 'H:\IcloudDrive\iCloudDrive\Documents\Ola_Lawal_Resume_Extracted.txt'
