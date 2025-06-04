
import os
import zipfile
import datetime
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import humanize

# 📋 ログ設定 / Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 🌱 環境変数の読み込み / Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WORLD_PATH = os.getenv("WORLD_PATH")
BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")
UPLOAD_TO_DISCORD = os.getenv("UPLOAD_TO_DISCORD", "true").lower() == "true"
ALLOWED_ROLE_IDS = [int(x) for x in os.getenv("ALLOWED_ROLE_IDS", "").split(",") if x.strip().isdigit()]
MAX_SIZE_MB = int(os.getenv("DISCORD_FILE_LIMIT_MB", "8"))
BACKUP_LIMIT = int(os.getenv("BACKUP_RETENTION_LIMIT", "30"))

# 🔍 バックアップ対象ルールの取得 / Load INCLUDE_ rules
INCLUDE_RULES = {}
EXCLUDED_KEYS = []
for key, value in os.environ.items():
    if key.startswith("INCLUDE_"):
        rule_key = key[8:].lower().replace("__", "/")
        is_included = value.strip().lower() == "true"
        INCLUDE_RULES[rule_key] = is_included
        if not is_included:
            EXCLUDED_KEYS.append(rule_key)

# ✅ コマンド実行許可ロール確認 / Role checking decorator
def is_allowed_user():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not ALLOWED_ROLE_IDS:
            return True
        if not interaction.guild or not hasattr(interaction.user, "roles"):
            return False
        user_roles = [role.id for role in interaction.user.roles]
        return any(role_id in user_roles for role_id in ALLOWED_ROLE_IDS)
    return app_commands.check(predicate)

# 🤖 Botの初期化 / Initialize the bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    logging.info(f"Bot is ready. Logged in as {bot.user}")

# ✅ /backup コマンド
@bot.tree.command(name="backup", description="Minecraftワールドをバックアップします / Backup Minecraft world")
@is_allowed_user()
@app_commands.checks.cooldown(1, 600, key=lambda i: i.guild_id)
async def backup(interaction: discord.Interaction):
    await interaction.response.send_message("🕒 バックアップを作成中...", ephemeral=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"world_backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, filename)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(WORLD_PATH):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, WORLD_PATH).replace("\\", "/")
                    matched = False
                    for rule, allowed in INCLUDE_RULES.items():
                        if rel_path.startswith(rule):
                            matched = True
                            if not allowed:
                                break
                    if matched and not INCLUDE_RULES.get(rule, True):
                        continue
                    zipf.write(abs_path, arcname=rel_path)
        logging.info(f"✅ バックアップ作成: {backup_path}")
    except Exception as e:
        logging.error(f"❌ バックアップ失敗: {e}")
        await interaction.followup.send(f"❌ バックアップ失敗: {e}", ephemeral=True)
        return

    # 通知と添付
    try:
        size = os.path.getsize(backup_path)
        size_mb = round(size / (1024 * 1024), 2)
        exclude_msg = "\n❗ 除外対象: " + ", ".join(EXCLUDED_KEYS) if EXCLUDED_KEYS else ""

        if size <= MAX_SIZE_MB * 1024 * 1024 and UPLOAD_TO_DISCORD:
            with open(backup_path, 'rb') as f:
                files = {"file": (filename, f)}
                data = {"content": f"📦 バックアップ完了！ `{filename}`（{size_mb}MB）{exclude_msg}"}
                requests.post(WEBHOOK_URL, data=data, files=files)
        else:
            msg = f"📦 バックアップ完了: `{filename}`（{size_mb}MB）"
            if not UPLOAD_TO_DISCORD:
                msg += "\n🔕 添付は無効化されています"
            elif size > MAX_SIZE_MB * 1024 * 1024:
                msg += f"\n⚠️ 添付上限（{MAX_SIZE_MB}MB）を超えました"
            msg += exclude_msg
            requests.post(WEBHOOK_URL, json={"content": msg})
        await interaction.followup.send("✅ バックアップ完了！", ephemeral=True)
    except Exception as e:
        logging.error(f"⚠️ 通知失敗: {e}")
        await interaction.followup.send(f"⚠️ 通知失敗: {e}", ephemeral=True)

    # 古いバックアップの削除
    try:
        files = sorted(
            [f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")],
            key=lambda x: os.path.getmtime(os.path.join(BACKUP_DIR, x))
        )
        if len(files) > BACKUP_LIMIT:
            for f in files[:-BACKUP_LIMIT]:
                os.remove(os.path.join(BACKUP_DIR, f))
                logging.info(f"🗑 古いバックアップ削除: {f}")
    except Exception as e:
        logging.error(f"❌ 古いファイル削除失敗: {e}")

# ✅ /listbackups バックアップ一覧表示
@bot.tree.command(name="listbackups", description="保存されたバックアップ一覧を表示します / List all saved backups")
@is_allowed_user()
async def list_backups(interaction: discord.Interaction):
    try:
        files = sorted(
            [f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")],
            key=lambda x: os.path.getmtime(os.path.join(BACKUP_DIR, x)),
            reverse=True
        )
        if not files:
            await interaction.response.send_message("⚠️ バックアップは存在しません。", ephemeral=True)
            return
        msg = "\n".join(f"`{f}`" for f in files)
        await interaction.response.send_message(f"🗂 バックアップ一覧:\n{msg}", ephemeral=True)
    except Exception as e:
        logging.error(f"❌ バックアップ一覧取得失敗: {e}")
        await interaction.response.send_message(f"❌ 取得エラー: {e}", ephemeral=True)

# ✅ /deletebackup 指定したバックアップを削除
@bot.tree.command(name="deletebackup", description="指定したバックアップファイルを削除します / Delete a backup file by name")
@is_allowed_user()
@app_commands.describe(filename="削除するZIPファイル名 / ZIP file name to delete")
async def delete_backup(interaction: discord.Interaction, filename: str):
    path = os.path.join(BACKUP_DIR, filename)
    if not os.path.isfile(path):
        await interaction.response.send_message(f"❌ ファイルが見つかりません: `{filename}`", ephemeral=True)
        return
    try:
        os.remove(path)
        logging.info(f"🗑 バックアップ削除: {filename}")
        await interaction.response.send_message(f"🗑 削除完了: `{filename}`", ephemeral=True)
    except Exception as e:
        logging.error(f"❌ 削除失敗: {e}")
        await interaction.response.send_message(f"❌ 削除失敗: {e}", ephemeral=True)

# ✅ /backupstatus バックアップ状況を確認
@bot.tree.command(name="backupstatus", description="バックアップの件数と合計サイズを表示 / Show number and size of backups")
@is_allowed_user()
async def backup_status(interaction: discord.Interaction):
    try:
        files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")]
        total_size = sum(os.path.getsize(os.path.join(BACKUP_DIR, f)) for f in files)
        size_mb = round(total_size / (1024 * 1024), 2)
        await interaction.response.send_message(f"🧾 バックアップ数: {len(files)} 件\n📦 合計サイズ: {size_mb} MB", ephemeral=True)
    except Exception as e:
        logging.error(f"❌ ステータス取得失敗: {e}")
        await interaction.response.send_message(f"❌ ステータス取得失敗: {e}", ephemeral=True)

# 🚀 Bot起動処理
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ コマンド同期完了: {len(synced)} 個のコマンド")
        print(f"Bot is ready. {bot.user}")
    except Exception as e:
        logging.error(f"❌ コマンド同期失敗: {e}")

# 🔑 Bot実行
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        logging.critical(f"❌ BOT起動失敗: {e}")
