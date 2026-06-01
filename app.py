import streamlit as st
import random

# --- キャラクターデータ定義 ---
CHARACTERS = {
    "戦士": {"hp": 120, "max_hp": 120, "attack": 15, "defense": 10, "skill": "大ダメージ"},
    "魔法使い": {"hp": 80, "max_hp": 80, "attack": 25, "defense": 5, "skill": "防御無視"},
    "盗賊": {"hp": 100, "max_hp": 100, "attack": 12, "defense": 8, "skill": "攻撃力UP"},
}

def init_game(char_name):
    stats = CHARACTERS[char_name]
    st.session_state.hp = stats["hp"]
    st.session_state.max_hp = stats["max_hp"]
    st.session_state.attack = stats["attack"]
    st.session_state.defense = stats["defense"]
    st.session_state.money = 0
    st.session_state.level = 1
    st.session_state.char_name = char_name
    st.session_state.skills = [stats["skill"]]
    st.session_state.log = [f"{char_name}で冒険を開始した！"]
    st.session_state.game_started = True

# --- イベント処理 ---
def trigger_event(event_name):
    if event_name == "戦闘":
        # ここに戦闘ロジック（後ほど実装）
        st.session_state.log.append("敵が現れた！(戦闘ロジックを実装してください)")
    elif event_name == "回復":
        heal_amount = int(st.session_state.max_hp * 0.3)
        st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + heal_amount)
        st.session_state.log.append(f"HPを{heal_amount}回復した！")
    # 他のイベントの条件分岐をここに追加...
    else:
        st.session_state.log.append(f"{event_name}はまだ工事中です。")

# --- メイン画面 ---
if 'game_started' not in st.session_state:
    st.title("キャラクター選択")
    col1, col2, col3 = st.columns(3)
    
    # 各キャラクターのボタン
    for i, (name, stats) in enumerate(CHARACTERS.items()):
        with [col1, col2, col3][i]:
            st.subheader(name)
            st.write(f"HP: {stats['hp']}")
            st.write(f"攻撃: {stats['attack']}")
            st.write(f"初期スキル: {stats['skill']}")
            if st.button(f"{name}を選択"):
                init_game(name)
                st.rerun()
else:
    # --- ゲーム本編 ---
    st.title(f"冒険者: {st.session_state.char_name}")
    # 以下、前回作成したゲームループへ続く...

    if 'hp' not in st.session_state:
        init_game()

    # サイドバーにステータス表示
    with st.sidebar:
        st.header("ステータス")
        st.write(f"HP: {st.session_state.hp}/{st.session_state.max_hp}")
        st.write(f"資金: {st.session_state.money}")
        st.write(f"攻撃力: {st.session_state.attack}")
        if st.button("リセット"):
            init_game()
            st.rerun()

    # メインイベント表示
    st.subheader("次に行う行動を選択してください")
    events = ["戦闘", "回復", "武器獲得", "防具獲得", "ショップ", "スキル獲得", "ステータス強化"]
    selected_events = random.sample(events, 3)

    cols = st.columns(3)
    for i, event in enumerate(selected_events):
        if cols[i].button(event):
            trigger_event(event)
            st.rerun()

    # ログ表示
    st.write("---")
    st.write("### 冒険の記録")
    for msg in reversed(st.session_state.log):
        st.write(f"- {msg}")