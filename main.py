import random
import time
import os
from yaylib import Client  # 非公式APIが必要な場合

# 環境変数からアカウント情報を取得
accounts = [
    {'email': os.getenv('YAY_EMAIL_1'), 'password': os.getenv('YAY_PASSWORD_1')},
    {'email': os.getenv('YAY_EMAIL_2'), 'password': os.getenv('YAY_PASSWORD_2')}
]

# 投稿内容のリスト
posts = [
    "おはよう！",
    "最近ハマってることがあるの",
    "今日も頑張ろう！",
    "ねぇ、これ知ってる？",
    "やばい、ちょっと楽しいかも"
]

# クライアントのリスト
clients = []

# 各アカウントでログイン
for account in accounts:
    client = Client()
    client.login(account['email'], account['password'])
    clients.append(client)

# 30分ごとに自動投稿
while True:
    for client in clients:
        post_content = random.choice(posts)
        client.create_post(post_content)
        print(f'投稿しました: {post_content}')
    time.sleep(1800)  # 30分待機
