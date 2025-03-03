import yaylib
import random
import time
import os
import threading
from datetime import datetime, timedelta
import pytz

# --- 共通設定 ---
# 日本時間（JST）のタイムゾーン
jst = pytz.timezone('Asia/Tokyo')

# 環境変数からアカウント情報を取得（"email:password,email:password,..."）
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

# ログイン処理（各アカウントで一度だけログイン）
yay_clients = []
print(f"🌐 ログイン処理開始（{len(accounts)}アカウント）")
for account in accounts:
    try:
        client = yaylib.Client()
        client.login(account["email"], account["password"])
        yay_clients.append(client)
        print(f"✅ {account['email']} でログイン成功")
    except Exception as e:
        print(f"❌ {account['email']} のログインに失敗: {e}")

print(f"✅ ログイン成功アカウント数: {len(yay_clients)}")
if not yay_clients:
    print("🚨 ログインできたアカウントがありません。終了します。")
    exit(1)

# --- 時間指定投稿機能 ---
# 各時間帯の投稿内容（各時間帯につき候補は8個以上推奨）
post_texts = {
    1: ["もう1時！？時間早すぎ…", "深夜のネットサーフィンが止まらない", "誰か電話しない？", "コンビニ行きたい",
        "夜中のラーメンは最強", "眠れない人いる〜？", "そろそろ寝ないと", "明日起きれるかな…", "つーわぼ #いいねでこちゃ"],
    2: ["深夜組集合〜！", "もうそろそろ寝ないと", "YouTube見てたらこんな時間", "小腹すいたなぁ…",
        "夜中に食べるお菓子は罪だけど美味い", "朝が来る前に寝るぞ！", "寝る前にストレッチしよ", "ラジオ聴いてる", "つーわぼ #いいねでこちゃ"],
    3: ["この時間起きてるのは少数派…？", "完全に夜更かししすぎた", "3時って一番眠くなる時間…", "もう寝なきゃ…",
        "夜の静けさって落ち着く", "SNS見てたら時間溶けた", "そろそろ寝落ちしそう", "夜中に考え事しちゃう…", "つーわぼ #いいねでこちゃ"],
    4: ["おはようって言っていいのか微妙な時間", "早起き？それとも夜更かし？", "空が少しずつ明るくなってきた", "この時間の空気好き",
        "もう朝かぁ…", "ちょっとだけ二度寝したい", "朝日が綺麗", "早起きは三文の徳ってほんと？", "つーわぼ #いいねでこちゃ"],
    5: ["朝が来た〜", "完全に寝不足", "もう朝！？", "目が開かない…", "コーヒー飲まなきゃ", "今日は何しよう？", "起きたけど布団から出れない",
        "寝坊したかも…", "つーわぼ #いいねでこちゃ"],
    6: ["おはよ〜！今日も頑張ろっ", "ねむい…あと5分寝たい", "朝ごはん食べた？", "今日の予定チェックしなきゃ", 
        "エナジードリンク飲もうかな", "朝から元気な人すごい", "すでに眠い", "とりあえず顔洗お", "つーわぼ #いいねでこちゃ"],
    7: ["まだちょっと眠い…", "朝ごはん食べた？", "支度しなきゃ", "今日の服どうしよう", "外寒いかな？", "電車混んでそう…", 
        "もうちょっと布団にいたい", "学校or仕事行きたくない", "つーわぼ #いいねでこちゃ"],
    8: ["眠すぎ", "電車混んでる…", "会社or学校ついた？", "朝の空気気持ちいい", "遅刻しそう", "通勤・通学中",
        "今日も頑張るぞ！", "あと何時間後に帰れるんだろ", "つーわぼ #いいねでこちゃ"],
    9: ["そろそろお腹すいてきたかも", "仕事中だ〜", "午前中が長い…", "集中力がもたない", "朝ごはん足りなかった",
        "早く休憩したい", "あと少しでお昼ごはん！", "誰かランチ行こ〜", "つーわぼ #いいねでこちゃ"],
    10: ["ちょっと一息つこ", "みんななにしてるの〜？？", "コーヒータイム", "次の休憩まであと何時間…", "そろそろ眠くなってきた",
         "やる気スイッチどこ…", "小腹すいた", "仕事or授業終わったら何しよう", "つーわぼ #いいねでこちゃ"],
    11: ["お昼ごはんどうしよ〜", "ランチ何にしようか迷う", "おすすめのランチある？", "お弁当派？外食派？", 
         "もうお昼ごはん食べた？", "午後もがんばるためにたくさん食べる", "ご飯よりお昼寝したい", "食べすぎ注意！", "つーわぼ #いいねでこちゃ"],
    12: ["ランチなう", "お昼ごはん美味しすぎ", "午後の予定考え中", "デザートも食べたい", "眠くなってきた…", 
         "午後もがんばるぞ！", "ご飯食べると元気でる", "みんな何食べた？", "つーわぼ #いいねでこちゃ"],
    13: ["午後の仕事or授業スタート！", "ランチ後って眠くなるよね", "集中力が試される時間", "眠気と戦い中",
         "カフェ行きたい", "今日の午後は長そう…", "もうひと頑張り！", "休憩時間が待ち遠しい", "つーわぼ #いいねでこちゃ"],
    14: ["まだお昼の眠気が抜けない", "そろそろおやつの時間", "午後のコーヒーは必須", "少し歩いてリフレッシュしよ",
         "あと何時間で終わるんだ…", "次の休憩までが遠い", "頑張る人えらい！", "ちょっと息抜きしよ", "つーわぼ #いいねでこちゃ"],
    15: ["おやつタイム〜", "あと少しで終業時間…", "チョコ食べたい", "お腹すいてきた…", "仕事が終わる気がしない",
         "頑張れ自分！", "時計見すぎる時間", "終わったら何しようかな", "つーわぼ #いいねでこちゃ"],
    16: ["あと少しで仕事終わる！！さいこーー", "夕方の空って綺麗だよね", "帰りたい…", "今日も1日お疲れ様！",
         "あとちょっと頑張ろう！", "晩ごはん何食べよう", "帰り道が好き", "明日の予定考えなきゃ", "つーわぼ #いいねでこちゃ"],
    17: ["みんなおつかれさま！", "夕方のこの時間、好きかも", "仕事or学校終わった？", "帰り道の空がきれい", 
         "リラックスタイム開始！", "今日頑張った自分を褒める", "友達とご飯行きたい", "夕方の風が気持ちいい", "つーわぼ #いいねでこちゃ"],
    18: ["夜ご飯の時間だ〜！", "今日の夕飯は何だと思う？", "みんな何食べるの？", "外食したい気分", 
         "家でのんびりご飯もいいよね", "お腹ぺこぺこ", "自炊するか迷う…", "夜ご飯のメニュー決まらん！", "つーわぼ #いいねでこちゃ"],
    19: ["夜ご飯食べ終わった？", "この時間はYouTubeかネトフリ見たくなる", "ゲームする時間！", "ご飯食べすぎたかも…",
         "お風呂入るのめんどい", "もう眠い…", "夜の時間ってあっという間", "寝る前にちょっとだけSNS", "つーわぼ #いいねでこちゃ"],
    20: ["夜のリラックスタイム", "そろそろお風呂入ろうかな", "1日あっという間だった", "明日の準備しなきゃ",
         "今日やり残したことある…", "夜の音楽タイム", "まったり時間が最高", "寝る前にストレッチ", "つーわぼ #いいねでこちゃ"],
    21: ["そろそろ寝る準備してる？", "今日の振り返り中", "明日も頑張ろう", "ちょっとだけ夜更かし",
         "夜の空って落ち着く", "眠いけどスマホいじっちゃう", "布団の中が天国", "寝落ちしそう", "つーわぼ #いいねでこちゃ"],
    22: ["寝る前のリラックスタイム", "夜更かしする人〜？", "今日1日どうだった？", "もう寝なきゃだけどSNS見ちゃう",
         "明日こそ早寝する！", "ベッドが幸せすぎる", "いい夢見れますように", "目閉じたら一瞬で朝きそう", "つーわぼ #いいねでこちゃ"],
    23: ["そろそろ寝ようかな", "夜って色々考えちゃうよね", "眠れない人いる？", "枕が気持ちよすぎる",
         "夜の静けさが好き", "布団に入るとスマホ触っちゃう", "寝る前にちょっとお話したい", "おやすみなさい〜", "つーわぼ #いいねでこちゃ"],
    24: ["こんな時間まで起きてる人いる？", "そろそろ寝る準備しよ〜", "明日が来るの早すぎる", "寝ようと思ったのに眠くない",
         "誰かと話したくなる時間", "夜更かししすぎたかも…", "気づいたらこんな時間", "そろそろ夢の中へ…", "つーわぼ #いいねでこちゃ"]
}

