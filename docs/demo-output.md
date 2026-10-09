# 합성 데이터 예제 실행 결과

이 저장소의 공개 예제는 모두 합성 데이터를 사용합니다.

아래 결과는 데이터 처리 방식을 설명하기 위한 예제이며 실제 시장 데이터나 실거래 성과가 아닙니다.

## 1. 기본 관측 데이터 예제

실행 명령:

```powershell
python src/analyze_sample.py
```

출력:

```text
SYNTHETIC DATA DEMO - not real market results
total: 8
duplicate: 1
invalid_id: 0
invalid_price: 2
valid: 5
mean_price_change_pct: +0.00
median_price_change_pct: +0.00
```

입력 8행 중 중복 1행과 유효하지 않은 가격이 포함된 2행을 제외하고 5행을 계산합니다.

평균과 중앙값이 0%인 것은 합성 데이터의 구성에 따른 결과이며 투자 성과를 의미하지 않습니다.

---

## 2. 연구 Outcome 예제

실행 명령:

```powershell
python src/analyze_research_outcomes.py
```

출력:

```text
SYNTHETIC RESEARCH OUTCOME DEMO - not real market results

STATUS SUMMARY
total: 10
observed: 8
unresolved: 1
censored: 1
duplicate: 0
invalid: 0

HORIZON SUMMARY

+1m
  observed: 4
  unresolved: 0
  censored: 0
  mean_return_pct: +1.00
  median_return_pct: +1.50

+3m
  observed: 1
  unresolved: 0
  censored: 0
  mean_return_pct: +3.50
  median_return_pct: +3.50

+5m
  observed: 3
  unresolved: 0
  censored: 0
  mean_return_pct: +2.67
  median_return_pct: +2.00

+30m
  observed: 0
  unresolved: 1
  censored: 1
  return_pct: N/A
```

10개의 Outcome 가운데 8개는 정상적으로 관측됐고, 1개는 `UNRESOLVED`, 1개는 `CENSORED`로 구분됩니다.

특히 +30분 결과에서는 정상적으로 관측된 데이터가 없기 때문에 수익률을 0%로 계산하지 않고 `N/A`로 표시합니다.

이는 실제로 가격 변화가 없었던 경우와 데이터를 확보하지 못했거나 구조적으로 측정할 수 없었던 경우를 구분하기 위한 처리입니다.

---

## 예제의 목적

두 예제는 서로 다른 데이터 처리 문제를 보여줍니다.

`analyze_sample.py`는 다음 내용을 확인합니다.

- 중복 관측 제거
- 유효하지 않은 가격 구분
- 정상 데이터만 이용한 가격 변화율 계산

`analyze_research_outcomes.py`는 다음 내용을 확인합니다.

- 여러 horizon의 Outcome 관리
- `OBSERVED`, `UNRESOLVED`, `CENSORED` 상태 구분
- 측정하지 못한 결과를 0% 수익률로 처리하지 않는 방식
- horizon별 평균 및 중앙값 계산

모든 종목명, 가격, 시각과 결과는 설명을 위해 만든 합성 값이며 실제 시장 데이터와 관련이 없습니다.
