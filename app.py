import streamlit as st
import random

# --- データ定義 ---
CHARACTERS = {
    "水龍の巫女": {
        "hp": 100, "max_hp": 100,  "speed": 10,
        "attack": 20, "defense": 10, "element": "water", "image_path": "image/water.png",
        "initial_skill": {"name": "翠明流流転斬り", "type": "攻撃", "power": 30, "turn": 1, "image": "image/water_skill1.png", "element": "water"}
    },
    "風の魔女": {
        "hp": 100, "max_hp": 100,  "speed": 12,
        "attack": 25, "defense": 5, "element": "wind", "image_path": "image/wind.png",
        "initial_skill": {"name": "ウィンドカッター", "type": "攻撃", "power": 30, "turn": 1, "image": "image/wind_skill1.png", "element": "wind"}
    },
    "月夜の暗殺者": {
        "hp": 100, "max_hp": 100, "speed": 14,
        "attack": 15, "defense": 8, "element": "shadow", "image_path": "image/shadow.png",
        "initial_skill": {"name": "シャドーナイフ", "type": "攻撃", "power": 40, "turn": 1, "image": "image/shadow_skill1.png", "element": "shadow"}
    },
}

# 獲得可能なランダムスキルのプール
WATER_SKILL_POOL = [
    {"name": "翠明流水沫斬り", "type": "攻撃", "power": 30, "turn": 1, "image": "image/water_a1.png", "element": "water"},  
    {"name": "翠明流雫刃", "type": "攻撃", "power": 20, "turn": 1, "image": "image/water_a2.png", "element": "water"},
    {"name":"翠明流流水剣逆巻き", "type": "攻撃", "power": 50, "turn": 2, "image": "image/water_a3.png", "element": "water"},
    {"name":"翠明流連波突き", "type": "攻撃", "power": 40, "turn": 2, "image": "image/water_a4.png", "element": "water"},
    {"name":"翠明流蒼龍昇天", "type": "攻撃", "power": 80, "turn": 3, "image": "image/water_a5.png", "element": "water"},
    {"name":"翠明流鏡水月", "type": "攻撃", "power": 70, "turn": 3, "image": "image/water_a6.png", "element": "water"},
    {"name":"翠明流海神葬", "type": "攻撃", "power": 100, "turn": 4, "image": "image/water_a7.png", "element": "water"},
    {"name":"恵雨の癒し", "type": "回復", "power": 50, "turn": 2, "image": "image/water_heal.png", "element": "water"},
    {"name":"水鏡の加護","type":"強化","power":20,"turn":2,"image":"image/water_power.png","element":"water"},
    {"name":"水陣結界","type":"防御","power":20,"turn":2,"image":"image/water_block.png","element":"water"}
]
WIND_SKILL_POOL = [
    {"name": "ガストショット", "type": "攻撃", "power": 40, "turn": 1, "image": "image/winda1.png", "element": "wind"},
    {"name": "エアリアルブレード", "type": "攻撃", "power": 50, "turn": 1, "image": "image/winda2.png", "element": "wind"},
    {"name":"トルネードバインド", "type": "攻撃", "power": 60, "turn": 2, "image": "image/winda3.png", "element": "wind"},
    {"name":"ハウリングストーム", "type": "攻撃", "power": 80, "turn": 3, "image": "image/winda4.png", "element": "wind"},
    {"name":"エア・プレッシャー", "type": "攻撃", "power": 70, "turn": 3, "image": "image/winda5.png", "element": "wind"},
    {"name":"アトモス・カタストロフ", "type": "攻撃", "power": 100, "turn": 4, "image": "image/winda6.png", "element": "wind"},
    {"name":"ウィンド・ブリーズ", "type": "回復", "power": 60, "turn": 2, "image": "image/windheal.png", "element": "wind"},
    {"name":"ヘイスト・ウィング","type":"強化","power":30,"turn":2,"image":"image/windpower.png","element":"wind"},
    {"name":"エア・バリア","type":"防御","power":30,"turn":2,"image":"image/windblock.png","element":"wind"}
]
SHADOW_SKILL_POOL = [
    {"name": "シャドウスラスト", "type": "攻撃", "power": 30, "turn": 1, "image": "image/shadowa1.png", "element": "shadow"},
    {"name": "ダークニードル", "type": "攻撃", "power": 20, "turn": 1, "image": "image/shadowa2.png", "element": "shadow"},
    {"name":"シャドウバインド", "type": "攻撃", "power": 50, "turn": 2, "image": "image/shadowa3.png", "element": "shadow"},
    {"name":"ダークエッジ・クロス", "type": "攻撃", "power": 70, "turn": 2, "image": "image/shadowa4.png", "element": "shadow"},
    {"name":"ナイトメア・シザーズ", "type": "攻撃", "power": 90, "turn": 3, "image": "image/shadowa5.png", "element": "shadow"},
    {"name":"シャドウクローン・ラッシュ", "type": "攻撃", "power": 80, "turn": 3, "image": "image/shadowa6.png", "element": "shadow"},
    {"name":"アビス・イクリプス", "type": "攻撃", "power": 100, "turn": 4, "image": "image/shadowa7.png", "element": "shadow"},
    {"name":"シャドウヒール", "type": "回復", "power": 40, "turn": 2, "image": "image/shadowheal.png", "element": "shadow"},
    {"name":"影の帳","type":"強化","power":25,"turn":2,"image":"image/shadowpower.png","element":"shadow"},
    {"name":"シャドウガード","type":"防御","power":25,"turn":2,"image":"image/shadowblock.png","element":"shadow"}
]
# --- 敵データの定義（スキル付き） ---
ENEMIES = [
    {
        "name": "ゴブリン", "type": "mob", "floor_range": (1, 19),
        "hp": 50, "max_hp": 50, "speed": 8, "attack": 10, 
        "image": "image/goblin.png",
        "skills": [
            {"name": "なぐる", "type": "攻撃", "power": 10, "element": "none"},
            {"name": "ひっかき", "type": "攻撃", "power": 15,  "element": "none"}
        ]
    },
    {
        "name": "スライム", "type": "mob", "floor_range": (1, 19),
        "hp": 30, "max_hp": 30, "speed": 5, "attack": 5, 
        "image": "image/slime.png",
        "skills": [
            {"name": "体当たり", "type": "攻撃", "power": 8,  "element": "none"},
            {"name": "どろかけ", "type": "攻撃", "power": 5, "element": "none"}
        ]
    },
    {
        "name":"草むらトカゲ", "type": "mob", "floor_range": (1, 19),
        "hp": 40, "max_hp": 40, "speed": 10, "attack": 8,
          "image": "image/st1en1.png",
        "skills":[
         {"name": "かみつく", "type": "攻撃", "power": 8, "element": "none"},
         {"name": "尻尾攻撃", "type": "攻撃", "power": 10, "element": "none"}
       ]
    },
    {
        "name": "蜂の兵隊","type": "mob", "floor_range": (1, 19),
        "hp": 35, "max_hp": 35, "speed": 12, "attack": 12,
        "image": "image/st1en2.png",
        "skills": [
            {"name": "ハチの針", "type": "継続", "power": 12, "element": "none"},
            {"name": "蜂の巣", "type": "攻撃", "power": 14, "element": "none"}
        ]
    },
    {
        "name":"野犬","type": "mob", "floor_range": (1, 19),
        "hp": 45, "max_hp": 45, "speed": 11, "attack": 13,
        "image": "image/st1en3.png",
        "skills":[
            {"name": "かみつく", "type": "攻撃", "power": 13, "element": "none"},
            {"name": "ひっかき", "type": "攻撃", "power": 15, "element": "none"}
        ]
    },
    {
        "name":"大王スライム","type": "boss", "floor": 20,
        "hp": 100, "max_hp": 100, "speed": 5, "attack": 20,
        "image": "image/st1en4.png",
        "skills":[
            {"name": "スライムボール", "type": "継続", "power": 25, "element": "none"},
            {"name": "再結合", "type": "回復", "power": 20, "element": "none"}
        ]
    },
    {
        "name":"ロックゴーレム","type": "mob", "floor_range": (21, 39),
        "hp": 80, "max_hp": 80, "speed": 4, "attack": 25,
        "image": "image/st2en1.png",
        "skills":[
            {"name": "岩石投げ", "type": "攻撃", "power": 30, "element": "rock"},
            {"name": "防御態勢", "type": "防御", "power": 20, "element": "rock"}
        ]
    },
    {
        "name":"影の亡霊","type": "mob", "floor_range": (21, 39),
        "hp": 60, "max_hp": 60, "speed": 9, "attack": 18,
        "image": "image/st2en2.png",
        "skills":[
            {"name": "シャドウスラスト", "type": "攻撃", "power": 30, "element": "shadow"},
            {"name": "ダークエッジ", "type": "攻撃", "power": 40, "element": "shadow"}
        ]
    },
    {
        "name":"洞窟コウモリ","type": "mob", "floor_range": (21, 39),
        "hp": 70, "max_hp": 70, "speed": 12, "attack": 20,
        "image": "image/st2en3.png",
        "skills":[
            {"name": "かみつく", "type": "攻撃", "power": 18, "element": "none"},
            {"name": "超音波", "type": "攻撃", "power": 20, "element": "shadow"}
        ]
    },
    {
        "name":"地底グモ","type": "mob", "floor_range": (21, 39),
        "hp": 70, "max_hp": 70, "speed": 10, "attack": 15,
        "image": "image/st2en4.png",
        "skills":[
            {"name": "糸を張る", "type": "攻撃", "power": 30, "element": "shadow"},
            {"name": "毒針", "type": "継続", "power": 40, "element": "shadow"}
        ]
    },
    {
        "name":"闇の鎧騎士","type": "mob", "floor_range": (21, 39),
        "hp": 90, "max_hp": 90, "speed": 6, "attack": 25,
        "image": "image/st2en5.png",
        "skills":[
            {"name": "ダークスラスト", "type": "攻撃", "power": 50, "element": "shadow"},
            {"name": "影の防御", "type": "防御", "power": 30, "element": "shadow"}
        ]
    },
    {
        "name":"暗黒地殻獣","type": "boss", "floor": 40,
        "hp": 200, "max_hp": 200, "speed": 5, "attack": 30,
        "image": "image/st2en6.png",
        "skills":[
            {"name": "地殻変動", "type": "攻撃", "power": 60, "element": "rock"},
            {"name": "暗黒の呪い", "type": "継続", "power": 40, "element": "shadow"},
            {"name": "岩盤障壁", "type": "防御", "power": 50, "element": "rock"},
            {"name": "テクトニッククラッシュ", "type": "攻撃", "power": 80, "element": "rock"}
        ]
    },
    {
        "name":"イフリート","type": "mob", "floor_range": (41, 59),
        "hp": 120, "max_hp": 120, "speed": 10, "attack": 35,
        "image": "image/st3en1.png",
        "skills":[
            {"name": "炎の嵐", "type": "攻撃", "power": 60, "element": "fire"},
            {"name": "火炎防御", "type": "防御", "power": 30, "element": "fire"}
        ]
    },
    {
        "name":"溶岩亀","type": "mob", "floor_range": (41, 59),
        "hp": 150, "max_hp": 150, "speed": 5, "attack": 40,
        "image": "image/st3en2.png",
        "skills":[
            {"name": "溶岩弾", "type": "継続", "power": 60, "element": "fire"},
            {"name": "硬化", "type": "防御", "power": 40, "element": "fire"}
        ]
    },
    {
        "name":"フェニックス","type": "mob", "floor_range": (41, 59),
        "hp": 120, "max_hp": 120, "speed": 12, "attack": 35,
        "image": "image/st3en3.png",
        "skills":[
            {"name": "炎の翼撃", "type": "攻撃", "power": 50, "element": "fire"},
            {"name": "火炎防御", "type": "防御", "power": 30, "element": "fire"}
        ]
    },
    {
        "name":"マグマゴーレム","type": "mob", "floor_range": (41, 59),
        "hp": 200, "max_hp": 200, "speed": 4, "attack": 45,
        "image": "image/st3en4.png",
        "skills":[
            {"name": "マグマ投げ", "type": "攻撃", "power": 70, "element": "fire"},
            {"name": "溶岩の鎧", "type": "防御", "power": 50, "element": "fire"}
        ]
    },
    {
        "name":"地獄の炎の魔術師","type": "mob", "floor_range": (41, 59),
        "hp": 150, "max_hp": 150, "speed": 6, "attack": 40,
        "image": "image/st3en5.png",
        "skills":[
            {"name": "地獄の炎", "type": "継続", "power": 60, "element": "fire"},
            {"name": "魔法防御", "type": "防御", "power": 40, "element": "fire"}
        ]
    },
    {
        "name":"灼熱の焔龍","type": "boss", "floor": 60,
        "hp": 300, "max_hp": 300, "speed": 8, "attack": 50,
        "image": "image/st3en6.png",
        "skills":[
            {"name": "インフェルノブレス", "type": "攻撃", "power": 80, "element": "fire"},
            {"name": "マグマドロップ", "type": "継続", "power": 50, "element": "fire"},
            {"name": "ヒートストーム", "type": "攻撃", "power": 70, "element": "fire"},
            {"name": "炎の防御", "type": "防御", "power": 60, "element": "fire"}
        ]
    },
    {
        "name":"氷の妖精","type": "mob", "floor_range": (61, 79),
        "hp": 200, "max_hp": 200, "speed": 12, "attack": 25,
        "image": "image/st4en1.png",
        "skills":[
            {"name": "氷のいたずら", "type": "攻撃", "power": 70, "element": "ice"},
            {"name": "氷の防御", "type": "防御", "power": 50, "element": "ice"}
        ]
    },
    {
        "name":"雪狼","type": "mob", "floor_range": (61, 79),
        "hp": 220, "max_hp": 220, "speed": 12, "attack": 30,
        "image": "image/st4en2.png",
        "skills":[
            {"name": "氷の牙", "type": "攻撃", "power": 70, "element": "ice"},
            {"name": "雪の防御", "type": "防御", "power": 40, "element": "ice"}
        ]
    },
    {
        "name":"氷塊兵","type": "mob", "floor_range": (61, 79),
        "hp": 250, "max_hp": 250, "speed": 10, "attack": 25,
        "image": "image/st4en3.png",
        "skills":[
            {"name": "氷の槍", "type": "攻撃", "power": 80, "element": "ice"},
            {"name": "氷の壁", "type": "防御", "power": 40, "element": "ice"}
        ]
    },
    {
        "name":"ブリザードコウモリ","type": "mob", "floor_range": (61, 79),
        "hp": 200, "max_hp": 200, "speed": 12, "attack": 30,
        "image": "image/st4en4.png",
        "skills":[
            {"name": "氷の超音波", "type": "攻撃", "power": 70, "element": "ice"},
            {"name": "氷の防御", "type": "防御", "power": 40, "element": "ice"}
        ]
    },
    {
        "name":"氷の魔像","type": "mob", "floor_range": (61, 79),
        "hp": 250, "max_hp": 250, "speed": 10, "attack": 25,
        "image": "image/st4en5.png",
        "skills":[
            {"name": "氷の彗星", "type": "攻撃", "power": 90, "element": "ice"},
            {"name": "氷の壁", "type": "防御", "power": 40, "element": "ice"}
        ]
    },
    {
        "name":"氷華の魔女","type": "boss", "floor": 80,
        "hp": 400, "max_hp": 400, "speed": 12, "attack": 30,
        "image": "image/st4en6.png",
        "skills":[
            {"name": "氷の華", "type": "攻撃", "power": 100, "element": "ice"},
            {"name": "氷の防御", "type": "防御", "power": 50, "element": "ice"},
            {"name": "クリスタルレイン", "type": "攻撃", "power": 80, "element": "ice"},
            {"name": "フロストプリズン", "type": "防御", "power": 100, "element": "ice"},
            {"name": "絶対零度", "type": "継続", "power": 60, "element": "ice"}
        ]
    },
    {
        "name":"警備ドローン","type": "mob", "floor_range": (81, 99),
        "hp": 300, "max_hp": 300, "speed": 12, "attack": 20,
        "image": "image/st5en1.png",
        "skills":[
            {"name": "レーザー", "type": "攻撃", "power": 100, "element": "thunder"},
            {"name": "防御シールド", "type": "防御", "power": 50, "element": "thunder"}
        ]
    },
    {
        "name":"電撃スライム","type": "mob", "floor_range": (81, 99),
        "hp": 320, "max_hp": 320, "speed": 12, "attack": 30,
        "image": "image/st5en2.png",
        "skills":[
            {"name": "電撃弾", "type": "攻撃", "power": 120, "element": "thunder"},
            {"name": "静電気防御", "type": "防御", "power": 60, "element": "thunder"}
        ]
    },
    {
        "name":"サイバー忍者","type": "mob", "floor_range": (81, 99),
        "hp": 350, "max_hp": 350, "speed": 14, "attack": 40,
        "image": "image/st5en3.png",
        "skills":[
            {"name": "サイバー斬撃", "type": "攻撃", "power": 130, "element": "thunder"},
            {"name": "電子防御", "type": "防御", "power": 50, "element": "thunder"}
        ]
    },
    {
        "name":"自動砲塔","type": "mob", "floor_range": (81, 99),
        "hp": 360, "max_hp": 360, "speed": 10, "attack": 50,
        "image": "image/st5en4.png",
        "skills":[
            {"name": "自動射撃", "type": "攻撃", "power": 150, "element": "thunder"},
            {"name": "防御シールド", "type": "防御", "power": 70, "element": "thunder"}
        ]
    },
    {
        "name":"ハッキングコア","type": "mob", "floor_range": (81, 99),
        "hp": 360, "max_hp": 360, "speed": 12, "attack": 40,
        "image": "image/st5en5.png",
        "skills":[
            {"name": "ハッキング", "type": "攻撃", "power": 120, "element": "thunder"},
            {"name": "システム防御", "type": "防御", "power": 60, "element": "thunder"}
        ]
    },
    {
        "name":"量産型AI軍団","type": "boss", "floor": 100,
        "hp": 400, "max_hp": 400, "speed": 10, "attack": 50,
        "image": "image/st5en6.png",
        "skills":[
            {"name": "一斉掃射", "type": "攻撃", "power": 200, "element": "thunder"},
            {"name": "量産型防御", "type": "防御", "power": 70, "element": "thunder"},
            {"name":"バックアップシステム", "type":"回復", "power":50, "element":"thunder"},
            {"name":"電磁パルス", "type":"継続", "power":150, "element":"thunder"}
        ]
    },
    
    {
        "name":"虚無の騎士","type": "mob", "floor_range": (101, 119),
        "hp": 420, "max_hp": 420, "speed": 10, "attack": 60,
        "image": "image/st6en1.png",
        "skills":[
            {"name": "虚無の刃", "type": "攻撃", "power": 200, "element": "none"},
            {"name": "虚無の防御", "type": "防御", "power": 80, "element": "none"}
        ]
    },
    {
        "name":"時間の澱み","type": "mob", "floor_range": (101, 119),
        "hp": 430, "max_hp": 430, "speed": 10, "attack": 50,
        "image": "image/st6en2.png",
        "skills":[
            {"name": "時間停止", "type": "攻撃", "power": 220, "element": "none"},
            {"name": "時間の防御", "type": "防御", "power": 70, "element": "none"}
        ]
    },
    {
        "name":"空間歪曲獣","type": "mob", "floor_range": (101, 119),
        "hp": 450, "max_hp": 450, "speed": 10, "attack": 55,
        "image": "image/st6en3.png",
        "skills":[
            {"name": "空間歪曲", "type": "攻撃", "power": 250, "element": "none"},
            {"name": "空間の防御", "type": "防御", "power": 90, "element": "none"}
        ]
    },
    {
        "name":"パラレル分身","type": "mob", "floor_range": (101, 119),
        "hp": 450, "max_hp": 450, "speed": 12, "attack": 40,
        "image": "image/st6en4.png",
        "skills":[
            {"name": "分身の術", "type": "攻撃", "power": 250, "element": "none"},
            {"name": "分身の防御", "type": "防御", "power": 70, "element": "none"}
        ]
    },
    {
        "name":"終焉の観測者","type": "mob", "floor_range": (101, 119),
        "hp": 470, "max_hp": 470, "speed": 10, "attack": 60,
        "image": "image/st6en5.png",
        "skills":[
            {"name": "終焉の刃", "type": "攻撃", "power": 270, "element": "none"},
            {"name": "終焉の防御", "type": "防御", "power": 100, "element": "none"}
        ]
    },
    {
        "name":"時空の観測者","type": "boss", "floor": 120,
        "hp": 500, "max_hp": 500, "speed": 10, "attack": 60,
        "image": "image/st6en6.png",
        "skills":[
            {"name": "時空の刃", "type": "攻撃", "power": 300, "element": "none"},
            {"name": "ディメンションシフト", "type": "防御", "power": 90, "element": "none"},
            {"name":"観測者の宣告", "type":"攻撃", "power":500, "element":"none"},
            {"name": "一斉掃射", "type": "攻撃", "power": 200, "element": "thunder"},
            {"name": "絶対零度", "type": "継続", "power": 100, "element": "ice"},
            {"name": "マグマドロップ", "type": "継続", "power": 100, "element": "fire"},
            {"name": "暗黒の呪い", "type": "継続", "power": 100, "element": "shadow"},
            {"name": "再結合", "type": "回復", "power": 60, "element": "none"}
        ]
    }
]

