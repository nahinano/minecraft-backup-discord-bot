<<<<<<< HEAD
JP

# 🧱 Minecraft Backup Discord Bot

このBotは、**Discord上のスラッシュコマンドからMinecraftサーバーのバックアップ**を管理できる便利なツールです。  
ZIP形式でバックアップを自動生成し、必要に応じてDiscordに添付＆通知してくれます。

---

## ✨ 主な機能 / Features

- `/backup`：現在のサーバーワールドをZIP形式でバックアップ
- `/listbackups`：バックアップファイル一覧を表示（最新10件）
- `/deletebackup <filename>`：指定ファイルを削除
- `/backupstatus`：保存件数と合計容量を確認
- `.env`で**Discord添付・対象ロール・バックアップ除外項目などの設定**が可能
- `.env`で特定フォルダ（例：`logs/`）を**バックアップ除外**できる

---

## 🛠 セットアップ手順 / Setup

### 1. BotをDiscordに登録

1. [Discord開発者ポータル](https://discord.com/developers/applications)にアクセス
2. 新しいアプリケーションを作成し、Botを有効化
3. 左メニューの「OAuth2 > URL Generator」で以下を選択：
    - ✅ `bot`
    - ✅ `applications.commands`
    - ✅ Botの権限（例：`Send Messages`, `Attach Files`。迷う場合は「すべて」でもOK）
4. 生成されたURLからBotを**Discordサーバーに招待**
5. 左メニュー「Bot」→ `Reset Token` を押してトークンをコピー

### 2. Webhookの作成

1. Discordの対象サーバー設定 > 「連携サービス」 > 「ウェブフック」
2. 「新しいウェブフック」を作成、名前をつける（例：`Captain Hook`）
3. ウェブフックURLをコピー

---

### 3. `.env` を編集して必要な設定を追加

プロジェクトに `.env` ファイルがある場合、その中に以下の設定がなければ追記、  
すでにある場合は編集してください：

```env
# Botトークン（Discord開発者ポータルから取得）
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxx

# DiscordのWebhook URL（通知先）
WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyyyyyyy

# Minecraftワールドフォルダのパス
WORLD_PATH=X:yyyyyyyy/zzzzzzzz

# バックアップ保存先フォルダ（事前に作成しておく）
BACKUP_DIR=A:bbbbbbbbb/ccccccccc

# コマンドを使えるロールID（複数可・カンマ区切り）
ALLOWED_ROLE_IDS=314159265358979323,846264338327950288

# DiscordにZIPを添付するか（true/false）
UPLOAD_TO_DISCORD=true

# 以下はバックアップから除外したい項目（false指定で除外されます）
INCLUDE_world__playerdata=true
INCLUDE_world__advancements=true
INCLUDE_world__region=true
INCLUDE_world__datapacks=true
INCLUDE_world__dimensions=true
INCLUDE_world__poi=true
INCLUDE_world__stats=true
INCLUDE_world__level_dat=true
INCLUDE_world__session_lock=true
INCLUDE_world__forcedchunks=true
INCLUDE_world__mca=true
INCLUDE_world__logs=false
INCLUDE_world__plugins=true
INCLUDE_world__eula_txt=false
INCLUDE_world__server_properties=true

.env ファイルの中身を保存し更新したら、Bot を起動してください。
# botの起動方法
🇯🇵 日本語
Python 3.10以上をインストール
必要なライブラリをインストールする
Microsoft PoworPhellなどで"pip install -r requirements.txt"と入力
cd "C:\Users\xxxxx\yyyyyy\zzzzzzzzz"と入力(このパスはbot.pyが入っているファイルのパス)
python bot.py　と入力　そうすると起動ができる

discordで/コマンドをしてあげるとバックアップが取れたりとかできる

## 📄 利用規約 / Terms of Use

このツールは非商用目的であれば自由に改変・再配布・公開できます。  
詳細は `TERMS_OF_USE.txt` をご確認ください。

© 2025 Nahinano. All rights reserved.
---

EN

🧱 Minecraft Backup Discord Bot
This Bot is a convenient tool that allows you to manage Minecraft server backups via Discord slash commands.
It automatically creates backups in ZIP format and attaches and notifies them on Discord as needed.

✨ Features
/backup: Create a ZIP backup of the current server world

/listbackups: Display a list of backup files (up to the latest 10)

/deletebackup <filename>: Delete a specified backup file

/backupstatus: Check the number of backups and total size

Configure Discord attachment, allowed roles, and backup exclusion items via .env

Exclude specific folders (e.g., logs/) from backup via .env

🛠 Setup
1. Register your Bot on Discord
Go to the Discord Developer Portal

Create a new application and enable the Bot

In the left menu, go to "OAuth2 > URL Generator" and select:

✅ bot

✅ applications.commands

✅ Bot permissions (e.g., Send Messages, Attach Files. You can select all permissions if unsure)

Use the generated URL to invite the Bot to your Discord server

In the left menu under "Bot", click Reset Token and copy the token

2. Create a Webhook
In your Discord server settings > "Integrations" > "Webhooks"

Create a new webhook and name it (e.g., Captain Hook)

Copy the webhook URL

3. Edit .env and add the necessary settings
If you have a .env file in your project, add or edit the following settings:

env
# Bot token (from Discord Developer Portal)
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxx

# Discord webhook URL (for notifications)
WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyyyyyyy

# Minecraft world folder path
WORLD_PATH=X:yyyyyyyy/zzzzzzzz

# Backup destination folder (create this beforehand)
BACKUP_DIR=A:bbbbbbbbb/ccccccccc

# Role IDs allowed to use commands (multiple IDs comma separated)
ALLOWED_ROLE_IDS=314159265358979323,846264338327950288

# Whether to attach ZIP backups to Discord (true/false)
UPLOAD_TO_DISCORD=true

# Items to exclude from backup (set false to exclude)
INCLUDE_world__playerdata=true
INCLUDE_world__advancements=true
INCLUDE_world__region=true
INCLUDE_world__datapacks=true
INCLUDE_world__dimensions=true
INCLUDE_world__poi=true
INCLUDE_world__stats=true
INCLUDE_world__level_dat=true
INCLUDE_world__session_lock=true
INCLUDE_world__forcedchunks=true
INCLUDE_world__mca=true
INCLUDE_world__logs=false
INCLUDE_world__plugins=true
INCLUDE_world__eula_txt=false
INCLUDE_world__server_properties=true
Save and update the .env file, then start the Bot.

🚀 How to Run
Install Python 3.10 or later

Install required libraries:
Open a terminal (PowerShell, CMD, etc.) and run:

bash
pip install -r requirements.txt
Navigate to the folder containing bot.py:

bash
cd "C:\Users\xxxxx\yyyyyy\zzzzzzzzz"
Start the bot:

bash
python bot.py
After starting, use slash commands on Discord to trigger backups or manage them.

📄 Terms of Use
This tool can be freely modified, redistributed, and published for non-commercial purposes only.
Please see TERMS_OF_USE.txt for detailed conditions.

© 2025 Nahinano. All rights reserved.

=======
# minecraft-backup-discord-bot
minecraftのサーバーをdiscordのbotのコマンド通じてバックアップができるdiscord bot
>>>>>>> 5fe8cdcc119b069929d45a7050ea4b470b2bff6b
