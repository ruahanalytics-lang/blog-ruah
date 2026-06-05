# Registra a tarefa no Windows Task Scheduler para rodar todo dia às 08:00
$python = (Get-Command python).Source
$script = "C:\Users\Administrador\Documents\blog-ruah\pipeline.py"
$workdir = "C:\Users\Administrador\Documents\blog-ruah"

$action  = New-ScheduledTaskAction -Execute $python -Argument $script -WorkingDirectory $workdir
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -StartWhenAvailable

Register-ScheduledTask -TaskName "BlogRuah-Pipeline" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Tarefa agendada com sucesso! Roda todo dia às 08:00."
