import yaylib
import random
import time
import os

# アカウント情報（環境変数から取得）
EMAIL = os.getenv('YAY_EMAIL')
PASSWORD = os.getenv('YAY_PASSWORD')

# 投稿内容リスト（ランダムに選択）
posts = [
    "今日は何しようかな",
    "最近楽しいことが増えた",
    "暇だな～誰か話そ？",
    "何か面白いことないかな",
    "ちょっとドキドキしてる…"
]

# クライアントログイン
client = yaylib.Client()
client.login(EMAIL, PASSWORD)

while True:
    try:
        # ランダムに投稿を選択
        post_content = random.choice(posts)
        client.create_post(post_content)
        print(f'投稿しました: {post_content}')
        
        # 次の投稿までランダムな待機時間（30～60分）
        delay = random.randint(1800, 3600)
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
