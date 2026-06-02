import streamlit as st
import random

# --- キャラクターデータ定義 ---
# image_pathには、プロジェクト内の画像ファイルへのパスや、Web上のURLを指定してください
CHARACTERS = {
    "水龍の巫女": {
        "hp": 120, "max_hp": 120, "mp": 20, "max_mp": 20, 
        "attack": 15, "defense": 10, "skill_name": "翠明流流転斬り", "skill_type": "攻撃",
        "image_path":"image/water.png"
    },
    "風の魔女": {
        "hp": 80, "max_hp": 80, "mp": 60, "max_mp": 60, 
        "attack": 25, "defense": 5, "skill_name": "ウィンドカッター", "skill_type": "攻撃",
        "image_path": "image/wind.png"
    },
    "月夜の暗殺者": {
        "hp": 100, "max_hp": 100, "mp": 30, "max_mp": 30, 
        "attack": 12, "defense": 8, "skill_name": "シャドーナイフ", "skill_type": "攻撃",
        "image_path": "image/shadow.png"
    },
}

def init_game(char_name):
    stats = CHARACTERS[char_name]
    st.session_state.hp = stats["hp"]
    st.session_state.max_hp = stats["max_hp"]
    st.session_state.mp = stats["mp"]
    st.session_state.max_mp = stats["max_mp"]
    st.session_state.attack = stats["attack"]
    st.session_state.defense = stats["defense"]
    st.session_state.money = 0
    st.session_state.char_name = char_name
    st.session_state.skill_name = stats["skill_name"]
    st.session_state.skill_type = stats["skill_type"]
    st.session_state.image_path = stats["image_path"]
    st.session_state.log = [f"{char_name}で冒険を開始した！"]
    st.session_state.game_started = True

# --- メインロジック ---
if 'game_started' not in st.session_state:
    st.title("キャラクター選択")
    cols = st.columns(3)
    for i, (name, stats) in enumerate(CHARACTERS.items()):
        with cols[i]:
            st.image(stats["image_path"], use_container_width=True)
            st.subheader(name)
            st.write(f"HP: {stats['hp']} / MP: {stats['mp']}")
            st.write(f"スキル: {stats['skill_name']} ({stats['skill_type']})")
            if st.button(f"{name}を選択"):
                init_game(name)
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
                st.session_state.log.append(f"戦闘開始！{st.session_state.skill_name}で攻撃！")
            elif event == "回復":
                st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 20)
                st.session_state.log.append("HPを回復した。")
            else:
                st.session_state.log.append(f"{event}を実行した。")
            
            st.session_state.current_events = random.sample(events, 3)
            st.rerun()

    st.write("---")
    for msg in reversed(st.session_state.log):
        st.write(f"- {msg}")