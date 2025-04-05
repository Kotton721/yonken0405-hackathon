# kano_q.py
import random
from kano_weighted_summary import get_weighted_muscle_scores

# --- minor_muscles の定義 ---
minor_muscles = [
    {"name": "大胸筋上部", "major_muscle_id": "chest_id"},
    {"name": "大胸筋下部", "major_muscle_id": "chest_id"},
    {"name": "広背筋", "major_muscle_id": "back_id"},
    {"name": "僧帽筋", "major_muscle_id": "back_id"},
    {"name": "三角筋前部", "major_muscle_id": "shoulder_id"},
    {"name": "三角筋側部", "major_muscle_id": "shoulder_id"},
    {"name": "上腕二頭筋", "major_muscle_id": "arm_id"},
    {"name": "上腕三頭筋", "major_muscle_id": "arm_id"},
    {"name": "大腿四頭筋", "major_muscle_id": "leg_id"},
    {"name": "ハムストリング", "major_muscle_id": "leg_id"},
]

# --- トレーニングスコア辞書（必要であれば training_scores_data.py に分けてもOK） ---
training_scores_data = {
    "チェストプレス": {"大胸筋上部": 35, "大胸筋下部": 30, "三角筋前部": 15, "上腕三頭筋": 20},
    "ペクトラルフライ": {"大胸筋上部": 45, "大胸筋下部": 45, "三角筋前部": 10},
    "ベンチプレス": {"大胸筋上部": 30, "大胸筋下部": 30, "三角筋前部": 15, "上腕三頭筋": 25},
    "インクラインベンチプレス": {"大胸筋上部": 50, "大胸筋下部": 20, "三角筋前部": 15, "上腕三頭筋": 15},
    "ダンベルフライ": {"大胸筋上部": 45, "大胸筋下部": 45, "三角筋前部": 10},
    "腕立て伏せ（プッシュアップ）": {"大胸筋上部": 35, "大胸筋下部": 35, "三角筋前部": 15, "上腕三頭筋": 15},
    "ディップス": {"大胸筋下部": 50, "上腕三頭筋": 40, "大胸筋上部": 10},
    "ラットプルダウン": {"広背筋": 60, "僧帽筋": 20, "上腕二頭筋": 20},
    "シーテッドローイング": {"広背筋": 50, "僧帽筋": 30, "上腕二頭筋": 20},
    "デッドリフト": {"広背筋": 30, "僧帽筋": 20, "ハムストリング": 30, "大腿四頭筋": 20},
    "ワンハンドダンベルローイング": {"広背筋": 60, "僧帽筋": 20, "上腕二頭筋": 20},
    "懸垂（プルアップ）": {"広背筋": 60, "上腕二頭筋": 30, "僧帽筋": 10},
    "逆手懸垂（アンダーグリップ・チンアップ）": {"広背筋": 50, "上腕二頭筋": 40, "僧帽筋": 10},
    "ショルダープレス": {"三角筋前部": 50, "三角筋側部": 30, "上腕三頭筋": 20},
    "ショルダープレスマシン": {"三角筋前部": 50, "三角筋側部": 30, "上腕三頭筋": 20},
    "サイドレイズ": {"三角筋側部": 80, "三角筋前部": 20},
    "パイクプッシュアップ": {"三角筋前部": 60, "上腕三頭筋": 30, "三角筋側部": 10},
    "トライセプスプレスダウン": {"上腕三頭筋": 100},
    "バイセップスカール": {"上腕二頭筋": 100},
    "バーベルカール": {"上腕二頭筋": 100},
    "ダンベルカール": {"上腕二頭筋": 100},
    "ハンマーカール": {"上腕二頭筋": 100},
    "フレンチプレス": {"上腕三頭筋": 100},
    "スカルクラッシャー（ライイングトライセプスエクステンション）": {"上腕三頭筋": 100},
    "レッグプレス": {"大腿四頭筋": 60, "ハムストリング": 40},
    "レッグエクステンション": {"大腿四頭筋": 100},
    "レッグカール": {"ハムストリング": 100},
    "スクワット": {"大腿四頭筋": 55, "ハムストリング": 45},
    "ブルガリアンスクワット": {"大腿四頭筋": 60, "ハムストリング": 40},
    "スプリットスクワット": {"大腿四頭筋": 60, "ハムストリング": 40}
}

# --- Q学習アルゴリズム ---
def q_learning_training_selection(current_scores, target_scores, training_scores_data,
                                  num_episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1, num_actions=5):
    q_table = {}
    actions = list(training_scores_data.keys())

    def get_state_key(scores):
        return tuple(scores)

    for episode in range(num_episodes):
        current_state = current_scores.copy()
        selected_actions = set()

        for step in range(num_actions):
            state_key = get_state_key(current_state)
            if state_key not in q_table:
                q_table[state_key] = {action: 0 for action in actions}

            available_actions = [a for a in actions if a not in selected_actions]
            if not available_actions:
                break

            if random.random() < epsilon:
                action = random.choice(available_actions)
            else:
                action = max(available_actions, key=lambda a: q_table[state_key].get(a, 0))

            new_scores = current_state.copy()
            for muscle, score in training_scores_data[action].items():
                muscle_idx = next((i for i, m in enumerate(minor_muscles) if m["name"] == muscle), None)
                if muscle_idx is not None:
                    new_scores[muscle_idx] += score

            reward = -sum(abs(t - s) for t, s in zip(target_scores, new_scores))

            new_state_key = get_state_key(new_scores)
            if new_state_key not in q_table:
                q_table[new_state_key] = {action: 0 for action in actions}

            q_table[state_key][action] += alpha * (
                reward + gamma * max(q_table[new_state_key].values()) - q_table[state_key][action]
            )

            current_state = new_scores
            selected_actions.add(action)

    state_key = get_state_key(current_scores)
    sorted_actions = sorted(q_table.get(state_key, {}).items(), key=lambda x: x[1], reverse=True)
    top_5_actions = [a for a, _ in sorted_actions[:num_actions]]

    final_scores = current_scores.copy()
    total_added_scores = {muscle["name"]: 0 for muscle in minor_muscles}
    for action in top_5_actions:
        for muscle, score in training_scores_data[action].items():
            muscle_idx = next((i for i, m in enumerate(minor_muscles) if m["name"] == muscle), None)
            if muscle_idx is not None:
                final_scores[muscle_idx] += score
                total_added_scores[muscle] += score

    return top_5_actions, total_added_scores, final_scores

# --- メイン関数 ---
def main():
    muscle_score_dict = get_weighted_muscle_scores()
    current_scores = [muscle_score_dict.get(m["name"], 0.0) for m in minor_muscles]
    target_scores = [150.0] * len(minor_muscles)


    print("=== 現在のスコア ===")
    for m, s in zip(minor_muscles, current_scores):
        print(f"{m['name']}: {s:.2f}")

    top_5_actions, total_added_scores, final_scores = q_learning_training_selection(
        current_scores, target_scores, training_scores_data
    )

    print("=== 最適な5つのトレーニング ===")
    for i, action in enumerate(top_5_actions):
        print(f"{i+1}. {action}")

    print("\n=== 追加されたスコア ===")
    for muscle, score in total_added_scores.items():
        print(f"{muscle}: {score}")

    print("\n=== 最終スコア ===")
    for i, (m, s) in enumerate(zip(minor_muscles, final_scores)):
        print(f"{m['name']}: {s:.2f}")

# --- 実行ブロック ---
if __name__ == "__main__":
    main()
