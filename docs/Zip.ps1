Param(
    [string] [Parameter(Mandatory=$true)] $Source,
	[string] [Parameter(Mandatory=$true)] $Destination
)

if (Test-path $Destination) { Remove-item $Destination }
Add-Type -AssemblyName "System.IO.Compression.FileSystem"
[System.IO.Compression.ZipFile]::CreateFromDirectory($Source, $Destination)