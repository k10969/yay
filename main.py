import yaylib
import random
import time
import os
import threading
from datetime import datetime
import pytz

# --- 共通設定 ---
jst = pytz.timezone('Asia/Tokyo')

# 環境変数からアカウント情報を取得
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

# ログイン処理
yay_clients = []
print(f"🌐 ログイン処理開始（{len(accounts)}アカウント）")
for account in accounts:
    try:
        client = yaylib.Client()
        client.login(account["email"], account["password"])
        yay_clients.append((client, account["email"]))  # client, email をペアで保存
        print(f"✅ {account['email']} でログイン成功")
    except Exception as e:
        print(f"❌ {account['email']} のログインに失敗: {e}")

if not yay_clients:
    print("🚨 ログインできたアカウントがありません。終了します。")
    exit(1)

# --- 投稿テキストの設定 ---
post_texts = {
    1: ["もう1時！？時間早すぎ…", "深夜のネットサーフィンが止まらない"],
    2: ["深夜組集合〜！", "もうそろそろ寝ないと"],
    3: ["この時間起きてるのは少数派…？", "完全に夜更かししすぎた"],
    4: ["おはようって言っていいのか微妙な時間", "早起き？それとも夜更かし？"],
    5: ["朝が来た〜", "完全に寝不足"],
    6: ["おはよ〜！今日も頑張ろっ", "ねむい…あと5分寝たい"],
    7: ["まだちょっと眠い…", "朝ごはん食べた？"],
    8: ["眠すぎ", "電車混んでる…"],
    9: ["そろそろお腹すいてきたかも", "仕事中だ〜"],
    10: ["ちょっと一息つこ", "みんななにしてるの〜？？"],
    11: ["お昼ごはんどうしよ〜", "ランチ何にしようか迷う"],
    12: ["ランチなう", "お昼ごはん美味しすぎ"],
    13: ["午後の仕事スタート！みんながんばろうね", "ランチ後って眠くなるよね"],
    14: ["まだお昼の眠気が抜けない", "そろそろおやつの時間"],
    15: ["おやつタイム〜", "あと少しで終業時間…"],
    16: ["あと少しで仕事終わる！！", "夕方の空って綺麗だよね"],
    17: ["みんなおつかれさま！", "夕方のこの時間、好きかも"],
    18: ["夜ご飯の時間だ〜！", "今日の夕飯は何だと思う？"],
    19: ["夜ご飯食べ終わった？", "この時間はYouTubeかネトフリ見たくなる"],
    20: ["夜のリラックスタイム", "そろそろお風呂入ろうかな"],
    21: ["そろそろ寝る準備してる？", "今日の振り返り中"],
    22: ["寝る前のリラックスタイム", "夜更かしする人〜？"],
    23: ["そろそろ寝ようかな", "夜って色々考えちゃうよね"],
    24: ["こんな時間まで起きてる人いる？", "そろそろ寝る準備しよ〜"]
}

dm_text = " 、だれかDMきてください。"

# 時間帯に応じた投稿を取得
def get_time_based_post():
    now = datetime.now(jst).hour
    if now == 0:
        now = 24  # 0時を24時として扱う
    post = random.choice(post_texts.get(now, ["つーわぼ #いいねでこちゃ"]))
    if random.randint(1, 4) == 1:
        post += dm_text
    return post

# 時間指定投稿のループ
def time_based_posting_loop():
    while True:
        print("\n🌟 新しい投稿サイクル開始")
        for client, email in yay_clients:
            try:
                post = get_time_based_post()
                client.create_post(post)
                print(f"✅ 投稿成功: {email} -> {post}")
            except Exception as e:
                print(f"❌ 投稿エラー ({email}): {e}")

        print("⏳ 次の投稿まで15分待機...")
        time.sleep(900)  # 15分ごとに投稿

# スレッドを開始
threading.Thread(target=time_based_posting_loop, daemon=True).start()

# メインスレッドを維持
while True:
    time.sleep(1)
