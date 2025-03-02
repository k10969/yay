import yaylib
import random
import time
import os
from datetime import datetime, timedelta
import pytz

# 日本時間（JST）のタイムゾーン
jst = pytz.timezone('Asia/Tokyo')

# 環境変数からアカウント情報を取得
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')

# ログイン情報リスト作成
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

# 投稿内容（時間ごと）
post_texts = {
    1: ["もう1時！？時間早すぎ…", "深夜のネットサーフィンが止まらない", "誰か電話しない？", "コンビニ行きたい",
        "夜中のラーメンは最強", "眠れない人いる〜？", "そろそろ寝ないと", "明日起きれるかな…", "つーわぼ #いいねでこちゃ"],
    # ...（省略）...
}

# DM誘導文
dm_text = " 、だれかDMしませんか。"

# 時間帯に応じた投稿を取得（ランダムでDM誘導を追加）
def get_time_based_post():
    now = datetime.now(jst).hour
    if now == 0:
        now = 24  # 0時を24時に変換

    post = random.choice(post_texts[now])

    # 4回に1回、DM誘導文を追加
    if random.randint(1, 4) == 1:
        post += dm_text

    return post

# ログイン処理
yay_clients = []

for account in accounts:
    try:
        client = yaylib.Client()
        client.login(account["email"], account["password"])
        yay_clients.append(client)
        print(f"{account['email']} でログイン成功")
    except Exception as e:
        print(f"{account['email']} のログインに失敗: {e}")

# 🚀 **ビルド完了後すぐに1投稿**
for client in yay_clients:
    try:
        first_post = get_time_based_post()
        client.create_post(first_post)
        print(f'✅ 初回投稿成功 ({client.email}): {first_post}')
    except Exception as e:
        print(f'❌ 初回投稿失敗 ({client.email}): {e}')

# ⏳ **最初の投稿後に次の投稿タイミングまで待機**
now = datetime.now(jst)
next_minute = (now.minute // 15 + 1) * 15
if next_minute == 60:
    next_minute = 0
    now += timedelta(hours=1)

next_time = now.replace(minute=next_minute, second=0, microsecond=0)
sleep_time = (next_time - datetime.now(jst)).total_seconds()
print(f"⏳ 最初の投稿後、次の投稿まで {int(sleep_time)} 秒待機")
time.sleep(sleep_time)

# 🎯 **メインの投稿ループ（15分ごと）**
while True:
    try:
        now = datetime.now(jst)

        for client in yay_clients:
            post_content = get_time_based_post()
            client.create_post(post_content)
            print(f'📢 投稿しました ({client.email}) [{now.strftime("%Y-%m-%d %H:%M:%S")}]: {post_content}')

        # 次の投稿時間を計算
        next_minute = (now.minute // 15 + 1) * 15
        if next_minute == 60:
            next_minute = 0
            now += timedelta(hours=1)

        next_time = now.replace(minute=next_minute, second=0, microsecond=0)
        sleep_time = (next_time - datetime.now(jst)).total_seconds()
        
        print(f"⏳ 次の投稿まで {int(sleep_time)} 秒待機")
        time.sleep(sleep_time)

    except yaylib.errors.HTTPError as e:
        if "429" in str(e):
            wait_time = random.randint(300, 900)  # 5〜15分待機
            print(f"🚧 429エラー: {wait_time} 秒待機して再試行")
            time.sleep(wait_time)
        else:
            print(f"⚠️ エラー発生: {e}")
            break  # 予期しないエラーなら停止
