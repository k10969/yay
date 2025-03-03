import yaylib
import random
import time
import os
import threading
from datetime import datetime
import pytz

# --- 設定 ---
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
print(f"🌐 ログイン開始（{len(accounts)}アカウント）")
for account in accounts:
    try:
        client = yaylib.Client()
        client.login(account["email"], account["password"])
        yay_clients.append((client, account["email"]))  # client, email をペアで保存
        print(f"✅ {account['email']} でログイン成功")
    except Exception as e:
        print(f"❌ {account['email']} のログイン失敗: {e}")

if not yay_clients:
    print("🚨 ログインできたアカウントがありません。終了します。")
    exit(1)

# --- 自動いいね・フォロー機能 ---
def auto_like_and_follow(client, email):
    print(f"🔍 {email} - 自動いいね & フォロー開始")
    hashtags = ["#いいねでこちゃ", "#いいねでレター"]

    try:
        for tag in hashtags:
            print(f"🔎 {email} - ハッシュタグ検索: {tag}")
            posts = client.search_posts(tag)
            print(f"📌 {email} - {tag} の投稿数: {len(posts)}")

            for post in posts:
                post_id = post.get('id')
                if post_id:
                    client.like_post(post_id)
                    print(f"👍 {email} - いいね成功: {post_id}")

        print(f"🔎 {email} - '通話募集' の投稿を検索")
        posts = client.search_posts("通話募集")
        print(f"📌 {email} - '通話募集' の投稿数: {len(posts)}")

        for post in posts:
            user_id = post.get('user_id')
            if user_id:
                user = client.get_user(user_id)
                username = user.get('username', 'Unknown')
                gender = user.get('gender', 'Unknown')
                
                if gender == 'male':
                    client.like_post(post['id'])
                    client.follow_user(user_id)
                    print(f"✅ {email} - {username} ({user_id}) をフォロー＆いいね")
    except Exception as e:
        print(f"❌ {email} の auto_like_and_follow でエラー: {e}")

# --- 自動DM返信機能 ---
def auto_reply(client, email):
    print(f"📩 {email} - 自動DM返信開始")
    try:
        chats = client.get_chats()
        print(f"📬 {email} - 取得した未返信チャット数: {len(chats)}")

        for chat in chats:
            sender_id = chat.get('sender_id')
            is_replied = chat.get('is_replied', False)

            if sender_id and not is_replied:
                reply_text = "はじめまして！インスタではなそ、@1316_21 これです！"
                client.send_message(sender_id, reply_text)
                print(f"📩 {email} - {sender_id} へメッセージ送信成功: {reply_text}")
    except Exception as e:
        print(f"❌ {email} の auto_reply でエラー: {e}")

# --- 自動投稿処理 ---
def time_based_posting_loop():
    while True:
        for client, email in yay_clients:
            try:
                post_text = "つーわぼ #いいねでこちゃ"
                client.create_post(post_text)
                print(f"📢 {email} - 投稿完了: {post_text}")
            except Exception as e:
                print(f"❌ {email} の投稿エラー: {e}")
        time.sleep(3600)

# --- 自動いいね・フォロー・DM返信ループ ---
def auto_action_loop():
    while True:
        for client, email in yay_clients:
            auto_like_and_follow(client, email)
            auto_reply(client, email)
        time.sleep(600)

# --- スレッド開始 ---
threading.Thread(target=time_based_posting_loop, daemon=True).start()
threading.Thread(target=auto_action_loop, daemon=True).start()

# メインスレッドを維持
while True:
    time.sleep(1)