# DM誘導文（投稿の最後に追加する文）
dm_text = " 、だれかDMしませんか。"

# 時間帯に応じた投稿を取得（DM誘導文を4回に1回追加）
def get_time_based_post():
    now = datetime.now(jst).hour
    if now == 0:
        now = 24  # 0時を24時として扱う
    post = random.choice(post_texts.get(now, ["つーわぼ #いいねでこちゃ"]))
    if random.randint(1, 4) == 1:
        post += dm_text
    return post

# --- 自動いいね・フォロー・自動返信機能 ---

# 自動いいね・フォロー機能
def auto_like_and_follow():
    # いいねする対象のハッシュタグ
    hashtags = ["#いいねでこちゃ", "#いいねでレター"]
    # 「通話募集」を含む投稿の場合、男性ならいいね＆フォローする
    try:
        # ハッシュタグを含む投稿にいいね
        for tag in hashtags:
            posts = client.search_posts(tag)
            for post in posts:
                client.like_post(post['id'])
                print(f"Liked post with tag {tag}: {post['id']}")
        # 「通話募集」を含む投稿を検索
        posts = client.search_posts("通話募集")
        for post in posts:
            user = client.get_user(post['user_id'])
            if user.get('gender') == 'male':
                client.like_post(post['id'])
                client.follow_user(user['id'])
                print(f"Liked and followed {user['username']}")
    except Exception as e:
        print(f"Error in auto_like_and_follow: {e}")

