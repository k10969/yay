import yaylib
import random
import time
import os
from datetime import datetime, timedelta
import pytz

print("🚀 スクリプト開始")

# 日本時間（JST）のタイムゾーン設定
jst = pytz.timezone('Asia/Tokyo')

# 環境変数からアカウント情報を取得（例: "email1:password1,email2:password2"）
account_list = os.getenv('YAY_ACCOUNTS', '').split(',')

# ログイン情報リスト作成
accounts = []
for account in account_list:
    parts = account.split(':')
    if len(parts) == 2:
        accounts.append({'email': parts[0], 'password': parts[1]})

print("取得したアカウント情報:", accounts)

# 各時間帯の投稿内容（1時間ごとに8個の候補）
# ※必要に応じて7〜22時も同様に記述してください。
post_texts = {
    1: ["もう1時！？時間早すぎ…", "深夜のネットサーフィンが止まらない", "誰か電話しない？", "コンビニ行きたい",
        "夜中のラーメンは最強", "眠れない人いる〜？", "そろそろ寝ないと", "明日起きれるかな…"],
    2: ["深夜組集合〜！", "もうそろそろ寝ないと", "YouTube見てたらこんな時間", "小腹すいたなぁ…",
        "夜中に食べるお菓子は罪だけど美味い", "朝が来る前に寝るぞ！", "寝る前にストレッチしよ", "ラジオ聴いてる"],
    3: ["この時間起きてるのは少数派…？", "完全に夜更かししすぎた", "3時って一番眠くなる時間…", "もう寝なきゃ…",
        "夜の静けさって落ち着く", "SNS見てたら時間溶けた", "そろそろ寝落ちしそう", "夜中に考え事しちゃう…"],
    4: ["おはようって言っていいのか微妙な時間", "早起き？それとも夜更かし？", "空が少し明るくなってきた",
        "そろそろ朝の準備するか…", "こんな時間に起きてるの自分だけ？", "朝ごはん食べる人いる？", "眠すぎる…", "今日の予定考え中"],
    5: ["朝が来た〜", "完全に寝不足", "眠いけど頑張る", "そろそろ朝ごはん食べようかな？", 
        "早起きさんいる？", "今日も一日頑張ろう", "なんだかんだ夜更かししちゃった", "おはよう世界"],
    6: ["おはよ〜！今日も頑張ろっ", "ねむい…あと5分寝たい", "朝ごはんはパン派？ごはん派？", "顔洗ったら少しスッキリ！", 
        "もう少し布団にいたいなぁ…", "朝の空気って気持ちいい", "今日の服どうしよ〜", "学校or仕事ファイト🔥"],
    7: ["まだちょっと眠い…", "朝ごはん食べた？", "今日の天気どうかな？", "みんな何時に起きるタイプ？", 
        "朝の準備バタバタする", "通勤中〜～", "コーヒー飲んで目覚まそ", "今日も楽しい1日になりますように"],
    8: ["眠すぎ", "電車混んでる…", "カフェでモーニングしてる", "職場ついた〜", 
        "朝って時間経つの早いよね", "今日の予定なにかある？", "みんな頑張りすぎずにね", "休日が待ち遠しい…！"],
    9: ["そろそろお腹すいてきたかも", "仕事中だ〜", "今日化粧ノリいい感じ", "朝のカフェって落ち着くよね", 
        "集中しなきゃだけど眠くなるよね…", "適度に休憩も大事", "今日やることメモしよ", "お昼なに食べよ〜？"],
    10: ["ちょっと一息つこ", "みんななにしてるの〜？？", "そろそろお昼の時間近づいてきたね", "眠くて頭まわらない", 
         "集中モードに入ろうかな", "休憩に入ったのでカフェでリラックス中", "音楽聞きながらリラックス", "誰かと話したいな〜"],
    11: ["お昼ごはんどうしよ〜", "ランチ何にしようか迷う", "お昼休みまであとちょっと…", "夜外食しようかな？", 
         "誰か一緒にランチ行こ〜", "お昼に甘いもの食べたい", "午後もがんばるぞ", "お昼寝したくなる時間"],
    12: ["ランチなう", "お昼ごはん美味しすぎ", "午後もがんばるぞー！！", "ちょっと眠くなってきた…", 
         "ごはん食べたら元気出た😌", "みんな何食べた？", "デザート食べたい", "午後の予定ある人〜？"],
    13: ["午後の仕事or授業スタート！", "ランチ後って眠くなるよね", "午後もがんばろ〜！", "コーヒー飲んで気合い入れよ",
         "午後は何しようかな？", "あー、めんどくさいなぁ", "休憩時間が待ち遠しい…", "ちょっと散歩しようかな"],
    14: ["まだお昼の眠気が抜けない", "そろそろおやつの時間", "午後の仕事やる気スイッチどこ？", "学校or仕事終わった人いる？",
         "何か面白いことないかな〜", "音楽聞きながらリラックス", "みんな午後は何してるの？", "ちょっと眠気覚ましにストレッチ！"],
    15: ["おやつタイム〜", "あと少しで終業時間…", "カフェに寄りたいな", "夕方の予定ある？", 
         "午後の授業or会議、がんばろう！", "今日のニュースチェック中", "そろそろ疲れてきた", "ちょっと仮眠しよっかな"],
    16: ["あと少しで仕事終わる！！さいこーー", "夕方の空って綺麗だよね", "今日の晩ごはん何にしよう？", "仕事帰りに寄り道しよっかな〜",
         "そろそろお家に帰る準備", "疲れたけどあと少し！", "カフェでのんびり中", "お風呂入ってチルしたい🥺"],
    17: ["みんなおつかれさま！", "夕方のこの時間、好きかも", "そろそろ帰ろう", "夕飯の準備しないと",
         "誰かとご飯行きたいな〜", "家に帰ったら即ゴロゴロしたい", "暗くなるの早くなったなぁ…", "まだ仕事の人、がんばれ"],
    18: ["夜ご飯の時間だ〜！", "今日の夕飯は何だと思う？", "仕事終わりのビール最高", "晩ごはん何食べた？"],
    19: ["夜ご飯食べ終わった？", "この時間はYouTubeかネトフリ見たくなる", "のんびりタイム"],
    20: ["夜のリラックスタイム", "そろそろお風呂入ろうかな", "一緒に寝る前のストレッチしよっか"],
    21: ["そろそろ寝る準備してる？", "今日の振り返り中", "お風呂上がりのアイス最高"],
    22: ["寝る前のリラックスタイム", "夜更かしする人〜？", "今日も1日お疲れさま"],
    23: ["そろそろ寝ようかな", "夜って色々考えちゃうよね", "えち時間になってきたね", "気持ちいことしたいね"],
    24: ["こんな時間まで起きてる人いる？", "そろそろ寝る準備しよ〜", "だれか電話しませんか", "楽しいことしよー"]
}

