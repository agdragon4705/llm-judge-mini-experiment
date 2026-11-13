"""채점자 여러 명 + LLM 비교. 사용법: python src/multi.py data/scores.csv
rater3 점수는 data/rater3.txt(한 줄에 숫자 하나, 30개)가 있으면 자동으로 추가."""
import os, sys
import numpy as np
import pandas as pd

d = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/scores.csv")
d = d.rename(columns={"rater1_me": "me", "rater2_friend": "friend", "llm_A_run0": "orig", "llm_A_run1": "A1", "llm_A_run2": "A2", "llm_B_run1": "B1", "llm_B_run2": "B2"})
if os.path.exists("data/rater3.txt"):
    d["r3"] = [int(x) for x in open("data/rater3.txt").read().split()]
humans = [c for c in ["me", "friend", "r3"] if c in d.columns]
d["llm"] = d[["orig", "A1", "A2", "B1", "B2"]].mean(axis=1)  # LLM 5회 평균

def stats(a, b):
    x = a - b
    return dict(평균차=round(x.mean(), 2), MAE=round(x.abs().mean(), 2),
                정확일치=round((x == 0).mean(), 2), 이내1=round((x.abs() <= 1).mean(), 2),
                Spearman=round(a.corr(b, method="spearman"), 2))

print("채점자별 평균:", {c: round(d[c].mean(), 2) for c in humans + ["llm"]})
print("\n[사람끼리]")
for i, a in enumerate(humans):
    for b in humans[i + 1:]:
        print(a, "vs", b, stats(d[a], d[b]))
print("\n[LLM(5회 평균) vs 각 사람]")
for h in humans:
    print("llm vs", h, stats(d["llm"], d[h]))
print("\n[LLM 첫 채점(orig) vs 각 사람]")
for h in humans:
    print("orig vs", h, stats(d["orig"].astype(float), d[h].astype(float)))
d["humans_mean"] = d[humans].mean(axis=1)
print("\n[LLM vs 사람 평균]", stats(d["llm"], d["humans_mean"]))
big = d.assign(spread=d[humans].max(axis=1) - d[humans].min(axis=1)).sort_values("spread", ascending=False)
print("\n사람끼리 가장 갈린 문장 TOP 5")
print(big[["id", "genre"] + humans + ["orig"]].head(5).to_string(index=False))
