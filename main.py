import yaylib
import random
import time
import os
from datetime import datetime

# 環境変数からアカウント情報を取得
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')

# ログイン情報のリスト作成
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

# 各時間帯の投稿リスト（1時間ごとに8個）
hourly_posts = {
    0: ["こんな時間まで起きてる人いる？", "そろそろ寝る準備しよ〜", "夜更かし最高✨", "深夜テンションやばい😂",
        "寝たいけど眠れない…", "誰か話そ💬", "YouTube見すぎた📱", "ベッドが最高すぎる"],
    1: ["もう1時！？時間早すぎ…", "深夜のネットサーフィンが止まらない", "誰か電話しない？📞", "コンビニ行きたい🍫",
        "夜中のラーメンは最強🍜", "眠れない人いる〜？", "そろそろ寝ないと💦", "明日起きれるかな…"],
    2: ["深夜組集合〜！", "もうそろそろ寝ないと😪", "YouTube見てたらこんな時間😱", "小腹すいたなぁ…",
        "夜中に食べるお菓子は罪だけど美味い", "朝が来る前に寝るぞ！", "寝る前にストレッチしよ🧘‍♀️", "ラジオ聴いてる📻"],
    3: ["この時間起きてるのは少数派…？", "完全に夜更かししすぎた😂", "3時って一番眠くなる時間…", "もう寝なきゃ…",
        "夜の静けさって落ち着く🌙", "SNS見てたら時間溶けた😵", "そろそろ寝落ちしそう😴", "夜中に考え事しちゃう…"],
    4: ["おはようって言っていいのか微妙な時間", "早起き？それとも夜更かし？", "空が少し明るくなってきた🌅",
        "そろそろ朝の準備するか…", "こんな時間に起きてるの自分だけ？", "朝ごはん食べる人いる？", "眠すぎる…", "今日の予定考え中🤔"],
    5: ["朝が来た〜🌞", "完全に寝不足😂", "眠いけど頑張る💪", "そろそろ朝ごはん食べようかな？", 
        "早起きさんいる？", "今日も一日頑張ろう✨", "なんだかんだ夜更かししちゃった💦", "おはよう世界🌎"],
    6: ["おはよー！今日も元気に！", "朝ごはん何食べた？🍞", "今日も一日ファイト💪", "まだ眠いよ〜😴",
        "布団から出たくない🥶", "学校（or 仕事）行きたくない…", "朝活してる人いる？", "今日もいい天気☀️"],
    # 7〜22時も同じように作成する（省略）
    23: ["そろそろ寝る時間かな？", "今日も1日お疲れ様✨", "夜ってなんか落ち着く…", "寝る前に少しおしゃべりしよ💬",
        "お風呂入ってスッキリ！", "ベッドに入ったけど眠れない😅", "明日の予定確認しなきゃ", "おやすみなさい💤"]
}

# 4回に1回、投稿の最後に付ける文章
dm_message = " だれかDMしませんか、フォローもお願いします！"

# 指定された時間帯の投稿リストからランダムに4つ選ぶ
def get_time_based_posts():
    now = datetime.now().hour
    posts = hourly_posts.get(now, ["なにしてるの〜？💬", "ちょっとおしゃべりしたい💖"])

    # リストが空でないことを確認してランダムに4つ選ぶ
    if len(posts) >= 4:
        selected_posts = random.sample(posts, 4)
    else:
        selected_posts = posts  # 投稿が4つ未満の場合、そのまま使用

    # 4回に1回の確率でDM誘導を追加
    for i in range(len(selected_posts)):
        if random.randint(1, 4) == 1:
            selected_posts[i] += dm_message

    return selected_posts

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

# メインの投稿ループ
while True:
    try:
        client = random.choice(yay_clients)
        posts = get_time_based_posts()

        for post_content in posts:
            client.create_post(post_content)
            print(f'投稿しました: {post_content}')
            time.sleep(900)

    except yaylib.errors.HTTPError as e:
        if "429" in str(e):
            wait_time = random.randint(600, 1800)
            print(f"429エラー: {wait_time} 秒待機して再試行")
            time.sleep(wait_time)
        else:
            print(f"エラー発生: {e}")
            break
