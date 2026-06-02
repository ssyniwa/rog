import streamlit as st
import random

# --- データ定義 ---
CHARACTERS = {
    "水龍の巫女": {
        "hp": 120, "max_hp": 120, "mp": 20, "max_mp": 20, "speed": 10,
        "attack": 15, "defense": 10, "element": "water", "image_path": "image/water.png",
        "initial_skill": {"name": "翠明流流転斬り", "type": "攻撃", "power": 30, "turn": 1, "image": "image/water_skill1.png", "element": "water"}
    },
    "風の魔女": {
        "hp": 80, "max_hp": 80, "mp": 60, "max_mp": 60, "speed": 12,
        "attack": 25, "defense": 5, "element": "wind", "image_path": "image/wind.png",
        "initial_skill": {"name": "ウィンドカッター", "type": "攻撃", "power": 25, "turn": 1, "image": "image/wind_skill1.png", "element": "wind"}
    },
    "月夜の暗殺者": {
        "hp": 100, "max_hp": 100, "mp": 30, "max_mp": 30, "speed": 14,
        "attack": 12, "defense": 8, "element": "shadow", "image_path": "image/shadow.png",
        "initial_skill": {"name": "シャドーナイフ", "type": "攻撃", "power": 20, "turn": 1, "image": "image/shadow_skill1.png", "element": "shadow"}
    },
}

# 獲得可能なランダムスキルのプール
SKILL_POOL = [
    {"name": "大回復", "type": "回復", "power": 40, "turn": 3, "image": "image/heal.png", "element": "neutral"},
    {"name": "防御無視の一撃", "type": "攻撃", "power": 50, "turn": 4, "image": "image/pierce.png", "element": "neutral"}
]
ENEMIES = [
    {"name": "ゴブリン", "hp": 50, "max_hp": 50, "mp": 10, "max_mp": 10, "speed": 8, "attack": 10, "image": "https://placehold.co/100x100/red/white?text=Enemy1"},
    {"name": "スライム", "hp": 30, "max_hp": 30, "mp": 0, "max_mp": 0, "speed": 5, "attack": 5, "image": "https://placehold.co/100x100/green/white?text=Enemy2"},
]
def init_game(char_name):
    stats = CHARACTERS[char_name]
    st.session_state.hp = stats["hp"]
    st.session_state.max_hp = stats["max_hp"]
    st.session_state.mp = stats["mp"]
    st.session_state.max_mp = stats["max_mp"]
    st.session_state.attack = stats["attack"]
    st.session_state.defense = stats["defense"]
    st.session_state.speed = stats["speed"]
    st.session_state.money = 0
    st.session_state.char_name = char_name
    st.session_state.skills = [stats["initial_skill"]]
    st.session_state.image_path = stats["image_path"]
    st.session_state.element = stats["element"]
    st.session_state.log = [f"{char_name}で冒険を開始した！"]
    st.session_state.game_started = True
    st.session_state.game_mode = "MAIN" # MAIN, BATTLE
# --- メインロジック ---
if 'game_started' not in st.session_state:
    st.title("キャラクター選択")
    cols = st.columns(3)
    for i, (name, stats) in enumerate(CHARACTERS.items()):
        with cols[i]:
            st.image(stats["image_path"], use_container_width=True)
            st.subheader(name)
            st.write(f"HP: {stats['hp']} / MP: {stats['mp']}")
            
            if st.button(f"{name}を選択"):
                init_game(name)
                st.rerun()
elif st.session_state.game_mode == "BATTLE":
    st.title("戦闘中！")
    enemy = st.session_state.current_enemy

    # 上部ステータス表示
    c1, c2 = st.columns(2)
    with c1:
        st.image(st.session_state.image_path, width=100)
        st.write(f"**プレイヤー** (SPD:{st.session_state.speed})")
        st.progress(st.session_state.hp / st.session_state.max_hp, text="HP")
        st.progress(st.session_state.mp / st.session_state.max_mp, text="MP")
    with c2:
        st.image(enemy["image"], width=100)
        st.write(f"**{enemy['name']}** (SPD:{enemy['speed']})")
        st.progress(enemy["hp"] / enemy["max_hp"], text="HP")

        st.write("---")
        # スキル選択ボタン
        st.subheader("スキルを選択")
        for skill in st.session_state.skills:
            if st.button(f"発動: {skill['name']} (威力:{skill['power']})"):
                # 簡易ダメージ処理
                dmg = skill['power']
                enemy['hp'] -= dmg
                st.session_state.log.append(f"{skill['name']}で{dmg}のダメージ！")

                if enemy['hp'] <= 0:
                    st.session_state.log.append("敵を倒した！")
                    st.session_state.game_mode = "MAIN"
                st.rerun()
else:
    # --- ゲーム本編 ---
    st.title(f"冒険者: {st.session_state.char_name}")
    
    with st.sidebar:
        st.image(st.session_state.image_path, use_container_width=True)
        st.header("ステータス")
        st.write(f"HP: {st.session_state.hp}/{st.session_state.max_hp}")
        st.write(f"MP: {st.session_state.mp}/{st.session_state.max_mp}")
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
                if st.button("戦闘を開始する"):
                    st.session_state.current_enemy = random.choice(ENEMIES).copy()
                    st.session_state.game_mode = "BATTLE"
                    st.rerun()
            elif event == "回復":
                st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 20)
                st.session_state.log.append("HPを回復した。")
            elif event == "スキル獲得":
                if len(st.session_state.skills) < 5:
                    new_skill = random.choice(SKILL_POOL)
                    st.session_state.skills.append(new_skill)
                    st.session_state.log.append(f"スキル「{new_skill['name']}」を獲得した！")
                else:
                    st.session_state.log.append("スキルスロットがいっぱいだ！")
            else:
                st.session_state.log.append(f"{event}を実行した。")
            
            st.session_state.current_events = random.sample(events, 3)
            st.rerun()

    st.write("---")
    for msg in reversed(st.session_state.log):
        st.write(f"- {msg}")