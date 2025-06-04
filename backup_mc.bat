@echo off
setlocal

:: バックアップ元（Minecraftワールドのフォルダ）
set WORLD_DIR=C:\Your\MinecraftServer\world

:: バックアップ保存先
set BACKUP_DIR=backups

:: 日付入りファイル名
set TIMESTAMP=%DATE:~0,4%-%DATE:~5,2%-%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set FILENAME=backup_%TIMESTAMP%.zip

:: フォルダがなければ作る
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

:: バックアップを作成
powershell Compress-Archive -Path "%WORLD_DIR%\*" -DestinationPath "%BACKUP_DIR%\%FILENAME%"

:: 通知を送る
python notify_discord.py "%FILENAME%"