# 自動返信機能
def auto_reply():
    try:
        chats = client.get_chats()
        for chat in chats:
            if not chat.get('is_replied'):
                sender_id = chat['sender_id']
                reply_text = "はじめまして！インスタではなそ、@1316_21 これです！"
                client.send_message(sender_id, reply_text)
                print(f"Sent message to {sender_id}")
    except Exception as e:
        print(f"Error in auto_reply: {e}")

# --- メインループ用スレッド定義 ---
def time_based_posting_loop():
    # 初回投稿（ビルド完了後すぐ）
    print("🚀 初回投稿開始")
    for client in yay_clients:
        try:
            first_post = get_time_based_post()
            print(f'📢 {client.email} が初回投稿: {first_post}')
            client.create_post(first_post)
            print(f'✅ 初回投稿成功 ({client.email})')
        except Exception as e:
            print(f'❌ 初回投稿失敗 ({client.email}): {e}')
    # 次の投稿タイミングまで待機
    now = datetime.now(jst)
    next_post_minute = (now.minute // 15 + 1) * 15
    if next_post_minute == 60:
        next_post_minute = 0
        next_hour = now.hour + 1
    else:
        next_hour = now.hour
    next_time = now.replace(hour=next_hour, minute=next_post_minute, second=0, microsecond=0)
    sleep_time = (next_time - datetime.now(jst)).total_seconds()
    print(f"⏳ 初回投稿後、次の投稿まで {int(sleep_time)} 秒待機")
    time.sleep(sleep_time)
    
    # メインループ：15分ごとに各アカウントで投稿
    while True:
        now = datetime.now(jst)
        current_minute = now.minute
        next_post_minute = (current_minute // 15 + 1) * 15
        if next_post_minute == 60:
            next_post_minute = 0
            next_hour = now.hour + 1
        else:
            next_hour = now.hour
        for client in yay_clients:
            try:
                post_content = get_time_based_post()
                print(f'📢 {client.email} が投稿: {post_content}')
                client.create_post(post_content)
                print(f'✅ 投稿成功 ({client.email})')
            except Exception as e:
                print(f'❌ 投稿エラー ({client.email}): {e}')
        next_time = now.replace(hour=next_hour, minute=next_post_minute, second=0, microsecond=0)
        sleep_time = (next_time - datetime.now(jst)).total_seconds()
        print(f"⏳ 次の投稿予定: {next_time.strftime('%Y-%m-%d %H:%M:%S')}（{int(sleep_time)}秒後）")
        time.sleep(sleep_time)

def auto_actions_loop():
    # このループは1分ごとに自動いいね・フォロー・自動返信を実行
    while True:
        for client in yay_clients:
            try:
                auto_like_and_follow()  # いいね・フォロー
                auto_reply()            # 自動返信
            except Exception as e:
                print(f"Auto action error ({client.email}): {e}")
        time.sleep(60)

# --- メイン ---
import threading

t_posting = threading.Thread(target=time_based_posting_loop, daemon=True)
t_actions = threading.Thread(target=auto_actions_loop, daemon=True)

t_posting.start()
t_actions.start()

# メインスレッドはずっと待機
while True:
    time.sleep(60)
