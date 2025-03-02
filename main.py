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
    13: ["午後の仕事or授業スタート！", "ランチ後って眠くなるよね"],
    14: ["まだお昼の眠気が抜けない", "そろそろおやつの時間"],
    15: ["おやつタイム〜", "あと少しで終業時間…"],
    16: ["あと少しで仕事終わる！！さいこーー", "夕方の空って綺麗だよね"],
    17: ["みんなおつかれさま！", "夕方のこの時間、好きかも"],
    18: ["夜ご飯の時間だ〜！", "今日の夕飯は何だと思う？"],
    19: ["夜ご飯食べ終わった？", "この時間はYouTubeかネトフリ見たくなる"],
    20: ["夜のリラックスタイム", "そろそろお風呂入ろうかな"],
    21: ["そろそろ寝る準備してる？", "今日の振り返り中"],
    22: ["寝る前のリラックスタイム", "夜更かしする人〜？"],
    23: ["そろそろ寝ようかな", "夜って色々考えちゃうよね"],
    24: ["こんな時間まで起きてる人いる？", "そろそろ寝る準備しよ〜"]
}

# DM誘導文
dm_text = " 、だれかDMしませんか。"

# 時間帯に応じた投稿を取得（ランダムでDM誘導を追加）
def get_time_based_post():
    now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst).hour
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

# 🎯 **メインの投稿ループ（15分ごと）**
while True:
    try:
        now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst)
        current_minute = now.minute

        # 次の投稿タイミング（0分, 15分, 30分, 45分）を計算
        next_post_minute = (current_minute // 15 + 1) * 15
        if next_post_minute == 60:
            next_post_minute = 0  # 次の時間に繰り越し
        
        for client in yay_clients:
            post_content = get_time_based_post()
            client.create_post(post_content)
            print(f'📢 投稿しました ({client.email}) [{now.strftime("%Y-%m-%d %H:%M:%S")}]: {post_content}')

        # 次の投稿時間まで待機
        next_time = now.replace(minute=next_post_minute, second=0, microsecond=0)
        if next_post_minute == 0:
            next_time += timedelta(hours=1)  # 0分なら次の時間に変更
        
        sleep_time = (next_time - datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst)).total_seconds()
        
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
