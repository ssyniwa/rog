import streamlit as st
import random

# --- データ定義 ---
CHARACTERS = {
    "水龍の巫女": {
        "hp": 120, "max_hp": 120,  "speed": 10,
        "attack": 15, "defense": 10, "element": "water", "image_path": "image/water.png",
        "initial_skill": {"name": "翠明流流転斬り", "type": "攻撃", "power": 30, "turn": 1, "image": "image/water_skill1.png", "element": "water"}
    },
    "風の魔女": {
        "hp": 80, "max_hp": 80,  "speed": 12,
        "attack": 25, "defense": 5, "element": "wind", "image_path": "image/wind.png",
        "initial_skill": {"name": "ウィンドカッター", "type": "攻撃", "power": 25, "turn": 1, "image": "image/wind_skill1.png", "element": "wind"}
    },
    "月夜の暗殺者": {
        "hp": 100, "max_hp": 100, "speed": 14,
        "attack": 12, "defense": 8, "element": "shadow", "image_path": "image/shadow.png",
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
]
# --- 敵データの定義（スキル付き） ---
ENEMIES = [
    {
        "name": "ゴブリン", 
        "hp": 50, "max_hp": 50, "speed": 8, "attack": 10, 
        "image": "image/goblin.png",
        "skills": [
            {"name": "なぐる", "type": "攻撃", "power": 10, "element": "neutral"},
            {"name": "ひっかき", "type": "攻撃", "power": 15,  "element": "neutral"}
        ]
    },
    {
        "name": "スライム", 
        "hp": 30, "max_hp": 30, "speed": 5, "attack": 5, 
        "image": "image/slime.png",
        "skills": [
            {"name": "体当たり", "type": "攻撃", "power": 8,  "element": "neutral"},
            {"name": "どろかけ", "type": "攻撃", "power": 5, "element": "earth"}
        ]
    },
]
def init_game(char_name):
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
    
    st.session_state.money = 0
    st.session_state.char_name = char_name
    st.session_state.skills = [stats["initial_skill"]]
    st.session_state.image_path = stats["image_path"]
    st.session_state.element = stats["element"]
    st.session_state.log = [f"{char_name}で冒険を開始した！"]
    st.session_state.game_started = True
    st.session_state.battle_mode = False
    # バフ情報の管理リストを追加
    st.session_state.active_buffs = []
    for s in st.session_state.skills:
        s['current_turn'] = 0
# --- メインロジック ---
if 'game_started' not in st.session_state:
    st.title("キャラクター選択")
    cols = st.columns(3)
    for i, (name, stats) in enumerate(CHARACTERS.items()):
        with cols[i]:
            st.image(stats["image_path"], use_container_width=True)
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
            if cols[i].button(skill['name'] if not is_disabled else f"{skill['name']} ({skill['current_turn']})", disabled=is_disabled):
                # 戦闘処理（簡易版）
                if skill['type']=="攻撃":
                    damage = skill['power']
                    st.session_state.enemy['hp'] -= damage
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
                skill['current_turn'] = skill['turn']
                # --- 敵の反撃処理 ---
                if st.session_state.enemy['hp'] > 0:
                    enemy_skill = random.choice(st.session_state.enemy['skills'])
                    enemy_dmg = enemy_skill['power']-st.session_state.defense
                    st.session_state.hp -= enemy_dmg
                    st.session_state.log.append(f"{st.session_state.enemy['name']}の「{enemy_skill['name']}」！{enemy_dmg} ダメージを受けた。")
                    
                # プレイヤーの選択スキルのクールダウンを1減らす
                    
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
                    else:
                        st.session_state.log.append("敗北した...")
                    st.session_state.battle_mode = False
                st.write("---")
                for msg in reversed(st.session_state.log):
                    st.write(f"- {msg}")
                st.rerun()
    elif st.session_state.get('swapping_mode', False):
        st.warning(f"スキルスロットがいっぱいです！新規スキル「{st.session_state.new_skill_candidate['name']}」をどうしますか？")
        
        col_swap, col_discard = st.columns(2)
        
        # 既存スキルと入れ替えるボタン
        st.write("入れ替えるスキルを選択してください:")
        for i, s in enumerate(st.session_state.skills):
            if st.button(f"{s['name']} と入れ替える"):
                st.session_state.skills[i] = st.session_state.new_skill_candidate
                st.session_state.skills[i]['current_turn'] = 0
                st.session_state.log.append(f"{s['name']} を捨て、{st.session_state.new_skill_candidate['name']} を習得した。")
                st.session_state.swapping_mode = False
                del st.session_state.new_skill_candidate
                st.rerun()
                
        # 新規スキルを捨てるボタン
        if st.button("やっぱり捨てる"):
            st.session_state.log.append(f"新規スキル「{st.session_state.new_skill_candidate['name']}」を破棄した。")
            st.session_state.swapping_mode = False
            del st.session_state.new_skill_candidate
            st.rerun()
        
        st.stop() # 入れ替えモード中は以下のイベント選択を表示しない 
    else:
        # --- 通常画面 ---
        st.title(f"冒険者: {st.session_state.char_name}")
        
        with st.sidebar:
            st.image(st.session_state.image_path, use_container_width=True)
            st.header("ステータス")
            st.write(f"HP: {st.session_state.hp}/{st.session_state.max_hp}")
            
            st.write(f"攻撃力: {st.session_state.attack}")
            st.subheader("所持スキル")
            for s in st.session_state.skills:
                st.write(f"- {s['name']} ({s['type']})")
            if st.button("リセット"):
                del st.session_state.game_started
                st.rerun()

        # 戦闘イベント時を想定した画像表示例
        # if st.session_state.current_event == "戦闘": ... とすることで条件分岐可能
        
        st.subheader("次に行う行動を選択")
        events = ["戦闘", "回復", "武器獲得", "防具獲得", "ショップ", "スキル獲得", "ステータス強化"]
        
        if 'current_events' not in st.session_state:
            st.session_state.current_events = random.sample(events, 3)

        cols = st.columns(3)
        for i, event in enumerate(st.session_state.current_events):
            if cols[i].button(event):
                # 戦闘イベントの例
                if event == "戦闘":
                    st.session_state.log.append(f"戦闘開始！")
                    st.session_state.enemy = random.choice(ENEMIES).copy()
                    st.session_state.battle_mode = True
                    for s in st.session_state.skills:
                        s['current_turn'] = 0
                    st.rerun()
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
                            st.session_state.log.append(f"スキル「{new_skill['name']}」を獲得した！")
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
                        st.rerun()
                else:
                    st.session_state.log.append(f"{event}を実行した。")
                
                st.session_state.current_events = random.sample(events, 3)
                st.rerun()

        st.write("---")
        for msg in reversed(st.session_state.log):
            st.write(f"- {msg}")