def init_game(char_name):
    st.session_state.floor = 1  # 階層の初期値を1に設定
    stats = CHARACTERS[char_name]
    st.session_state.hp = stats["hp"]
    st.session_state.max_hp = stats["max_hp"]
    
    # ベース値を保存
    st.session_state.base_attack = stats["attack"]
    st.session_state.base_speed = stats["speed"]
    # 現在の値をベース値に初期化
    st.session_state.attack = stats["attack"]
    st.session_state.speed = stats["speed"]
    st.session_state.defense = stats["defense"]
    st.session_state.level = 1
    st.session_state.exp = 0
    st.session_state.exp_to_next = 100  # 次のレベルに必要な経験値
    st.session_state.money = 0
    st.session_state.char_name = char_name
    st.session_state.skills = [stats["initial_skill"]]
    st.session_state.image_path = stats["image_path"]
    st.session_state.element = stats["element"]
    st.session_state.log = [f"{char_name}で冒険を開始した！"]
    st.session_state.game_started = True
    st.session_state.battle_mode = False
    st.session_state.enemy_defense=0
    # バフ情報の管理リストを追加
    st.session_state.active_buffs = []
    for s in st.session_state.skills:
        s['current_turn'] = 0
def get_enemy_by_floor(floor):
    # 階層がボス階層ならボスを返す
    bosses = {
        20: "大王スライム", 
        40: "暗黒地殻獣", 
        60: "灼熱の焔龍", 
        80: "氷華の魔女", 
        100: "量産型AI軍団", 
        120: "時空の観測者"
    }
    
    if floor in bosses:
        return next(e for e in ENEMIES if e["name"] == bosses[floor])
    
    # 通常階層なら範囲内のmobからランダム
    candidates = [e for e in ENEMIES if e["type"] == "mob" and e["floor_range"][0] <= floor <= e["floor_range"][1]]
    return random.choice(candidates)        
