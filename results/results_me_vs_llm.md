# 결과 요약

## 전체 일치도

- 채점한 문장 수: 30
- Spearman 상관계수: 0.26
- 가중 카파(QWK): 0.32
- 정확히 같은 점수 비율: 0.50
- ±1점 이내 비율: 0.90
- 평균 절대 오차(MAE): 0.67
- 평균 점수 차이(LLM - 나): 0.47

## 장르별

```
            n  내 평균  LLM 평균  평균 차이  Spearman
genre                                       
daily    10.0   3.8     4.7    0.9     -0.51
esports  10.0   3.5     3.9    0.4      0.44
news     10.0   4.7     4.8    0.1      0.22
```

## LLM이 나보다 후하게 준 문장 TOP 5

```
 id   genre                                                      english                                                 korean_mt  my_score  llm_score                                        llm_reason
 26   daily I can't believe you haven't seen that movie yet — you hav...                   아직 그 영화를 안 봤다니 믿을 수가 없어. 이번 주말에 꼭 봐야 해.         2          5                                  놀람과 권유의 어조가 정확하다
 16 esports Gen.G is playing it safe, farming under the tower and wai...              Gen.G는 안전하게 타워 아래에서 파밍하며 상대방의 실수를 기다리고 있습니다.         2          5                          안전한 운영·파밍·상대 실수 대기가 정확하다
 25   daily It's raining cats and dogs outside, so let's stay in toni...                               밖에 비가 억수같이 쏟아지니 오늘은 집에서 쉬자.         3          5                            관용구를 '억수같이'로 자연스럽게 살렸다
 14 esports The crowd goes wild as the underdogs take game three and ...         약체로 평가받던 팀이 3세트를 따내며 승부를 마지막 세트로 끌고 가자 관중들은 열광했다.         4          5 'game three'와 'force a decider'가 e스포츠 문맥에 맞게 번역됐다
  2    news Officials said the bridge will remain closed until at lea... 관계자들은 엔지니어들이 피해 상황을 평가하는 동안 다리가 최소한 3월까지는 폐쇄될 것이라고 밝혔습니다.         4          5           '최소한 3월까지는 폐쇄'와 피해 평가 중이라는 조건이 정확히 전달됐다
```

## LLM이 나보다 박하게 준 문장 TOP 5

```
 id   genre                                                      english                                                  korean_mt  my_score  llm_score                                         llm_reason
  4    news The city council voted 7-2 to approve the new housing pla... 시의회는 일부 주민들의 반대에도 불구하고 새로운 주택 건설 계획을 찬성 7표, 반대 2표로 승인했습니다.         5          4 7-2 표결과 반대 의견은 정확하지만 'housing plan'에 없는 '건설'이 추가됐다
 17 esports If they lose this fight, they're basically out of the tou...                           이번 경기에서 지면 사실상 토너먼트에서 탈락하는 셈입니다.         4          3                 'fight'(교전)를 '경기'로 옮겨 상황의 규모가 달라졌다
 24   daily       She told her sister that she would pick her up at six.                                그녀는 여동생에게 6시에 데리러 가겠다고 말했다.         5          4         대명사 모호성을 한 해석으로 정했고 'sister'를 '여동생'으로 가정했다
  1    news The central bank held interest rates steady on Tuesday, c...                 중앙은행은 화요일에 인플레이션에 대한 불확실성을 이유로 기준금리를 동결했다.         5          5              의미·수치 모두 정확하고 자연스러우며 '기준금리'도 문맥상 적절하다
  7    news The company denied that it had known about the defect bef...              회사 측은 리콜 발표 이전에 해당 결함에 대해 알고 있었다는 주장을 부인했습니다.         5          5                         '알고 있었다는 사실을 부인'한 의미가 정확하다
```

산점도: scatter.png (점선 위에 있을수록 두 점수가 일치)