"""사람 채점 vs LLM 채점 비교 분석.

사용법:  python analysis.py ratings.csv
필요한 것: pandas, numpy, matplotlib (구글 코랩에는 기본 설치돼 있음)
결과: 화면 출력 + results.md + scatter.png
"""
import sys

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "ratings.csv"
df = pd.read_csv(path)

required = ["id", "genre", "english", "korean_mt", "my_score", "llm_score"]
missing = [c for c in required if c not in df.columns]
if missing:
    sys.exit(f"ratings.csv에 필요한 열이 없어요: {missing}")

for col in ["my_score", "llm_score"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

done = df.dropna(subset=["my_score", "llm_score"]).copy()
n = len(done)
if n < 5:
    sys.exit(f"점수가 모두 채워진 행이 {n}개뿐이에요. my_score와 llm_score를 채운 뒤 다시 실행하세요.")

done["diff"] = done["llm_score"] - done["my_score"]  # +면 LLM이 나보다 후함


def quadratic_weighted_kappa(a, b, lo=1, hi=5):
    """순서가 있는 점수의 일치도(1이면 완전 일치, 0이면 우연 수준)."""
    k = hi - lo + 1
    obs = np.zeros((k, k))
    for x, y in zip(a.astype(int), b.astype(int)):
        obs[x - lo, y - lo] += 1
    exp = np.outer(obs.sum(axis=1), obs.sum(axis=0)) / obs.sum()
    w = np.array([[(i - j) ** 2 for j in range(k)] for i in range(k)]) / (k - 1) ** 2
    denom = (w * exp).sum()
    return np.nan if denom == 0 else 1 - (w * obs).sum() / denom


def safe_corr(x, y):
    if x.nunique() < 2 or y.nunique() < 2:
        return np.nan
    return x.corr(y, method="spearman")


overall = {
    "채점한 문장 수": n,
    "Spearman 상관계수": safe_corr(done["my_score"], done["llm_score"]),
    "가중 카파(QWK)": quadratic_weighted_kappa(done["my_score"], done["llm_score"]),
    "정확히 같은 점수 비율": (done["diff"] == 0).mean(),
    "LLM이 나보다 후한 문장 비율": (done["diff"] > 0).mean(),  # 직접 추가한 줄
    "±1점 이내 비율": (done["diff"].abs() <= 1).mean(),
    "평균 절대 오차(MAE)": done["diff"].abs().mean(),
    "평균 점수 차이(LLM - 나)": done["diff"].mean(),
}

by_genre = (
    done.groupby("genre")
    .apply(
        lambda g: pd.Series(
            {
                "n": len(g),
                "내 평균": g["my_score"].mean(),
                "LLM 평균": g["llm_score"].mean(),
                "평균 차이": g["diff"].mean(),
                "Spearman": safe_corr(g["my_score"], g["llm_score"]),
            }
        )
    )
    .round(2)
)

# ---- 내 확신도별 일치도 (my_confidence: 1=헷갈림, 2=보통, 3=확신) ----
by_conf = None
if "my_confidence" in done.columns:
    done["my_confidence"] = pd.to_numeric(done["my_confidence"], errors="coerce")
    with_conf = done.dropna(subset=["my_confidence"])
    if len(with_conf):
        by_conf = (
            with_conf.groupby("my_confidence")
            .apply(
                lambda g: pd.Series(
                    {
                        "n": len(g),
                        "평균 절대 오차": g["diff"].abs().mean(),
                        "±1점 이내 비율": (g["diff"].abs() <= 1).mean(),
                        "평균 차이": g["diff"].mean(),
                    }
                )
            )
            .round(2)
        )

cols = ["id", "genre", "english", "korean_mt", "my_score", "llm_score"]
if "my_confidence" in done.columns:
    cols.insert(5, "my_confidence")
if "llm_reason" in done.columns:
    cols.append("llm_reason")
too_generous = done.sort_values("diff", ascending=False).head(5)[cols]
too_strict = done.sort_values("diff", ascending=True).head(5)[cols]

# ---- 산점도 (점이 겹치지 않게 살짝 흔들어서 그림) ----
rng = np.random.default_rng(0)
jx = done["my_score"] + rng.uniform(-0.12, 0.12, n)
jy = done["llm_score"] + rng.uniform(-0.12, 0.12, n)
plt.figure(figsize=(5, 5))
for genre, g in done.groupby("genre"):
    plt.scatter(jx[g.index], jy[g.index], label=genre, alpha=0.8)
plt.plot([1, 5], [1, 5], "k--", linewidth=1)
plt.xlabel("my score")
plt.ylabel("LLM score")
plt.title("Human vs LLM judge")
plt.xticks(range(1, 6))
plt.yticks(range(1, 6))
plt.legend()
plt.tight_layout()
plt.savefig("scatter.png", dpi=150)

# ---- 출력 + results.md ----
lines = ["# 결과 요약", "", "## 전체 일치도", ""]
for k, v in overall.items():
    lines.append(f"- {k}: {v:.2f}" if isinstance(v, float) else f"- {k}: {v}")
fence = "```"
lines += ["", "## 장르별", "", fence, by_genre.to_string(), fence, ""]
if by_conf is not None:
    lines += [
        "## 내 확신도별 일치도 (1=헷갈림, 2=보통, 3=확신)",
        "",
        fence,
        by_conf.to_string(),
        fence,
        "확신이 낮은 문장에서 LLM과 더 많이 갈렸다면, 사람 점수가 '정답'이 아닐 수 있다는 뜻이다.",
        "",
    ]
lines += ["## LLM이 나보다 후하게 준 문장 TOP 5", "", fence, too_generous.to_string(index=False, max_colwidth=60), fence, ""]
lines += ["## LLM이 나보다 박하게 준 문장 TOP 5", "", fence, too_strict.to_string(index=False, max_colwidth=60), fence, ""]
lines += ["산점도: scatter.png (점선 위에 있을수록 두 점수가 일치)"]
report = "\n".join(lines)
print(report)
with open("results.md", "w", encoding="utf-8") as f:
    f.write(report)
