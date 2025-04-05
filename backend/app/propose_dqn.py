import random
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

# minor_musclesの定義
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
    {"name": "ハムストリング", "major_muscle_id": "leg_id"}
]

# トレーニングデータ（例）
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

# Q学習ネットワークの定義
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)  # 入力層（状態サイズ）
        self.fc2 = nn.Linear(128, 128)         # 隠れ層
        self.fc3 = nn.Linear(128, action_size) # 出力層（行動数）

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.buffer = []
        self.index = 0

    def push(self, experience):
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.index] = experience
            self.index = (self.index + 1) % self.capacity

    def sample(self, batch_size=32):
        return random.sample(self.buffer, min(len(self.buffer), batch_size))

    def size(self):
        return len(self.buffer)

class DQNAgent:
    def __init__(self, state_size, action_size, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon  # 探索率（ランダム行動）
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.replay_buffer = ReplayBuffer(capacity=10000)  # capacityを指定
        self.model = self._build_model()  # Qネットワーク
        self.target_model = self._build_model()  # ターゲットネットワーク
        self.update_target_model()  # 初回のターゲットネットワーク更新

    def _build_model(self):
        # PyTorchでのニューラルネットワークモデル構築
        model = nn.Sequential(
            nn.Linear(self.state_size, 64),  # 入力層 -> 隠れ層1
            nn.ReLU(),
            nn.Linear(64, 64),  # 隠れ層1 -> 隠れ層2
            nn.ReLU(),
            nn.Linear(64, self.action_size)  # 隠れ層2 -> 出力層
        )
        return model

    def select_action(self, state, selected_actions):
        # エクスプロレーションとエクスプロイテーションのバランス
        if random.random() < self.epsilon:
            # ランダムに行動を選択（すでに選ばれた行動は除外）
            available_actions = [a for a in range(self.action_size) if a not in selected_actions]
            return random.choice(available_actions)  # ランダムなアクション（探索）
        else:
            q_values = self.model(torch.tensor(state, dtype=torch.float32).unsqueeze(0))  # 状態をテンソルに変換してモデルに入力
            available_actions = [a for a in range(self.action_size) if a not in selected_actions]
            # 最大Q値を持つアクションの中から選択
            return max(available_actions, key=lambda x: q_values[0][x].item())  # 最大Q値を持つアクション（活用）

    def replay(self):
        # 経験リプレイから学習
        batch = self.replay_buffer.sample()
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                target += 0.99 * torch.max(self.target_model(torch.tensor(next_state, dtype=torch.float32).unsqueeze(0))[0])
            target_f = self.model(torch.tensor(state, dtype=torch.float32).unsqueeze(0))
            target_f[0][action] = target
            loss = nn.MSELoss()(target_f, torch.tensor(target_f, dtype=torch.float32))
            optimizer = optim.Adam(self.model.parameters())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        # epsilonの減衰（探索率を減らす）
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        # ターゲットネットワークの重みをQネットワークにコピー
        self.target_model.load_state_dict(self.model.state_dict())

# Q学習のトレーニング関数（修正後）
def q_learning_training_selection(current_scores, target_scores, training_scores_data, num_episodes=1000):
    state_size = len(current_scores)
    action_size = len(training_scores_data)

    agent = DQNAgent(state_size, action_size)
    optimal_actions = []  # 提案された5つの行動
    final_scores = current_scores.copy()

    for episode in range(num_episodes):
        state = current_scores  # 現在のスコアを状態として使用

        actions_taken = []  # 選択されたアクションを保存
        selected_actions = set()  # 選ばれたアクションを記録するセット

        for _ in range(5):  # 5回の行動選択
            # 選択可能なアクションをフィルタリング（すでに選ばれたアクションを除外）
            if len(selected_actions) == action_size:
                break  # すべてのアクションが選ばれた場合、終了

            # ランダムに選択されたアクション（重複しないように）
            action = agent.select_action(state, selected_actions)  # Q学習に基づいてアクションを選択

            action_name = list(training_scores_data.keys())[action]

            # 新しいスコアを計算
            new_scores = state.copy()
            for muscle, score in training_scores_data[action_name].items():
                muscle_idx = next((i for i, m in enumerate(minor_muscles) if m["name"] == muscle), None)
                if muscle_idx is not None:
                    new_scores[muscle_idx] += score

            actions_taken.append({
                "action": action_name,
                "added_scores": training_scores_data[action_name],
                "new_scores": new_scores
            })

            selected_actions.add(action)
            state = new_scores

        # 合計スコアを計算して報酬を計算
        final_state = actions_taken[-1]['new_scores']
        reward = -sum([abs(t - s) for t, s in zip(target_scores, final_state)])

        # 経験リプレイに追加
        done = False  # エピソード終了フラグ
        state = current_scores
        for action_data in actions_taken:
            action_idx = list(training_scores_data.keys()).index(action_data['action'])
            next_state = action_data['new_scores']
            agent.replay_buffer.push((state, action_idx, reward, next_state, done))
            state = next_state
        agent.replay()

        if episode % 10 == 0:
            agent.update_target_model()

        if episode % 100 == 0:
            print(f"エピソード {episode}")

    return actions_taken

# 現在のスコア
current_scores = [100, 30, 50, 150, 0, 60, 20, 20, 40, 50]

# 目標のスコア
target_scores = [200, 200, 200, 200, 200, 100, 100, 100, 100, 100]

# q-learning訓練の開始
optimal_actions = q_learning_training_selection(current_scores, target_scores, training_scores_data)

# 結果の表示
print("\n提案された5つのトレーニングアクションとその結果:")
for action in optimal_actions:
    print(f"トレーニング: {action['action']}, 追加されたスコア: {action['added_scores']}, 新しいスコア: {action['new_scores']}")