# 0時は通常の24時として扱うので、post_texts[0] はそのまま利用可能です。

# 4回に1回、投稿の最後に追加するDM誘導文
dm_text = " だれかDMしませんか、フォローもお願いします！"

# 時間帯に応じた投稿をランダムに取得（4個選んで、4回に1回DM誘導を追加）
def get_time_based_posts():
    current_hour = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst).hour
    if current_hour == 0:
        current_hour = 24  # 0時は24時として扱う

    print(f"現在の時刻（JST）: {current_hour} 時")  # デバッグ用

    posts = post_texts.get(current_hour, ["なにしてるの〜？💬", "ちょっとおしゃべりしたい💖"])
    if not posts:
        print("⚠️ 投稿する内容がありません！")
        return ["なにしてるの〜？💬"]

    # 4個の投稿をランダムに選ぶ（候補数が4未満の場合はそのまま）
    selected_posts = random.sample(posts, min(4, len(posts)))

    for i in range(len(selected_posts)):
        if random.randint(1, 4) == 1:
            selected_posts[i] += dm_text

    return selected_posts

# ログイン処理（各アカウントごとに10～30秒の待機を挟む）
yay_clients = []
for account in accounts:
    try:
        time.sleep(random.randint(10, 30))
        client = yaylib.Client()
        client.login(account["email"], account["password"])
        yay_clients.append(client)
        print(f"✅ {account['email']} でログイン成功")
    except Exception as e:
        print(f"❌ {account['email']} のログインに失敗: {e}")

if len(yay_clients) == 0:
    print("⚠️ ログイン成功したアカウントがありません。処理を終了します。")
    exit()

print(f"ログイン成功したアカウント数: {len(yay_clients)}")

# 🚀 ビルド完了後すぐにテスト投稿を実施
for client in yay_clients:
    try:
        test_post = get_time_based_posts()[0]
        print(f"テスト投稿内容（{client.email}）: {test_post}")
        response = client.create_post(test_post)
        print(f"✅ 初回テスト投稿成功 ({client.email}): {response}")
    except Exception as e:
        print(f"❌ 初回テスト投稿失敗 ({client.email}): {e}")

# 🎯 メインの投稿ループ（15分ごと）
while True:
    try:
        now = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst)
        current_minute = now.minute

        # 次の投稿タイミングを計算（0分, 15分, 30分, 45分）
        next_post_minute = (current_minute // 15 + 1) * 15
        if next_post_minute >= 60:
            next_post_minute = 0
            next_time = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
        else:
            next_time = now.replace(minute=next_post_minute, second=0, microsecond=0)

        print(f"⏳ 現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}, 次回投稿時刻: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 各アカウントで投稿（各アカウントからランダムな投稿内容を1つずつ投稿）
        for client in yay_clients:
            post_content = random.choice(get_time_based_posts())
            try:
                response = client.create_post(post_content)
                print(f"📢 投稿成功 ({client.email}) [{now.strftime('%Y-%m-%d %H:%M:%S')}]: {post_content} | Response: {response}")
            except yaylib.errors.HTTPError as e:
                print(f"❌ 投稿エラー ({client.email}): {e}")
                if "429" in str(e):
                    wait_time = random.randint(300, 900)  # 5〜15分待機
                    print(f"🚧 429エラー: {wait_time} 秒待機して再試行")
                    time.sleep(wait_time)
                elif "403" in str(e):
                    print("⚠️ 403エラー: このアカウントを使用停止")
                    yay_clients.remove(client)
                elif "401" in str(e):
                    print("⚠️ 401エラー: 認証エラー")
                    yay_clients.remove(client)
                else:
                    print("⚠️ その他のエラー発生")
                    continue

        # 次の投稿までの待機時間を計算
        sleep_time = (next_time - datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(jst)).total_seconds()
        print(f"⏳ 次の投稿まで {int(sleep_time)} 秒待機")
        time.sleep(sleep_time)

    except Exception as e:
        print(f"❌ 致命的なエラー発生: {e}")
        time.sleep(1800)  # 30分待機して再試行
