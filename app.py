from pathlib import Path
import re

from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np

from agent02_experiment import (
    Config,
    ECommerceEnvironment,
    QLearningAgent,
    RuleBasedAgent,
    train_rl_against_rule,
)

app = Flask(__name__)
app.secret_key = "change-this-for-local-demo"
BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "agent02_results"
Q_TABLE_FILE = RESULT_DIR / "q_tables.txt"

config = Config()


def load_or_train_agent():
    """Load the saved text Q-table when possible; otherwise train once."""
    agent = QLearningAgent(
        alpha=config.alpha,
        gamma=config.gamma,
        epsilon=config.epsilon_min,
        seed=config.seed + 10_000,
    )

    if Q_TABLE_FILE.exists():
        text = Q_TABLE_FILE.read_text(encoding="utf-8")
        pattern = re.compile(
            r"State=\((\d+),\s*(\d+)\)\s*\|\s*Q0=([-+\deE.]+)\s*\|\s*Q1=([-+\deE.]+)"
        )
        found = False
        for demand, previous_action, q0, q1 in pattern.findall(text):
            agent.q[int(demand), int(previous_action), 0] = float(q0)
            agent.q[int(demand), int(previous_action), 1] = float(q1)
            found = True
        if found:
            print(f"Loaded Q-table from {Q_TABLE_FILE}")
            return agent

    print("No readable saved Q-table found; training RL agent once...")
    agent, _ = train_rl_against_rule(config, seed=config.seed)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    # Save the text Q-table in the same format as the original experiment.
    with Q_TABLE_FILE.open("w", encoding="utf-8") as file:
        file.write("Q-table: Q[demand, competitor_previous_action, action]\n")
        file.write("Action 0 = no discount; Action 1 = discount\n\n")
        for demand in range(2):
            for previous_action in range(2):
                q0, q1 = agent.q[demand, previous_action]
                best = int(np.argmax(agent.q[demand, previous_action]))
                file.write(
                    f"State=({demand}, {previous_action}) | Q0={q0:.6f} | "
                    f"Q1={q1:.6f} | Greedy action={best}\n"
                )
    return agent


rl_agent = load_or_train_agent()
rule_agent = RuleBasedAgent()
sim_env = ECommerceEnvironment(config, seed=config.seed + 999)


def initialize_session():
    session["step"] = 0
    session["previous_actions"] = [0, 0]  # [RL, rule-based]
    session["history"] = []
    session["total_rewards"] = [0.0, 0.0]


@app.route("/", methods=["GET"])
def index():
    if "step" not in session:
        initialize_session()
    return render_template(
        "index.html",
        step=session["step"] + 1,
        history=session.get("history", []),
        total_rewards=session.get("total_rewards", [0.0, 0.0]),
        q_table=rl_agent.q.tolist(),
    )


@app.route("/step", methods=["POST"])
def run_step():
    if "step" not in session:
        initialize_session()

    demand = int(request.form.get("demand", "0"))
    if demand not in (0, 1):
        flash("Demand không hợp lệ.", "error")
        return redirect(url_for("index"))

    previous_actions = session.get("previous_actions", [0, 0])
    # State format follows the original environment:
    # RL observes the rule agent's previous action and vice versa.
    states = [
        (demand, previous_actions[1]),
        (demand, previous_actions[0]),
    ]
    rl_action = rl_agent.act(states[0], explore=False)
    rule_action = rule_agent.act(states[1])
    actions = [rl_action, rule_action]

    # Reuse the original environment's reward/conversion logic.
    sim_env.demand = demand
    sim_env.previous_actions = list(previous_actions)
    _, rewards, info = sim_env.step(actions)

    action_names = ["Không giảm giá", "Giảm giá"]
    row = {
        "step": session["step"] + 1,
        "demand": "Cao" if demand == 1 else "Thấp",
        "customers": info["customers"],
        "rl_action": action_names[rl_action],
        "rule_action": action_names[rule_action],
        "rl_conversion": round(info["conversion"][0], 3),
        "rule_conversion": round(info["conversion"][1], 3),
        "rl_sales": info["sales"][0],
        "rule_sales": info["sales"][1],
        "rl_reward": round(rewards[0], 2),
        "rule_reward": round(rewards[1], 2),
    }

    history = session.get("history", [])
    history.append(row)
    session["history"] = history[-50:]
    session["step"] = session.get("step", 0) + 1
    session["previous_actions"] = actions
    totals = session.get("total_rewards", [0.0, 0.0])
    session["total_rewards"] = [
        round(totals[0] + rewards[0], 2),
        round(totals[1] + rewards[1], 2),
    ]
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    initialize_session()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