# --- メインロジック ---
if 'game_started' not in st.session_state:
    st.title("キャラクター選択")
    cols = st.columns(3)
    for i, (name, stats) in enumerate(CHARACTERS.items()):
        with cols[i]:
            st.image(stats["image_path"], width='stretch')
            st.subheader(name)
            st.write(f"HP: {stats['hp']}")
            
            if st.button(f"{name}を選択"):
                init_game(name)
                st.rerun()
else:
    # --- 戦闘ロジック ---
    if st.session_state.battle_mode:
        st.title("戦闘中！")
        c1, c2 = st.columns(2)
        # プレイヤー表示
        with c1:
            st.image(st.session_state.image_path, width=350)
            st.write(f"**{st.session_state.char_name}**")
            st.progress(st.session_state.hp / st.session_state.max_hp)
            st.write(f"HP: {st.session_state.hp}/{st.session_state.max_hp}")
            
        # 敵表示
        with c2:
            enemy = st.session_state.enemy
            st.image(enemy['image'], width=350)
            st.write(f"**{enemy['name']}**")
            st.progress(enemy['hp'] / enemy['max_hp'])
            st.write(f"HP: {enemy['hp']}/{enemy['max_hp']}")

        # スキル選択
        st.subheader("スキルを選択")
        cols = st.columns(len(st.session_state.skills))
        for i, skill in enumerate(st.session_state.skills):
            with cols[i]:
                st.image(skill['image'], width=250)
            # クールダウン中ならボタンを無効化
            is_disabled = skill['current_turn'] > 0
            # --- ターン開始時の継続ダメージ処理 ---
            if st.session_state.get('poison_turns', 0) > 0:
                
                st.session_state.hp -= st.session_state.poison_damage
                st.session_state.poison_turns -= 1
                st.session_state.log.append(f"継続ダメージ！{st.session_state.poison_damage} 受けた。(残り{st.session_state.poison_turns}ターン)")
                
                # HPが0になったら即座に判定
                if st.session_state.hp <= 0:
                    st.session_state.log.append("継続ダメージで力尽きた...")
                    st.session_state.battle_mode = False
                    st.rerun()
            if cols[i].button(f"{skill['type']}{skill['power']}:{skill['name']}" if not is_disabled else f"{skill['name']} ({skill['current_turn']})", disabled=is_disabled):
                # --- 速度判定による先攻・後攻の処理 ---
                # 敵の攻撃ターン (敵のスピードがプレイヤーより高い場合、先に反撃を受ける)
                if st.session_state.speed < st.session_state.enemy.get('speed', 0):
                    enemy_skill = random.choice(st.session_state.enemy['skills'])
                    st.session_state.log.append(f"敵は「{enemy_skill['name']}」を使った！")

                    if enemy_skill['type'] == "攻撃":
                        enemy_dmg = enemy_skill['power']-st.session_state.defense
                        st.session_state.hp -= enemy_dmg
                        st.session_state.log.append(f"{enemy_dmg} ダメージを受けた。")
                    elif enemy_skill['type'] == "回復":
                        # 敵自身のHPを回復
                        heal_amount = enemy_skill['power']
                        st.session_state.enemy['hp'] = min(st.session_state.enemy['max_hp'], st.session_state.enemy['hp'] + heal_amount)
                        st.session_state.log.append(f"敵の体力が {heal_amount} 回復した。")

                    elif enemy_skill['type'] == "防御":
                        # 敵の防御力を一時的に上げるなどの処理（例：一時的なダメージ無効化フラグなど）
                        st.session_state.enemy_defense += enemy_skill['power']
                        st.session_state.log.append(f"敵は身構えて{st.session_state.enemy_defense}防御を固めた！")

                    elif enemy_skill['type'] == "継続":
                        # 継続ダメージ（毒など）をプレイヤーに付与する処理
                        st.session_state.poison_damage = enemy_skill['power']
                        st.session_state.poison_turn = 3 # 3ターンの間
                        st.session_state.log.append(f"継続ダメージを受けた！毎ターン {enemy_skill['power']} のダメージ！")                # プレイヤーの選択スキルのクールダウンを1減らす
                # 戦闘処理（簡易版）
                if skill['type']=="攻撃":
                    damage = skill['power']
                    st.session_state.enemy['hp'] -= damage-st.session_state.enemy_defense
                    st.session_state.log.append(f"{skill['name']}で {damage} ダメージを与えた！")
                elif skill['type']=="回復":
                    heal = skill['power']
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + heal)
                    st.session_state.log.append(f"{skill['name']}で {heal} HPを回復した！")
                elif skill['type']=="防御":
                    st.session_state.defense += skill['power']
                    st.session_state.log.append(f"{skill['name']}で防御力が {skill['power']} 上がった！")
                elif skill['type']=="強化":
                    # バフを適用
                    st.session_state.attack += skill['power']
                    st.session_state.speed += skill['power']/10
                    # スキルと終了ターン(残りターン)を管理リストに追加
                    st.session_state.active_buffs.append({
                        "power": skill['power'],
                        "remaining_turn": skill['turn'] 
                    })
                    st.session_state.log.append(f"{skill['name']}で攻撃力が {skill['power']} 上がった！")
                # スキルのクールダウンを設定
                skill['current_turn'] = skill['turn']-1
                # --- 敵の反撃処理 ---
                if st.session_state.enemy['hp'] > 0:
                    enemy_skill = random.choice(st.session_state.enemy['skills'])
                    st.session_state.log.append(f"敵は「{enemy_skill['name']}」を使った！")

                    if enemy_skill['type'] == "攻撃":
                        enemy_dmg = enemy_skill['power']-st.session_state.defense
                        st.session_state.hp -= enemy_dmg
                        st.session_state.log.append(f"{enemy_dmg} ダメージを受けた。")
                    elif enemy_skill['type'] == "回復":
                        # 敵自身のHPを回復
                        heal_amount = enemy_skill['power']
                        st.session_state.enemy['hp'] = min(st.session_state.enemy['max_hp'], st.session_state.enemy['hp'] + heal_amount)
                        st.session_state.log.append(f"敵の体力が {heal_amount} 回復した。")

                    elif enemy_skill['type'] == "防御":
                        # 敵の防御力を一時的に上げるなどの処理（例：一時的なダメージ無効化フラグなど）
                        st.session_state.enemy_defense += enemy_skill['power']
                        st.session_state.log.append(f"敵は身構えて{st.session_state.enemy_defense}防御を固めた！")

                    elif enemy_skill['type'] == "継続":
                        enemy_dmg = enemy_skill['power']-st.session_state.defense
                        st.session_state.hp -= enemy_dmg
                        # 継続ダメージ（毒など）をプレイヤーに付与する処理
                        st.session_state.poison_damage = enemy_skill['power']
                        st.session_state.poison_turn = 3 # 3ターンの間
                        st.session_state.log.append(f"継続ダメージを受けた！毎ターン {enemy_skill['power']} のダメージ！")                # プレイヤーの選択スキルのクールダウンを1減らす
                    
                if st.session_state.skills[i]['current_turn'] > 0:
                    st.session_state.skills[i]['current_turn'] -= 1
                new_buffs = []
                for buff in st.session_state.active_buffs:
                    buff["remaining_turn"] -= 1
                    if buff["remaining_turn"] <= 0:
                        # ステータスを元に戻す
                        st.session_state.attack -= buff["power"]
                        st.session_state.speed -= buff["power"] / 10
                        st.session_state.log.append("強化効果が切れた！")
                    else:
                        new_buffs.append(buff)
                st.session_state.active_buffs = new_buffs
                # 勝敗判定部分に追加
                if st.session_state.enemy['hp'] <= 0 or st.session_state.hp <= 0:
                    # 全てのバフを強制解除して元に戻す
                    for buff in st.session_state.active_buffs:
                        st.session_state.attack -= buff["power"]
                        st.session_state.speed -= buff["power"] / 10
                    st.session_state.active_buffs = []
                    
                    if st.session_state.enemy['hp'] <= 0:
                        st.session_state.log.append("勝利した！")
                        # --- 経験値獲得とレベルアップ判定 ---
                        gained_exp = 50  # 敵ごとに設定しても良い
                        st.session_state.exp += gained_exp
                        st.session_state.log.append(f"{gained_exp} の経験値を獲得した！")
                        
                        if st.session_state.exp >= st.session_state.exp_to_next:
                            st.session_state.level += 1
                            st.session_state.exp -= st.session_state.exp_to_next
                            st.session_state.exp_to_next = int(st.session_state.exp_to_next * 1.5) # 次のレベルは少し大変に
                            
                            # ステータス強化
                            st.session_state.max_hp += 20
                            st.session_state.hp = st.session_state.max_hp
                            st.session_state.attack += 10
                            for st.session_state.skill in st.session_state.skills:
                                st.session_state.skill['power'] += 10
                            st.session_state.log.append(f"レベルアップ！Lv.{st.session_state.level}になった！")
                    else:
                        st.session_state.log.append("敗北した...")
                    st.session_state.battle_mode = False
                st.rerun()
        
        st.write("---")
        for msg in reversed(st.session_state.log):
            st.write(f"- {msg}")
                
    elif st.session_state.get('swapping_mode', False):
        st.warning(f"スキルスロットがいっぱいです！新規スキル「{st.session_state.new_skill_candidate['type']}{st.session_state.new_skill_candidate['power']}:{st.session_state.new_skill_candidate['name']}」をどうしますか？")

        col_swap, col_discard = st.columns(2)
        
        # 既存スキルと入れ替えるボタン
        st.write("入れ替えるスキルを選択してください:")
        for i, s in enumerate(st.session_state.skills):
            if st.button(f"{s['type']}{s['power']}:{s['name']} と入れ替える"):
                st.session_state.skills[i] = st.session_state.new_skill_candidate
                st.session_state.skills[i]['current_turn'] = 0
                st.session_state.log.append(f"スキル「{s['type']}{s['power']}:{s['name']}」を捨て、スキル「{st.session_state.new_skill_candidate['type']}{st.session_state.new_skill_candidate['power']}:{st.session_state.new_skill_candidate['name']}」を習得した。")
                st.session_state.swapping_mode = False
                del st.session_state.new_skill_candidate
                st.rerun()
                
        # 新規スキルを捨てるボタン
        if st.button("やっぱり捨てる"):
            st.session_state.log.append(f"新規スキル「{st.session_state.new_skill_candidate['type']}{st.session_state.new_skill_candidate['power']}:{st.session_state.new_skill_candidate['name']}」を破棄した。")
            st.session_state.swapping_mode = False
            del st.session_state.new_skill_candidate
            st.rerun()
        
        st.stop() # 入れ替えモード中は以下のイベント選択を表示しない 
    else:
        # --- 通常画面 ---
        st.title(f"冒険者: {st.session_state.char_name}")
        st.subheader(f"現在階層: {st.session_state.floor} F")
        with st.sidebar:
            st.image(st.session_state.image_path, width='stretch')
            st.header("ステータス")
            st.write(f"HP: {st.session_state.hp}/{st.session_state.max_hp}")
            st.write(f"Lv: {st.session_state.level}") # 追加
            st.write(f"EXP: {st.session_state.exp} / {st.session_state.exp_to_next}") # 追加
            st.write(f"攻撃力: {st.session_state.attack}")
            st.subheader("所持スキル")
            for s in st.session_state.skills:
                st.write(f"- {s['name']} ({s['type']}{s['power']})")
            if st.button("リセット"):
                del st.session_state.game_started
                st.rerun()

        # 戦闘イベント時を想定した画像表示例
        # if st.session_state.current_event == "戦闘": ... とすることで条件分岐可能
        
        st.subheader("次に行う行動を選択")
        events = ["戦闘", "回復", "武器獲得", "防具獲得", "ショップ", "スキル獲得", "ステータス強化"]
        if 'current_events' not in st.session_state:
            st.session_state.current_events = random.sample(events, 3)
        

        cols = st.columns(len(st.session_state.current_events))
        for i, event in enumerate(st.session_state.current_events):
            if cols[i].button(event):
                st.session_state.floor += 1
                # 戦闘イベントの例
                if event == "戦闘":
                    st.session_state.log.append(f"戦闘開始！")
                    target_floor = st.session_state.floor
                    st.session_state.enemy = get_enemy_by_floor(target_floor).copy()
                    st.session_state.battle_mode = True
                    st.session_state.poison_turns = 0
                    st.session_state.poison_damage=0
                    for s in st.session_state.skills:
                        s['current_turn'] = 0
                    
                    
                    
                elif event == "回復":
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 20)
                    st.session_state.log.append("HPを回復した。")
                    
                elif event == "スキル獲得":
                    if len(st.session_state.skills) < 5:
                        # 所持しているスキル名のリストを作成
                        owned_skill_names = [s['name'] for s in st.session_state.skills]
                        
                        # キャラクターに応じたプールから、所持していないものだけを抽出
                        if st.session_state.char_name == "水龍の巫女":
                            pool = WATER_SKILL_POOL
                        elif st.session_state.char_name == "風の魔女":
                            pool = WIND_SKILL_POOL
                        else:
                            pool = SHADOW_SKILL_POOL
                            
                        available_skills = [s for s in pool if s['name'] not in owned_skill_names]
                        
                        if available_skills:
                            new_skill = random.choice(available_skills).copy()
                            new_skill['current_turn'] = 0 # 初期値
                            st.session_state.skills.append(new_skill)
                            st.session_state.log.append(f"スキル「{new_skill['type']}{new_skill['power']}:{new_skill['name']}」を獲得した！")
                        
                    else:
                        # 所持しているスキル名のリストを作成
                        owned_skill_names = [s['name'] for s in st.session_state.skills]
                        
                        # キャラクターに応じたプールから、所持していないものだけを抽出
                        if st.session_state.char_name == "水龍の巫女":
                            pool = WATER_SKILL_POOL
                        elif st.session_state.char_name == "風の魔女":
                            pool = WIND_SKILL_POOL
                        else:
                            pool = SHADOW_SKILL_POOL
                            
                        available_skills = [s for s in pool if s['name'] not in owned_skill_names]
                        
                        if available_skills:
                            new_skill = random.choice(available_skills).copy()
                            st.session_state.new_skill_candidate = new_skill

                        st.session_state.swapping_mode = True
                        
                        
                    
                else:
                    st.session_state.log.append(f"{event}を実行した。")
                    
                # 階層が20の倍数（ボス階層）の場合は「戦闘」のみにする
                if st.session_state.floor % 20 == 19:
                    st.session_state.current_events = ["戦闘"]
                    st.session_state.log.append("エリアボスが出現！")
                else:
                    # 通常階層ならランダムに3つ
                    
                    
                    st.session_state.current_events = random.sample(events, 3)
                
                
                st.rerun()

        st.write("---")
        for msg in reversed(st.session_state.log):
            st.write(f"- {msg}")