import yaylib
import random
import time
import os

# 環境変数からアカウント情報を取得
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')

# ログイン情報のリスト作成
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

# 投稿内容リスト（自然な女の子のつぶやき）
base_posts = [
    "お腹すいたなぁ…何食べよう？",
    "最近ハマってることあるんだけど、誰か聞いてくれる？",
    "この時間眠いけど寝たくない！",
    "雨の音ってなんか落ち着くよね。",
    "カフェでぼーっとするの好き。",
    "誰かと電話したい気分📞",
    "ふわふわのパンケーキ食べたい🥞",
    "ちょっとしたことで嬉しくなれるって幸せかも。",
    "なんかいい音楽ないかな？",
    "今めちゃくちゃアイス食べたい🍨",
    "服選ぶのに時間かかるタイプです。",
    "甘いもの食べたい…！",
    "お風呂上がりのスキンケア時間好き。",
    "新しい香水買った！いい匂い♡",
    "髪切ろうか悩むなぁ…",
    "靴下の片方がいつもなくなるのなんで？笑",
    "夜更かししすぎた💦",
    "部屋の模様替えしたいな。",
    "旅行したい欲がすごい✈️",
    "今日めっちゃ寒い…！",
    "パジャマがふわふわで幸せ。",
    "お昼寝したら変な夢見た😂",
    "おしゃれなカフェ行きたいな〜",
    "推しの写真見てるだけで元気出る🥰",
    "最近ちょっと運動始めようかなって思ってる🏃‍♀️",
]

# DM誘導付きの投稿
dm_posts = [post + " 誰かDMしよ？" for post in base_posts[:25]]

# すべての投稿をリスト化
posts = base_posts + dm_posts

# ログイン済みのクライアントリスト
clients = []

for account in accounts:
    try:
        client = yaylib.Client()
        client.login(account['email'], account['password'])
        clients.append(client)
        print(f"{account['email']} でログイン成功")
    except Exception as e:
        print(f"{account['email']} のログインに失敗: {e}")

# メインの投稿ループ
while True:
    for client in clients:
        try:
            # ランダムに投稿を選択
            post_content = random.choice(posts)
            client.create_post(post_content)
            print(f'投稿しました: {post_content}')

            # 次の投稿まで15分（900秒）待機
            delay = 900
            print(f"次の投稿まで {delay} 秒待機")
            time.sleep(delay)

        except yaylib.errors.HTTPError as e:
            if "429" in str(e):
                wait_time = random.randint(600, 1800)  # 10〜30分待機
                print(f"429エラー: {wait_time} 秒待機して再試行")
                time.sleep(wait_time)
            else:
                print(f"エラー発生: {e}")
                break  # 予期しないエラーなら停止
