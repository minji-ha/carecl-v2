# 진단 리포트 이미지 목록 (개발 전달용)

리포트 글은 DB에서 불러오고, 그림은 이 폴더(`assets/img/report/`)의 파일을 **키 이름 그대로** 불러오면 됩니다.
시안 코드는 `js/report.js`의 `RIMG + '폴더/키.확장자'`로 불러오며, 6가지 유형(혼합형 3종 포함 8가지 결과) 모두 이 폴더 안의 파일만 씁니다.
파일은 `python tools/build_report_assets.py`로 다시 만들 수 있습니다 (2026-11-27).

## 1. 6가지 유형 아이콘 — `types/`

| 키 | 유형 | 기본(회색) | 내 유형(주황) |
|---|---|---|---|
| `early` | 초기노화형 · 전구형 | `types/early.svg` | `types/early-on.svg` |
| `tired` | 피로형 · 너구리형 | `types/tired.svg` | `types/tired-on.svg` |
| `fine` | 잔주름형 · 스카프형 | `types/fine.svg` | `types/fine-on.svg` |
| `sag` | 변형·처짐형 · 아이스크림형 | `types/sag.svg` | `types/sag-on.svg` |
| `muscle` | 근육형 · 협곡형 | `types/muscle.svg` | `types/muscle-on.svg` |
| `mixed` | 혼합형 · 지도형 | `types/mixed.svg` | `types/mixed-on.svg` |

리포트 맨 위 6가지 유형 띠에서 씁니다. 고객 유형만 `-on`이고, 나머지 다섯 개는 기본 아이콘입니다.

## 2. 집중 케어 부위 — `area/{부위 코드}.jpg` (360×360)

Aging Map 22 부위 코드 = 파일 이름. 원 안에 잘라 보여 주고, 가운데 주황 점은 화면(CSS)에서 얹습니다.

| 구역 | 코드 → 파일 |
|---|---|
| 상안부 | `U1` 이마 · `U2` 미간 · `U3` 눈썹 · `U4` 눈가 · `U5` 눈밑 · `U6` 눈꺼풀 · `U7` 관자놀이 |
| 중안부 | `M1` 앞광대 · `M2` 심부볼 · `M3` 팔자 · `M4` 옆볼 |
| 하안부 | `L1` 인중·윗입술 · `L2` 마리오네트 · `L3` 턱 · `L4` 턱선 · `L5` 귀뒤 · `L6` 이중턱 |
| 목·바디 | `B1` 목 · `B2` 데콜테 |

**제작 필요:** `B3` 손등 · `B4` 팔뚝 · `B5` 무릎은 얼굴 사진 밖이라 아직 파일이 없습니다. 지금 결과 데이터에는 쓰이지 않지만, DB에 들어오면 같은 규격(360×360, 가운데가 해당 부위)으로 만들어야 합니다.

## 3. 모드별 사용 방법 그림 — `guide/` (TECH FIT 사용 가이드북 12~14쪽)

| 키 | 쓰는 곳 | 파일 |
|---|---|---|
| `eye` | 부위별 SHOT 가이드 — EYE SHOT 부위를 누르면 | `guide/eye.jpg` |
| `face` | 〃 FACE SHOT (일러스트만, 실사 사진 뺌) | `guide/face.jpg` |
| `body` | 〃 BODY SHOT | `guide/body.jpg` |
| `glow` | SHOT 이후 마무리 — GLOW 카드 | `guide/glow.jpg` (새 GLOW 가이드 받으면 교체) |
| `ems` | 〃 EMS 카드 | `guide/ems-side.png` (3컷 전체는 `guide/ems.jpg`) |

DB의 SHOT 모드 이름 → 키: `EYE SHOT`→`eye`, `FACE SHOT`→`face`, `BODY SHOT`→`body`, `GLOW 모드`→`glow`, `EMS 모드`→`ems`.

## 4. 관리 순서 — `steps/`

| 단계 글에 들어간 말 | 파일 |
|---|---|
| 세안 | `steps/wash.svg` (선 아이콘) |
| 기초 관리(토너·에멀젼) | `steps/basic.svg` (선 아이콘) |
| 그리드 마스크팩 / 콜라겐 젤 | `steps/mask.svg` (선 아이콘) |
| EYE / FACE / BODY SHOT 모드 | `steps/eye.jpg` · `steps/face.jpg` · `steps/body.jpg` (기기 사진) |
| GLOW 모드 · EMS 모드 | `steps/glow.jpg` · `steps/ems.jpg` (기기 사진) |
| 그 밖의 단계 (예: 턱선, 팔자 2 Pass) | `steps/dot.svg` |

개발 시에는 단계마다 DB에 `step_icon` 키(wash · basic · mask · eye · face · body · glow · ems · dot)를 두는 것을 권장합니다. 시안은 글에 든 말로 고릅니다.

## 5. 생활습관 아이콘 — `life/`

`sun` 자외선 · `water` 수분 섭취 · `drop` 보습 · `moon` 수면 · `face` 그 밖 — `life/{키}.svg`

## 6. 유형과 관계없이 같은 사진 — `common/`

| 자리 | 파일 |
|---|---|
| 02 홈케어 루틴 · 추천 성분 · 생활습관 | `common/care.jpg` (거울 앞 여성, 제품 세트는 잘라 냄) |
| 03 고주파(RF) 기술과 케어클 | `common/rf-stamp.jpg` |
| 06 혜택 — TECH FIT | `common/coupon-techfit.jpg` |
| 06 혜택 — 소모품 | `common/coupon-consumables.jpg` (제품컷 케어클20804) |

## 7. 아직 비어 있는 자리

- 07 고객 후기 사진 — 화면에 '후기 이미지 자리'로 비워 둠. 후기마다 1장(가로 4:3) 필요.
- GLOW 모드 사용 가이드 — 새 버전 받으면 `guide/glow.jpg` 교체.
- `area/B3.jpg` · `area/B4.jpg` · `area/B5.jpg` (위 2번).
