# -*- coding: utf-8 -*-
"""careCL GRID 시안 (쥬베룩 톤, 2026-11-05 · STEM 최종본에서 복사) — 페이지 생성기

    python build.py

공통 헤더·푸터·로딩 물방울을 한곳에서 관리하고 페이지를 찍어낸다.
생성된 HTML을 직접 고치면 다음 빌드 때 덮어써진다.
"""
import io
import os
import re
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = time.strftime("%y%m%d%H%M%S")


def read(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


# ── 로고 (벡터, currentColor) ─────────────────────────────
LOGO = re.sub(r"<title>.*?</title>\s*", "", read("assets/img/carecl-logo.svg"), flags=re.S).strip()

# ── 메뉴 — 노션 '케어클 홈페이지 구성' 메뉴 구조 그대로 (COMPANY / AGING LAB / TECHNOLOGY / PRODUCTS / CONTACT)
# 헤더 드롭다운·모바일 메뉴·푸터가 모두 이 표를 쓴다. 서브 페이지 탭(MENU)도 같은 순서.
HNAV = [
    ("Company", "about.html", [("About careCL", "about.html", "회사 소개"),
                               ("Our Story", "greeting.html", "브랜드 스토리"),
                               ("R&amp;D / Patent", "rnd.html", "연구개발 · 특허"),
                               ("Awards &amp; Certification", "certification.html", "수상 · 인증"),
                               ("Contact", "contact.html", "문의")]),
    ("Aging Lab", "aging-types.html", [("6 Aging Types", "aging-types.html", "6가지 노화 타입"),
                                       ("Aging Map 22", "aging-map.html", "22개 관리 부위")]),
    ("Technology", "technology.html", [("careCL Technology", "technology.html", "TECH FIT 기술"),
                                       ("Product", "products.html", "디바이스 · 코스메틱")]),
]   # 수정요청 261030: Contact는 Company 밑, 기술 두 페이지는 하나로 / 261102: Technology 밑은 careCL Technology · Product 둘
# 오른쪽 — SHOP · LOGIN · KR/EN(작게). 공식몰·로그인 주소는 받는 대로 바꾼다.
SHOP_HREF = "products.html"
LOGIN_HREF = "#"


def head(title, desc, sub=False, css=(), body_cls=""):
    subcss = f'<link rel="stylesheet" href="css/sub.css?v={VER}">\n' if sub else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/img/carecl-logo.svg" type="image/svg+xml">
<link rel="preload" href="fonts/metropolis-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/urbanist-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/caviar-dreams.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/static/woff2/SUIT.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.7.2/animate.min.css">
<link rel="stylesheet" href="css/stem.css?v={VER}">
<link rel="stylesheet" href="css/home261019.css?v={VER}">
{subcss}{"".join(f'<link rel="stylesheet" href="{c}?v={VER}">' + chr(10) for c in css if "grid" not in c)}<link rel="stylesheet" href="css/grid.css?v={VER}">
{"".join(f'<link rel="stylesheet" href="{c}?v={VER}">' + chr(10) for c in css if "grid" in c)}<script type="importmap">{{"imports":{{"three":"./libs/three/three.module.min.js"}}}}</script>
</head>
<body{(' class="' + body_cls + '"') if body_cls else ""}>
"""


def loader():
    return f"""<div class="loader" data-loader aria-hidden="true">
  <div class="led9 loader__head" data-led9="red" data-led9-mode="progress"><canvas></canvas></div>
  <span class="loader__logo">{LOGO}</span>
  <span class="loader__count" data-loader-count>00</span>
</div>
"""


def header(active=""):
    def group(t, h, subs):
        on = active and (active == h or any(active == sh for _, sh, _ in subs))
        sub = "".join(f'<a href="{sh}"><b>{st}</b><small>{sk}</small></a>' for st, sh, sk in subs)
        return (f'<div class="hnav"><a class="hnav__top" href="{h}"{" aria-current=\"page\"" if on else ""}>{t}</a>'
                f'<div class="hnav__sub"><div class="hnav__in">{sub}</div></div></div>')
    left = "".join(group(*g) for g in HNAV)
    mnav = "".join(
        f'<div class="mnav__grp"><a class="mnav__top" href="{h}">{t}</a>'
        + "".join(f'<a class="mnav__sub" href="{sh}">{st}<small>{sk}</small></a>' for st, sh, sk in subs) + '</div>'
        for t, h, subs in HNAV)
    return f"""<header class="header">
  <a class="header__logo" href="index.html" aria-label="careCL 홈">{LOGO}</a>
  <div class="header__pill">
    <nav class="header__nav" aria-label="주 메뉴">{left}</nav>
    <nav class="header__nav header__nav--right header__util" aria-label="쇼핑 · 로그인 · 언어">
      <a href="{SHOP_HREF}">Shop</a><a href="{LOGIN_HREF}">Login</a>
      <span class="header__lang"><a href="#" aria-current="true" lang="ko">KR</a><i aria-hidden="true">/</i><a href="#" lang="en">EN</a></span>
    </nav>
  </div>
  <button class="header__menu" type="button" data-menu aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span></button>
</header>
<nav class="mnav" aria-label="모바일 메뉴">{mnav}
  <div class="mnav__util"><a href="{SHOP_HREF}">Shop</a><a href="{LOGIN_HREF}">Login</a><span class="header__lang"><a href="#" aria-current="true">KR</a><i aria-hidden="true">/</i><a href="#">EN</a></span></div>
</nav>
"""


# 푸터 SNS — 링크 주소는 받는 대로 href에 넣는다. 유튜브만 가로형이라 따로 크기를 준다.
SNS = [("Instagram", "instagram", ""), ("Facebook", "facebook", ""),
       ("YouTube", "youtube", ' class="is-wide"'), ("KakaoTalk", "kakaotalk", "")]

FOOTER = f"""<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div class="foot__brand">
        <a class="foot__logo" href="index.html" aria-label="careCL 홈">{LOGO}</a>
      </div>
      <div class="foot__side">
        <h2>AI Skin Test</h2>
        <p>2분 설문으로 나의 노화 타입과<br>먼저 관리할 부위를 확인하세요.</p>
        <a class="btn-line" href="survey.html">진단 시작하기</a>
      </div>
    </div>
    <div class="foot__row">
      <nav class="foot__nav" aria-label="푸터 메뉴">
        {"".join(f'<a href="{h}">{t}</a>' for t, h, _ in HNAV)}
      </nav>
      <div class="foot__sns">{"".join(f'<a href="#" aria-label="{t}"><img{c} src="assets/img/sns/{f}.svg" alt=""></a>' for t, f, c in SNS)}</div>
    </div>
  </div>
  <div class="foot__bar">
    <span>CARECL CO.,Ltd. · CEO Hyungkyu Choi · 사업자등록번호 591-88-03097 · 통신판매업 제2025-고양일산동-0585호</span>
    <span>TEL +82 31-943-1028 · support@carecl.co.kr</span>
    <span>© 2026 CARECL. All rights reserved.</span>
  </div>
</footer>
"""


# 링크 없는 버튼(2026-11-06 요청) — 진단 비공개 중에도 보이게 <a> 대신 <button>
AIFAB = ('<button type="button" class="aifab" aria-label="AI 피부 진단"><span class="aifab__ico">'
         '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2.2 14 8.4 20.2 10.4 14 12.4 12 18.6 10 12.4 3.8 10.4 10 8.4Z" fill="currentColor"/>'
         '<circle cx="19.4" cy="4.2" r="1.7" fill="currentColor" opacity=".9"/><circle cx="4.8" cy="18.4" r="1.2" fill="currentColor" opacity=".7"/></svg></span>'
         '<span class="aifab__txt">AI 피부 진단</span></button>\n')


def tail(three=True, js=(), fab=True, mods=()):
    mod = f'<script type="module" src="js/device3d.js?v={VER}"></script>\n' if three else ""
    mod += "".join(f'<script type="module" src="{m}?v={VER}"></script>' + chr(10) for m in mods)
    return (AIFAB if fab else "") + f"""<script src="libs/lenis.min.js"></script>
<script src="js/led.js?v={VER}"></script>
<script src="js/stem.js?v={VER}"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/wow/1.1.2/wow.min.js"></script>
<script src="js/grid-header.js?v={VER}"></script>
{"".join(f'<script src="{j}?v={VER}"></script>' + chr(10) for j in js)}{mod}</body>
</html>
"""


# 배경에 깔리는 옅은 물결 면
WAVE = """<svg viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 210C210 120 380 60 640 92c260 32 330 170 560 182 170 9 300-60 400-120v520c-190 90-360 140-620 110-250-29-330-150-560-150C230 834 90 880 0 900Z"/></svg>"""


# ═══════════════════════════════════════════════════════════
#  메인
# ═══════════════════════════════════════════════════════════
# ── 메인 원고 (기존 사이트 메인 순서·문구 그대로) ─────────────
SOLUTIONS = [
    ("Device", "Device Solution", "정해진 자리에 머무르는 스탬핑 디바이스",
     "문지르지 않고 관리할 부위에 머물러 에너지를 전달합니다.", "c-techfit-case.jpg", "products.html"),
    ("Cosmetics", "Beauty Solution", "디바이스와 함께 쓰는 전용 코스메틱",
     "그리드 마스크와 전용 제형으로 관리 위치를 정확히 안내합니다.", "c-gel-drop.jpg", "products.html#cosmetics"),
    ("Aging Map 22", "Care Solution", "얼굴과 목 · 바디를 22개 부위로",
     "나의 노화 방식을 이해하고 먼저 관리할 곳부터 순서대로 제안합니다.", "n-mask-glass-wide.jpg", "aging-map.html"),
]

CORE = [  # (번호 EN, 제목, 질문, 링크 문구, 링크, 위치 left%, top%)
    ("01 Read", "6가지 노화 타입", "나는 어떻게 나이 드는가", "타입 보기", "aging-types.html", 14, 20),
    ("02 Map", "22개 관리 부위", "어디부터 관리할까", "부위 보기", "aging-map.html", 86, 20),
    ("03 Tech", "5초 스탬핑샷", "한 칸에 5초", "기술 보기", "technology.html", 14, 74),
    ("04 Clinic", "17년의 클리닉 경험", "클리닉 노하우를 집으로", "스토리 보기", "greeting.html", 86, 74),
]   # 수정요청 261030 문구

PRODUCTS = [  # (분류, 이름, 설명, 이미지, 링크, 마우스를 올리면 보이는 같은 제품의 다른 컷)
    ("Device", "TechFit", "5초 스탬핑 고주파 디바이스", "p-techfit.jpg", "products.html", "n-techfit-stand.jpg"),
    ("Device", "CLB", "고주파 마사지기", "p-clb.jpg", "products.html", "e-clb-v.jpg"),
    ("Cosmetic", "Collagen Booster Gel", "콜라겐 부스터 젤", "p-gel.jpg", "products.html#cosmetics", "e-gel-blue-v.jpg"),
    ("Cosmetic", "Grid Mask", "그리드 마스크", "p-mask.jpg", "products.html#cosmetics", "s-mask-glass.jpg"),
    ("Cosmetic", "Toning Serum", "라이트 토닝 세럼", "p-serum.jpg", "products.html#cosmetics", "e-serum-warm-v.jpg"),
    ("Accessory", "Firenze Bag", "케어클 피렌체 백 · 디바이스 전용 가죽 케이스", "p-case.jpg", "products.html", "c-techfit-case.jpg"),
]

STEPS = [  # (EN, 한글, 설명, 모바일용 사진) — 수정요청 261030 문구
    ("Notice", "알아차림", "어느 날, 거울 속 얼굴이 낯설어집니다.", "p-gel.jpg"),
    ("Read", "나의 노화 타입", "6가지 중, 내가 나이 드는 방식을 찾습니다.", "s-mask-glass.jpg"),
    ("Map", "시작된 자리", "노화가 시작된 자리를 22개 부위에서 짚습니다.", "p-techfit.jpg"),
    ("Care", "맞춤 케어", "내 타입에 맞는 방법으로 관리합니다.", "p-serum.jpg"),
    ("Check", "다시 읽기", "다시 읽으면, 변화가 보입니다.", "n-lineup-sq.jpg"),
]

# 물방울 속에 띄울 누끼 제품 (tools: 흰 배경 제품컷 → 투명 PNG). 순서는 STEPS와 같다
STEP_CUTS = ["cut-gel.png", "cut-mask.png", "cut-device.png", "cut-serum.png", "cut-case.png"]
STEP_FINAL_CUT = "cut-fullset.webp"   # 마지막 단계 뒤 가운데 큰 물방울 속

CONTACTS = [
    ("Global Business", "해외 사업", "수출 · 해외 유통 문의<br>support@carecl.co.kr", "contact.html#global"),
    ("Partnership", "유통 · 제휴", "총판 및 제휴 제안<br>support@carecl.co.kr", "contact.html#partnership"),
    ("Media / PR", "미디어", "취재 · 광고 · 협찬<br>support@carecl.co.kr", "contact.html#press"),
    ("General", "일반 문의", "제품 사용 · A/S<br>TEL +82 31-943-1028", "contact.html#inquiry"),
]


def hero_merge():
    """care CLINICAL LEVEL → careCL. C·L만 남기고 LINICAL과 EVEL이 동시에 끝 글자부터 하나씩 사라진 뒤 빈칸이 닫힌다.
    각 조각의 data-mg-at="시작,끝"은 스크롤 진행도(0~1) 구간 — stem.js heroMerge가 읽는다."""
    def word(txt):
        n, out = len(txt), []
        for j, ch in enumerate(txt):
            k = n - 1 - j                       # 끝 글자부터
            st = k / n * 0.62
            out.append(f'<span class="mg mg--drop" data-mg data-mg-at="{st:.3f},{st + 0.62 / n + 0.06:.3f}">{ch}</span>')
        return "".join(out)
    gap = '<span class="mg mg--drop" data-mg data-mg-at=".62,1">&nbsp;</span>'
    return ('<span class="mg mg--care">care</span>' + gap + '<span class="mg mg--cl">C</span>' + word("LINICAL")
            + gap + '<span class="mg mg--cl">L</span>' + word("EVEL"))


# 메인 물방울(네 가지 기준 로고 물방울 · 데일리 루틴 물방울) — False면 숨김(2026-10-20 사용자 요청).
# 숨김 중: 네 가지 기준은 가운데 careCL 로고만, 데일리 루틴은 단계별 사진(원형)이 글 옆에 지그재그. True로 바꾸면 그대로 복구.
MAIN_BUBBLES = False
# 네 가지 기준 가운데 — 사용자 제공 데모(carecl-bubble.html)의 투명 콜라겐 젤 방울 (js/gel.js)
MAIN_GEL = False
# 메인 물방울 — 사용자 제공 물방울구현.html(STEM식 엔진, 주황 빛) : 네 가지 기준 가운데 + 데일리 루틴 (js/stembubble.js)
MAIN_STEM_BUBBLE = True


# ── GRID 시안 메인 (2026-11-05 고객 수정요청: 쥬베룩 톤 — 세로선 그리드 · 둥근 이미지 카드 · 넓은 좌우 여백) ──
# 사진 카드 규격은 하나: 둥근 모서리 + 아주 옅은 그림자.
GSTEPS = [  # (번호, EN, 한글, 설명, 사진, 출발 높이 vh — 단계마다 다르게 내려온다)
    ("01", "Notice", "알아차림", "어느 날, 거울 속 얼굴이 낯설어집니다.", "g-step1.jpg", 120),
    ("02", "Read", "나의 노화 타입", "6가지 중, 내가 나이 드는 방식을 찾습니다.", "g-step2b.jpg", 80),
    ("03", "Map", "시작된 자리", "노화가 시작된 자리를 22개 부위에서 짚습니다.", "g-step5.jpg", 150),
    ("04", "Care", "맞춤 케어", "내 타입에 맞는 방법으로 관리합니다.", "g-step4.jpg", 95),
    ("05", "Check", "다시 읽기", "다시 읽으면, 변화가 보입니다.", "g-step5b.jpg", 135),
]

GWHY_IMG = ["g-why-types.jpg", "g-why-map.jpg", "g-why-stamp.jpg", "g-clinic-session.jpg"]   # CORE 순서

GLINEUP = [  # (분류, 이름, 설명, 누끼, 링크)
    ("Device", "TechFit", "5초 스탬핑 고주파 디바이스", "cut-device.png", "products.html"),
    ("Device", "CLB", "고주파 마사지기", "cut-clb.png", "products.html"),
    ("Cosmetic", "Collagen Booster Gel", "디바이스와 함께 쓰는 콜라겐 부스터 젤", "cut-gel.png", "products.html#cosmetics"),
    ("Cosmetic", "Grid Mask", "관리 부위를 안내하는 그리드 마스크", "cut-mask.png", "products.html#cosmetics"),
    ("Cosmetic", "Toning Serum", "디바이스 사용 전후에 쓰는 토닝 세럼", "cut-serum.png", "products.html#cosmetics"),
    ("Accessory", "Firenze Bag", "디바이스 전용 가죽 케이스", "cut-case.png", "products.html"),
]


def page_index():
    HERO_MERGE = hero_merge()
    steps = "\n".join(f"""        <li class="gstep" data-gstep style="--from:{fy}vh;--i:{i}">
          <figure class="gstep__img gcard"><img src="assets/img/{im}?v={VER}" alt="{kr}" loading="lazy"></figure>
          <div class="gstep__txt">
            <p class="gstep__head"><em>{no}</em> {en}</p>
            <b class="gstep__kr">{kr}</b>
            <p class="gstep__desc">{desc}</p>
          </div>
        </li>""" for i, (no, en, kr, desc, im, fy) in enumerate(GSTEPS))

    why_imgs = "\n".join(
        f'          <img class="gwhy__pic{" is-on" if i == 0 else ""}" data-why-pic src="assets/img/{im}?v={VER}" alt="" loading="lazy">'
        for i, im in enumerate(GWHY_IMG))
    why_items = "\n".join(f"""          <article class="gwhy__item{" is-on" if i == 0 else ""}" data-why>
            <figure class="gwhy__mpic gcard"><img src="assets/img/{GWHY_IMG[i]}?v={VER}" alt="" loading="lazy"></figure>
            <em class="glabel">{no}</em>
            <h3 class="gwhy__title">{t}</h3>
            <p class="gwhy__q">{q}</p>
            <a class="gpill" href="{h}">{lk}</a>
          </article>""" for i, (no, t, q, lk, h, *_) in enumerate(CORE))

    tiles = "\n".join(f"""          <a class="gtile" href="{h}" style="--i:{i}" draggable="false">
            <span class="gtile__no">{i + 1:02d}</span>
            <span class="gtile__img"><img src="assets/img/{cut}?v={VER}" alt="" loading="lazy" draggable="false"></span>
            <em class="gtile__tag">{tag}</em>
            <b class="gtile__name">{name}</b>
          </a>""" for i, (tag, name, desc, cut, h) in enumerate(GLINEUP))

    contact_links = "\n".join(f"""        <a class="gcc" href="{h}" style="--i:{i}">
          <em class="gcc__en">{en}</em>
          <b class="gcc__kr">{kr}</b>
          <p class="gcc__desc">{desc}</p>
          <i class="gcc__go" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i>
        </a>""" for i, (en, kr, desc, h) in enumerate(CONTACTS))

    body = f"""<main class="ghome">

  <!-- 01 메인 영상 (그대로) -->
  <section class="hero" aria-label="메인 영상">
    <img class="hero__poster" src="assets/img/main-film-poster.jpg?v={VER}" alt="">
    <video class="hero__video" poster="assets/img/main-film-poster.jpg?v={VER}"
           autoplay muted loop playsinline preload="metadata" aria-hidden="true">
      <source src="assets/video/main-film-m.mp4?v={VER}" media="(max-width: 767px)" type="video/mp4">
      <source src="assets/video/main-film.mp4?v={VER}" type="video/mp4">
    </video>
    <div class="hero__copy" data-merge>
      <h1 class="hero__title hero__title--merge" aria-label="care Clinical Level — careCL">{HERO_MERGE}</h1>
    </div>
  </section>

  <!-- 03 홈케어 5단계 — 사진이 세로선을 타고 내려와 한 줄로 맞춰진다 -->
  <section class="gsteps" data-gsteps aria-labelledby="gsteps-title">
    <div class="gsteps__pin">
      <div class="gsteps__lines" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div class="ghead">
        <span class="gsteps__logo" aria-hidden="true">{LOGO}</span>
        <h2 class="ghead__big" id="gsteps-title" aria-label="careCL 5 STEPS">5 STEPS</h2>
        <p class="ghead__kr">내 노화 타입에 맞춘 홈케어 5단계</p>
      </div>
      <ol class="gsteps__row">
{steps}
      </ol>
    </div>
  </section>

  <!-- 04 네 가지 기준 — 왼쪽 큰 사진 카드(멈춤) + 오른쪽 글 -->
  <section class="gwhy" data-gwhy aria-labelledby="gwhy-title">
    <div class="gwrap">
      <div class="ghead">
        <p class="glabel">How careCL Works</p>
        <h2 class="ghead__title" id="gwhy-title">케어클의 <span class="gacc">네 가지 기준</span></h2>
      </div>
      <div class="gwhy__grid">
        <div class="gwhy__media gcard" aria-hidden="true">
{why_imgs}
        </div>
        <div class="gwhy__list">
{why_items}
        </div>
      </div>
      <div class="core__cta">
        <a class="gpill gpill--solid" href="survey.html">AI 피부 진단 시작하기</a>
      </div>
    </div>
  </section>

  <!-- 05 라인업 — 좌우로 넘기는 제품 카드 (끌기 · 화살표 · 진행 막대) -->
  <section class="gline" data-gline aria-labelledby="gline-title">
    <div class="gwrap gline__head">
      <div>
        <p class="glabel">careCL Lineup</p>
        <h2 class="ghead__title" id="gline-title">진단 결과에 맞춰 <span class="gacc">조합하는 제품</span></h2>
      </div>
      <div class="gline__btns">
        <button type="button" class="gline__nav" data-line-prev aria-label="이전 제품"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button type="button" class="gline__nav" data-line-next aria-label="다음 제품"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
    </div>
    <div class="gline__slider" data-line-slider>
      <div class="gline__track" data-gtiles>
{tiles}
      </div>
    </div>
    <div class="gwrap"><div class="gline__bar" aria-hidden="true"><i data-line-bar></i></div></div>
  </section>

  <!-- 06 공식몰 — 알약 모양 창이 열리듯 사진이 펼쳐지고, 다 열리면 글이 한 줄씩 올라온다 -->
  <section class="gshop" data-gshop aria-labelledby="gshop-title">
    <div class="gshop__pin">
      <div class="gwrap">
        <div class="gshop__card" data-gshop-card>
          <img src="assets/img/m-model-set.jpg?v={VER}" alt="TechFit 풀세트와 디바이스를 든 모델" data-gshop-img>
          <div class="gshop__copy">
            <h2 id="gshop-title"><span>Shop the</span> <span>Official Store</span></h2>
            <p><span>진단 결과에 맞는 구성으로 담아 보세요.</span></p>
            <a class="gpill gpill--light" href="{SHOP_HREF}">Shop 바로가기</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 07 문의 — 한 줄로 (해외·유통·미디어는 아래 작은 링크로) -->
  <section class="gcontact" aria-labelledby="gcontact-title">
    <div class="gwrap">
      <h2 class="ghead__big ghead__big--ink" id="gcontact-title">Contact us</h2>
      <p class="ghead__kr">careCL — 정밀하게 읽고, 부위별로 되돌리다</p>
      <a class="gpill" href="contact.html">문의하기</a>
      <nav class="gcontact__cards" aria-label="문의 종류">
{contact_links}
      </nav>
    </div>
  </section>

</main>
"""
    return (head("careCL 케어클 — 정밀하게 읽고, 부위별로 되돌리다",
                 "얼굴을 22개 부위로 나누어 읽고, 먼저 관리해야 할 곳부터 제안하는 홈 에이징 케어",
                 css=("css/grid-home.css",))
            + loader() + header() + body + FOOTER + tail(three=False, js=("js/grid-home.js",)))


# ── 메인 v2 (2026-11-26 회의 화이트보드 구조) — 기존 index.html은 그대로 두고 main-v2.html로 따로 만든다 ──
# 순서: 영상+바로가기 → 5 STEPS(6 type 자리, 기존 섹션 그대로) → 22개 부위 → 5초 스탬핑 → 진단지 샘플 → 진단별 제품 → 특허·수출 → 푸터
# (고객 댓글 Top5는 사용자 요청으로 뺌)
V2_BAR = [  # 영상 아래 바로가기
    ("AI Skin Test", "AI 피부 진단 시작하기", "survey.html", True),
    ("6 Aging Types", "6가지 노화 타입", "aging-types.html", False),
    ("Aging Map 22", "22개 관리 부위", "aging-map.html", False),
    ("Products", "제품 보기", "products.html", False),
]
V2_MAP = [  # content/aging-map.html 원고
    ("6 × 22", "같은 부위라도 타입에 따라 관리가 달라집니다", "6가지 유형과 22개 부위를 교차해 개인별 관리 순서를 도출합니다."),
    ("22", "얼굴 22개 좌표", "얼굴과 목 · 바디를 22개 좌표로 나누어 관리 부위를 정의합니다."),
    ("01 →", "먼저 관리할 곳부터 순서대로 제안합니다", "진단 결과에 따라 우선 관리 부위와 케어 순서를 안내합니다."),
]
V2_PATENTS = [  # content/rnd.html 원고
    ("RF 스탬핑", "제10-2938674호", "피부 접촉에 따른 전압 증폭 및 반복 출력 제어를 이용한 고주파 스탬핑 피부 미용 방법"),
    ("HIFU · RF 복합", "제10-2799588호 / 제10-2799593호", ""),
    ("전달 기술", "제10-1647183호", "치료약물 및 세포전달용 마이크로입자 및 이의 제조방법"),
]
V2_EXPORT = [  # 발표자료_v2 16·19쪽: 수출신고필증(홍콩·호주·캐나다), 두바이·이집트 2년 독점 계약
    ("HK", "홍콩", "Hong Kong", "수출"),
    ("AU", "호주", "Australia", "수출"),
    ("CA", "캐나다", "Canada", "수출"),
    ("AE", "두바이", "Dubai", "독점 계약"),
    ("EG", "이집트", "Egypt", "독점 계약"),
]


# Aging Map 22 좌표 — 자료/AI Agent 구성용 Contents 원본 - 0730.xlsx 'Face MAP' 탭 (이름만). 점 위치는 t-face-clean.jpg(1672×941, 원본 = 글자다날린이미지.png) 위에서 잰 %.
# 바디(B1~B5)는 얼굴 사진 밖이라 탭에서 뺌
V2_ZONES = [
    ("upper", "Upper", "상안부", [("U1", "이마", 49.0, 20.2), ("U2", "미간", 45.5, 33.5), ("U3", "눈썹", 50.2, 29.2), ("U4", "눈가", 54.5, 35.7),
                              ("U5", "눈밑", 50.5, 38.9), ("U6", "눈꺼풀", 50.4, 32.7), ("U7", "관자놀이", 58.1, 30.8)]),
    ("mid", "Mid", "중안부", [("M1", "앞광대", 54.4, 43.6), ("M2", "심부볼", 56.2, 55.5), ("M3", "팔자", 51.8, 52.7), ("M4", "옆볼", 60.5, 52.1)]),
    ("lower", "Lower", "하안부", [("L1", "인중·윗입술", 47.2, 52.7), ("L2", "마리오네트", 52.2, 61.2), ("L3", "턱", 49.0, 67.6),
                              ("L4", "턱선", 57.5, 62.9), ("L5", "귀뒤", 65.8, 44.6), ("L6", "이중턱", 52.2, 72.5)]),
]


# PC에서 Upper/Mid/Lower 글자 줄의 높이 — 사진 속 얼굴 높이(눈 아래 · 입 위 · 턱 끝, t-face-clean.jpg 기준 %)
V2_ZONE_Y = {"upper": 42.8, "mid": 55.2, "lower": 68.6}   # 사용자 기준 이미지(1672×941) 선 높이 403 · 519 · 646px


def v2_report_sample():
    """진단지 샘플 — js/report-data.js의 잔주름형(fine) 원고로 그린다. 점수는 없이 모양만(예시)."""
    import json
    raw = read("js/report-data.js")
    data = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    d = data["fine"]
    # 오각형: 잔주름 · 변형처짐 · 근육 · 피로 · 초기노화 (설문 5유형) — 예시 모양
    import math
    axes = ["잔주름", "변형처짐", "근육", "피로", "초기노화"]
    shape = [.92, .38, .46, .62, .3]
    cx = cy = 120; R = 92
    def pt(i, r):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        return cx + R * r * math.cos(a), cy + R * r * math.sin(a)
    grid = "".join(f'<polygon class="rd__grid" points="{" ".join("%.1f,%.1f" % pt(i, k) for i in range(5))}"/>' for k in (1, .66, .33))
    spokes = "".join('<line class="rd__grid" x1="%d" y1="%d" x2="%.1f" y2="%.1f"/>' % ((cx, cy) + pt(i, 1)) for i in range(5))
    poly = '<polygon class="rd__val" points="' + " ".join("%.1f,%.1f" % pt(i, v) for i, v in enumerate(shape)) + '"/>'
    labels = "".join('<text x="%.1f" y="%.1f"%s>%s</text>' % (pt(i, 1.24) + (' class="is-main"' if i == 0 else "", t))
                     for i, t in enumerate(axes))
    radar = f'<svg class="rd__radar" viewBox="-30 -20 300 280" aria-hidden="true">{grid}{spokes}{poly}{labels}</svg>'

    shots = d["shots"]
    freq = d["frequency"].split("·")[0].strip()
    modes = []
    for x in shots:
        if x["mode"] not in modes: modes.append(x["mode"])
    shot_rows = "\n".join(f"""                <tr><td class="rd__code">{x['code']}</td><td>{x['name']}</td><td>{x['mode']}</td><td>{x['dir']}</td><td class="rd__num">{x['count']}</td></tr>""" for x in shots)
    evid = "".join(f"<li>{e}</li>" for e in d["evidence"])
    ingr = " · ".join(d["ingredients"])
    areas = " · ".join(a["name"] for a in d["areas"])
    return f"""        <article class="rd" data-v2-in aria-label="AI 피부 진단 리포트 예시">
          <header class="rd__head">
            <div class="rd__brand"><b class="lf">careCL</b><span>AI Skin Diagnosis Report</span></div>
            <dl class="rd__meta">
              <div><dt>No.</dt><dd>2611-0000</dd></div>
              <div><dt>Date</dt><dd>2026.11.26</dd></div>
              <div><dt>Method</dt><dd>Aging Map 22 · 18 Q</dd></div>
            </dl>
          </header>
          <p class="rd__sample">SAMPLE · 예시 리포트</p>
          <section class="rd__sec rd__sec--result">
            <h4 class="rd__h"><em>01</em>진단 결과</h4>
            <div class="rd__split">
              <table class="rd__tbl rd__tbl--kv">
                <tbody>
                  <tr><th>대표 유형</th><td><b class="rd__type">잔주름형</b><span class="rd__en">Fine Wrinkle Type</span></td></tr>
                  <tr><th>주요 신호</th><td><ul class="rd__chips">{evid}</ul></td></tr>
                  <tr><th>집중 관리 부위</th><td><b>{len(d['areas'])}곳</b> <span class="rd__sub">{areas}</span></td></tr>
                  <tr><th>권장 SHOT</th><td><b>{d['shotTotal']}샷</b> <span class="rd__sub">{' · '.join(modes)}</span></td></tr>
                  <tr><th>권장 빈도</th><td><b>{freq}</b></td></tr>
                </tbody>
              </table>
              <figure class="rd__fig">{radar}<figcaption>Fig. 1 &nbsp;5가지 노화 신호 분포</figcaption></figure>
            </div>
          </section>
          <section class="rd__sec">
            <h4 class="rd__h"><em>02</em>부위별 관리 계획 <small>Aging Map 22</small></h4>
            <table class="rd__tbl rd__tbl--grid">
              <thead><tr><th>좌표</th><th>부위</th><th>모드</th><th>방향</th><th class="rd__num">SHOT</th></tr></thead>
              <tbody>
{shot_rows}
              </tbody>
              <tfoot><tr><td colspan="4">합계</td><td class="rd__num">{d['shotTotal']}</td></tr></tfoot>
            </table>
            <p class="rd__line"><span>추천 성분</span>{ingr}</p>
          </section>
          <footer class="rd__foot">
            <p>본 리포트는 설문 응답을 바탕으로 한 홈케어 참고 자료이며, 의료 진단을 대신하지 않습니다.</p>
            <div class="rd__seal" aria-hidden="true"><span>careCL</span><small>AGING LAB</small></div>
          </footer>
        </article>"""


def page_index2():
    bar = "\n".join(f"""      <a class="v2bar__item{' v2bar__item--main' if main else ''}" href="{h}">
        <em>{en}</em><b>{kr}</b>
        <i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i>
      </a>""" for en, kr, h, main in V2_BAR)
    steps = "\n".join(f"""        <li class="gstep" data-gstep style="--from:{fy}vh;--i:{i}">
          <figure class="gstep__img gcard"><img src="assets/img/{im}?v={VER}" alt="{kr}" loading="lazy"></figure>
          <div class="gstep__txt">
            <p class="gstep__head"><em>{no}</em> {en}</p>
            <b class="gstep__kr">{kr}</b>
            <p class="gstep__desc">{desc}</p>
          </div>
        </li>""" for i, (no, en, kr, desc, im, fy) in enumerate(GSTEPS))
    zone_tabs = "\n".join(f"""          <button type="button" class="v2zm__tab{' is-on' if i == 0 else ''}" role="tab" aria-selected="{'true' if i == 0 else 'false'}" data-zone="{k}" style="--y:{V2_ZONE_Y[k]}%">
            <b>{en}</b><span>{kr}</span><i>{len(z):02d}</i>
          </button>""" for i, (k, en, kr, z) in enumerate(V2_ZONES))
    zone_dots = "\n".join(f"""            <i class="v2zm__dot" data-zone="{k}" style="left:{x}%;top:{y}%;--d:{j}"><em>{c}</em></i>"""
                          for k, en, kr, z in V2_ZONES for j, (c, n, x, y) in enumerate(z))
    zone_lists = "\n".join(f"""          <ol class="v2zm__ol{' is-on' if i == 0 else ''}" data-zone="{k}" aria-label="{en} {kr} 부위">
""" + "\n".join(f"""            <li style="--d:{j}"><code>{c}</code>{n}</li>""" for j, (c, n, x, y) in enumerate(z)) + """
          </ol>""" for i, (k, en, kr, z) in enumerate(V2_ZONES))
    map_rows = "\n".join(f"""          <li class="v2map__row" data-v2-in style="--i:{i}">
            <span class="v2map__no">{no}</span>
            <div><b>{t}</b><p>{p}</p></div>
          </li>""" for i, (no, t, p) in enumerate(V2_MAP))
    tiles = "\n".join(f"""          <a class="gtile" href="{h}" style="--i:{i}" draggable="false">
            <span class="gtile__no">{i + 1:02d}</span>
            <span class="gtile__img"><img src="assets/img/{cut}?v={VER}" alt="" loading="lazy" draggable="false"></span>
            <em class="gtile__tag">{tag}</em>
            <b class="gtile__name">{name}</b>
          </a>""" for i, (tag, name, desc, cut, h) in enumerate(GLINEUP))
    patents = "\n".join(f"""            <li><em>{k}</em><b>{no}</b>{f"<p>{t}</p>" if t else ""}</li>""" for k, no, t in V2_PATENTS)
    def _gl(st, label, en):
        cs = [(c, kr, e) for c, kr, e, t in V2_EXPORT if t == st]
        li = "".join(f'<li><img src="assets/img/flags/{c.lower()}.svg" alt="" width="56" height="42"><b>{kr}</b><em>{e}</em></li>' for c, kr, e in cs)
        return f'<div class="v2gl__grp{" v2gl__grp--deal" if st != "수출" else ""}"><p class="v2gl__h"><span>{label}</span><b>{len(cs)}</b><em>{en}</em></p><ul class="v2gl__list" style="--n:{len(cs)}">{li}</ul></div>'
    exports = _gl("수출", "수출", "Export") + _gl("독점 계약", "독점 계약", "Exclusive")

    body = f"""<main class="ghome ghome--v2">

  <!-- 01 메인 영상 + 바로가기 (영상을 끝까지 보지 않아도 이동) -->
  <section class="hero hero--v2" aria-label="메인 영상">
    <img class="hero__poster" src="assets/img/main-film-poster.jpg?v={VER}" alt="">
    <video class="hero__video" poster="assets/img/main-film-poster.jpg?v={VER}"
           autoplay muted loop playsinline preload="metadata" aria-hidden="true">
      <source src="assets/video/main-film-m.mp4?v={VER}" media="(max-width: 767px)" type="video/mp4">
      <source src="assets/video/main-film.mp4?v={VER}" type="video/mp4">
    </video>
    <nav class="v2bar" aria-label="바로가기">
      <div class="v2bar__in">
{bar}
      </div>
    </nav>
  </section>

  <!-- 02 5 STEPS (6 type 자리 — 기존 섹션 그대로) -->
  <section class="gsteps" data-gsteps aria-labelledby="gsteps-title">
    <div class="gsteps__pin">
      <div class="gsteps__lines" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div class="ghead">
        <span class="gsteps__logo" aria-hidden="true">{LOGO}</span>
        <h2 class="ghead__big" id="gsteps-title" aria-label="careCL 5 STEPS">5 STEPS</h2>
        <p class="ghead__kr">내 노화 타입에 맞춘 홈케어 5단계</p>
      </div>
      <ol class="gsteps__row">
{steps}
      </ol>
    </div>
  </section>

  <!-- 03 22개 부위 — Upper/Mid/Lower를 고르면 사진 위 해당 점이 켜지고 오른쪽에 부위 목록 -->
  <section class="v2map" data-v2map aria-labelledby="v2map-title">
    <div class="gwrap">
      <div class="v2map__head">
        <p class="glabel">Aging Map 22</p>
        <h2 class="ghead__title" id="v2map-title">노화는 얼굴 전체가 아니라<br><span class="gacc">특정 부위</span>에서 시작됩니다</h2>
        <p class="v2map__lead">6 Aging Types가 어떤 노화인가를 말한다면, Aging Map 22는 어디를 먼저 관리할 것인가를 말합니다.</p>
      </div>
      <div class="v2zm">
        <figure class="v2zm__img gcard">
          <div class="v2zm__stage">
            <img src="assets/img/t-face-clean.jpg?v={VER}" alt="Aging Map 22 대표 모델" loading="lazy">
            <div class="v2zm__dots" aria-hidden="true">
{zone_dots}
            </div>
          </div>
        </figure>
        <div class="v2zm__tabs" role="tablist" aria-label="얼굴 구역">
{zone_tabs}
        </div>
        <div class="v2zm__list">
{zone_lists}
        </div>
      </div>
      <div class="v2map__more"><a class="gpill" href="aging-map.html">Aging Map 22 자세히 보기</a></div>
    </div>
  </section>

  <!-- 04 5초 스탬핑 — 영상: 케어클 유튜브 eFbtW7kB00E → assets/video/stamping.mp4 (H.264 1280) -->
  <section class="v2stamp" aria-labelledby="v2stamp-title">
    <div class="gwrap">
    <div class="v2stamp__block" data-v2-in>
      <div class="v2stamp__cap">
        <p class="v2stamp__k"><i></i>Core Technology</p>
        <h2 id="v2stamp-title" class="v2stamp__title"><span class="v2stamp__num">5</span><span class="v2stamp__unit">sec</span><span class="v2stamp__name">Stamping<br>Shot</span></h2>
        <p class="v2stamp__lead">피부에 닿는 순간을 감지해 출력을 조절하고, 한 자리에 5초간 머무르며 반복 전달합니다.</p>
        <ol class="v2stamp__steps">
          <li><b>01</b><span>닿는 순간 감지</span></li>
          <li><b>02</b><span>출력 조절</span></li>
          <li><b>03</b><span>5초간 반복 전달</span></li>
        </ol>
      </div>
      <figure class="v2stamp__media">
        <video class="v2stamp__video" poster="assets/img/v2-stamping-poster.jpg?v={VER}" muted loop playsinline autoplay preload="metadata" aria-label="케어클 스탬핑 메커니즘 설명 영상">
          <source src="assets/video/stamping.mp4?v={VER}" type="video/mp4">
        </video>
        <button class="v2stamp__snd" type="button" aria-pressed="false" aria-label="소리 켜기"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path class="on" d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/><path class="off" d="M16 9l6 6M22 9l-6 6"/></svg><span>소리</span></button>
      </figure>
    </div>
    </div>
  </section>

  <!-- 05 진단지 샘플 → 설문 진단 -->
  <section class="v2report" aria-labelledby="v2report-title">
    <div class="gwrap">
      <div class="ghead">
        <p class="glabel">AI Skin Report</p>
        <h2 class="ghead__title" id="v2report-title">진단이 끝나면 <span class="gacc">리포트로 받아봅니다</span></h2>
        <p class="ghead__kr">노화 유형, 먼저 관리할 부위, 부위별 샷 수까지 한 장으로 정리합니다.</p>
      </div>
      <div class="rdclip">
{v2_report_sample()}
        <div class="rdclip__more">
          <p>전체 리포트는 진단을 마치면 바로 받아볼 수 있어요</p>
          <a class="rdclip__btn" href="{{V2_AI_HREF}}">AI 피부 진단 바로가기<i aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></i></a>
        </div>
      </div>
    </div>
  </section>

  <!-- 06 진단별 제품 -->
  <section class="gline" data-gline aria-labelledby="gline-title">
    <div class="gwrap gline__head">
      <div>
        <p class="glabel">careCL Lineup</p>
        <h2 class="ghead__title" id="gline-title">진단 결과에 맞춰 <span class="gacc">조합하는 제품</span></h2>
      </div>
      <div class="gline__btns">
        <button type="button" class="gline__nav" data-line-prev aria-label="이전 제품"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
        <button type="button" class="gline__nav" data-line-next aria-label="다음 제품"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
      </div>
    </div>
    <div class="gline__slider" data-line-slider>
      <div class="gline__track" data-gtiles>
{tiles}
      </div>
    </div>
    <div class="gwrap"><div class="gline__bar" aria-hidden="true"><i data-line-bar></i></div></div>
  </section>

  <!-- 07 특허 기술 + 수출 국가 — 위쪽 색 띠에 제목, 그 아래 [사진|글] · [글|사진] 두 줄 (2026-11-26 레퍼런스) -->
  <section class="v2trust" aria-labelledby="v2trust-title">
    <div class="v2trust__band">
      <div class="gwrap">
        <p class="glabel glabel--light">Patent &amp; Global</p>
        <h2 class="v2trust__title" id="v2trust-title">직접 연구한 기술로, <b>해외 시장</b>에 갑니다</h2>
      </div>
    </div>
    <div class="gwrap v2trust__rows">
      <article class="v2row" data-v2-in>
        <figure class="v2row__img"><img src="assets/img/v2-patents.jpg?v={VER}" alt="케어클 등록특허 특허증 4장" loading="lazy"></figure>
        <div class="v2row__txt">
          <p class="v2row__k">Patent</p>
          <h3 class="v2row__t">등록특허 <b>4</b>건</h3>
          <p class="v2row__lead">피부에 닿는 방식부터 에너지를 전달하는 방식까지, 홈케어 기기의 핵심 기술을 직접 연구합니다.</p>
          <ul class="v2pat">
{patents}
          </ul>
          <a class="v2row__more" href="rnd.html">연구개발 · 특허 보기<i aria-hidden="true">→</i></a>
        </div>
      </article>
      <article class="v2row v2row--rev" data-v2-in>
        <figure class="v2row__img v2row__img--map"><img src="assets/img/v2-export-map.jpg?v={VER}" alt="수출 · 독점 계약 국가를 표시한 세계지도: 캐나다, 이집트, 두바이, 홍콩, 호주" loading="lazy"></figure>
        <div class="v2row__txt">
          <p class="v2row__k">Global</p>
          <h3 class="v2row__t">수출 · 독점 계약 <b>5</b>개국</h3>
          <div class="v2gl">{exports}</div>
          <a class="v2row__more" href="contact.html#global">해외 사업 문의<i aria-hidden="true">→</i></a>
        </div>
      </article>
    </div>
  </section>

</main>
"""
    return (head("careCL 케어클 — 메인 v2",
                 "얼굴을 22개 부위로 나누어 읽고, 먼저 관리해야 할 곳부터 제안하는 홈 에이징 케어",
                 css=("css/grid-home.css", "css/grid-home2.css"))
            .replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
            + loader() + header() + body + FOOTER + tail(three=False, js=("js/grid-home.js", "js/grid-home2.js"))
            # 진단이 비공개인 동안 시안(noindex) 페이지에서만 비밀 주소로 연결 — 공개되면 survey.html
            ).replace("{V2_AI_HREF}", "survey.html" if AI_TEST_PUBLIC else AI_SECRET + "-survey-c.html")


PAGES = {"index.html": page_index, "main-v2.html": page_index2}

# ═══════════════════════════════════════════════════════════
#  서브 페이지 (14개) — 본문은 content/<파일>.html (기존 사이트 원고)
# ═══════════════════════════════════════════════════════════
# (1뎁스 EN, LED 색, [(2뎁스 EN, 파일, 한글)])
MENU = [
    ("Company", "purple", [("About careCL", "about.html", "회사 소개"),
                           ("Our Story", "greeting.html", "브랜드 스토리"),
                           ("R&D / Patent", "rnd.html", "연구개발 · 특허"),
                           ("Awards & Certification", "certification.html", "수상 · 인증"),
                           ("Contact", "contact.html", "문의")]),
    ("Aging Lab", "green", [("6 Aging Types", "aging-types.html", "6가지 노화 타입"),
                            ("Aging Map 22", "aging-map.html", "22개 관리 부위")]),
    ("Technology", "red", [("careCL Technology", "technology.html", "TECH FIT 기술"),
                           ("Product", "products.html", "디바이스 · 코스메틱")]),
]
# 머리말 제목 줄바꿈 (탭 이름은 그대로 한 줄)
TITLE_BREAK = {}   # GRID 시안: 상세페이지 제목은 모두 한 줄

# 메뉴별 머리말 오른쪽 이미지 (회사 소개는 오렌지 C, 문의는 없음)
HEAD_VISUAL = {"Company": ("C", "letter"),
               "products.html": ("h-package.jpg", "photo photo--pkg"),   # 제품 탭은 Technology 밑이지만 머리말은 패키지 사진
               "Technology": ("h-techfit-lit.webp", "cut cut--tall"),
               "Aging Lab": ("h-model.jpg", "photo")}
GROUP_HREF = {"Company": "about.html", "Aging Lab": "aging-types.html", "Technology": "technology.html",
              "Products": "products.html", "Contact": "contact.html"}

# 기존 사진 → 새 사진 (사람 모델이 나온 사진은 제품·정물 컷으로)
IMG_MAP = {
    "cc-model-c.jpg": "c-beam.jpg",
    "p-leaning.jpg": "c-techfit-case.jpg",
    "p-skin.jpg": "c-gel-silk.jpg",
    "p-eye.jpg": "n-techfit-side.jpg",
    "cc-stamping-c.jpg": "n-techfit-stand.jpg",
    "p-mask-close.jpg": "s-mask-glass.jpg",
    "p-devices.jpg": "c-overhead.jpg",
    "p-cheek.jpg": "c-techfit-case.jpg",
    "p-mask-face.jpg": "n-mask-packs.jpg",
    "p-mask-hands.jpg": "n-mask-glass-wide.jpg",
    "product-techfit.jpg": "p-techfit.jpg",
    "product-clb.png": "p-clb.jpg",
    "product-gel.png": "p-gel.jpg",
    "product-mask.jpg": "p-mask.jpg",
    "product-serum.jpg": "p-serum.jpg",
}


def sub_page(group, led, items, idx):
    title_en, slug, title_kr = items[idx]
    body = read("content/" + slug)

    def img(m):
        src = m.group(1)
        name = src.split("/")[-1].split("?")[0]
        if "/doc/" in src:
            return 'src="assets/img/doc/' + name + '"'
        return 'src="assets/img/' + IMG_MAP.get(name, name) + '"'
    body = re.sub(r'src="(assets/img/[^"]+)"', img, body)
    # 섹션마다 LED 색 지정
    body = body.replace('<div class="qcard rv">', '<div class="qcard rv"><span class="qcard__logo" aria-hidden="true">' + LOGO + '</span>')   # 문구 카드 뒤 큰 로고
    body = re.sub(r'<section class="(sec|figbreak|dp)', lambda m: '<section data-led="' + led + '" class="' + m.group(1), body)
    # 회사 소개의 파티클 캔버스 → 9구 LED 헤드
    body = re.sub(r'<div class="about__visual ceo__visual" id="brandParticles">.*?</div></div>',
                  '<div class="about__visual"><div class="led9 about__led" data-led9><canvas></canvas></div>'
                  '<span class="about__tag">Ageless Beauty</span></div>', body, flags=re.S)
    # 지도 자리 → 구글 지도 (주소 그대로 검색)
    body = re.sub(r'<div class="map( rv)?">.*?</div>',
                  lambda m: '<div class="map' + (m.group(1) or '') + '"><iframe title="케어클 위치 — 경기도 고양시 일산동구 동국로 32" loading="lazy" '
                  'referrerpolicy="no-referrer-when-downgrade" '
                  'src="https://www.google.com/maps?q=%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EA%B3%A0%EC%96%91%EC%8B%9C%20%EC%9D%BC%EC%82%B0%EB%8F%99%EA%B5%AC%20%EB%8F%99%EA%B5%AD%EB%A1%9C%2032&output=embed"></iframe></div>',
                  body, count=1, flags=re.S)

    tabs = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == slug else ""}>{t}</a>' for t, h, _ in items)
    vis = HEAD_VISUAL.get(slug) or HEAD_VISUAL.get(group)
    if vis and vis[0] == "C":
        # 회사 소개 — 화면 오른쪽에 잘려 보이는 크고 두꺼운 오렌지 C
        vis_html = ('<div class="subhead__vis subhead__vis--letter" aria-hidden="true">'
                    '<svg viewBox="0 0 1000 1000"><path d="M 768 259 A 360 360 0 1 0 768 741" '
                    'fill="none" stroke="currentColor" stroke-width="200" stroke-linecap="round"/></svg></div>')
    else:
        vis_html = (f'<div class="subhead__vis subhead__vis--{vis[1]}" aria-hidden="true">'
                    f'<img src="assets/img/{vis[0]}?v={VER}" alt="" decoding="async"></div>') if vis else ""
    head_html = f"""<main class="sub">
  <section class="subhead{' subhead--vis' if vis else ''} subhead--{group.lower().replace(' ', '-')}" data-led="{led}">
    <div class="subhead__top">
      {vis_html}
      <div class="wrap">
        <p class="label">{group}</p>
        <h1 class="subhead__title">{TITLE_BREAK.get(title_en, title_en)}</h1>
      </div>
    </div>
    <nav class="subtabs" aria-label="{group} 하위 메뉴"><div class="wrap subtabs__in">{tabs}</div></nav>
  </section>
  <div class="sub-body">
{body}
  </div>
</main>
"""
    return (head(f"{title_kr} | careCL 케어클", f"careCL {title_kr}", sub=True, css=("css/detail.css", "css/grid-sub.css"))
            + header(GROUP_HREF[group]) + head_html + FOOTER + tail(three=False))


for _g, _led, _items in MENU:
    for _i, (_, _slug, _) in enumerate(_items):
        PAGES[_slug] = (lambda g=_g, l=_led, it=_items, i=_i: sub_page(g, l, it, i))

# 문의 4개 페이지는 Company > Contact 한 페이지로 (GRID 시안 261105) — 예전 주소는 그 자리로
for _old, _id in (("partnership.html", "partnership"), ("press.html", "press"), ("inquiry.html", "inquiry")):
    PAGES[_old] = (lambda o=_old, i=_id: '<!doctype html><meta charset="utf-8"><title>Contact</title>'
                   f'<meta http-equiv="refresh" content="0;url=contact.html#{i}">'
                   f'<link rel="canonical" href="contact.html"><a href="contact.html#{i}">Contact</a>')

# 코스메틱은 Product 페이지 안으로 (261102) — 예전 주소는 그 자리로
PAGES["cosmetics.html"] = lambda: ('<!doctype html><meta charset="utf-8"><title>Product</title>'
                                   '<meta http-equiv="refresh" content="0;url=products.html#cosmetics">'
                                   '<link rel="canonical" href="products.html"><a href="products.html#cosmetics">Product</a>')
# 예전 careCL Technology 주소 → 하나로 합친 Technology 페이지로 (261030)
PAGES["carecl-technology.html"] = lambda: ('<!doctype html><meta charset="utf-8"><title>careCL Technology</title>'
                                           '<meta http-equiv="refresh" content="0;url=technology.html">'
                                           '<link rel="canonical" href="technology.html"><a href="technology.html">Technology</a>')



# ═══════════════════════════════════════════════════════════
#  AI 피부 진단 설문 · 결과 리포트
# ═══════════════════════════════════════════════════════════
def page_survey():
    body = """<script>if(/[?&]embed=1/.test(location.search))document.documentElement.classList.add('is-embed')</script>
<main class="sv sv--stem" data-led="red">
  <aside class="sv__panel">
    <div class="sv__dots" data-dotfield></div>
    <div class="sv__stick">
      <div class="sv__lock">
        <em>AI Skin Agent</em>
        <b>Aging Map 22</b>
        <p>얼굴을 22개 좌표로 나누어<br>당신의 노화 타입을 진단합니다</p>
      </div>
      <!-- 왼쪽 그래픽 자리 (임시: 살아 움직이는 구체 — 새 AI 진단 그래픽으로 바꿀 예정) -->
      <div class="sv__orbwrap"><div class="sv__orb" data-orb aria-hidden="true"><canvas></canvas></div></div>
    </div>
  </aside>
  <section class="sv__body"><div class="sv__form" id="svForm"></div></section>
</main>
"""
    return (head("노화 타입 진단 | Aging Map 22 — careCL 케어클", "2분 설문으로 나의 노화 타입과 먼저 관리할 부위를 확인하세요",
                 css=("css/bridge.css", "css/survey.css", "css/checkup-result.css", "css/report.css"), body_cls="survey")
            + header("aging-types.html") + body + FOOTER
            + tail(three=False, js=("js/report-data.js", "js/report.js", "js/radar.js", "js/survey.js", "js/orb.js"), fab=False))


def page_report():
    body = """<script>if(/[?&]embed=1/.test(location.search))document.documentElement.classList.add('is-embed')</script>
<main class="sub">
  <section class="subhead" data-led="purple">
    <div class="wrap">
      <p class="label">Aging Lab</p>
      <h1 class="subhead__title">Aging Report</h1>
      <p class="subhead__kr">진단 결과 리포트</p>
    </div>
  </section>
  <div class="report-body" data-led="purple"><div data-rpt-out></div></div>
</main>
"""
    return (head("진단 결과 리포트 | Aging Map 22 — careCL 케어클", "careCL 노화 타입 진단 결과 리포트",
                 sub=True, css=("css/bridge.css", "css/checkup-result.css", "css/report.css"))
            + header("aging-types.html") + body + FOOTER
            + tail(three=False, js=("js/report-data.js", "js/report.js", "js/radar.js", "js/reportpage.js"), fab=False))


PAGES["survey.html"] = page_survey


# ── 왼쪽 패널 그래픽 시안별 리포트 (로그인 전 화면 비교용) ──
PANEL_VARIANTS = [
    ("survey-p1.html", "lab/left-1-particle-face.html", "입자 얼굴"),
    ("survey-p2.html", "lab/left-3-terminal.html", "터미널"),
    ("survey-p3.html", "lab/left-4-hologram-device.html", "홀로그램"),
    ("survey-p4.html", "lab/left-5-aurora.html", "오로라"),
    ("survey-p5.html", "lab/left-6-device-3d.html", "3D 기기"),
    ("survey-p6.html", "lab/left-7-zone-photo.html", "부위 사진"),
]


def page_survey_panel(idx):
    name, src, _ = PANEL_VARIANTS[idx]
    tabs = "".join(f'<a href="{n}" data-src="{s_}"{" class=on" if i == idx else ""}><i>{i + 1}</i>{label}</a>'
                   for i, (n, s_, label) in enumerate(PANEL_VARIANTS))
    out = page_survey()
    out = re.sub(r'<div class="sv__stick">.*?</div>\n    </div>\n  </aside>',
                 f'<div class="sv__stick sv__stick--frame"><iframe src="{src}?embed=1&amp;v={VER}" title="AI 진단 그래픽" loading="eager"></iframe></div>\n  </aside>',
                 out, count=1, flags=re.S)
    out = out.replace('<main class="sv sv--stem"', f'<nav class="pvtabs" aria-label="왼쪽 그래픽 시안">{tabs}</nav>\n<main class="sv sv--stem sv--framed"', 1)
    out = out.replace('<script src="js/orb.js', '<script data-off="js/orb.js', 1)
    # 탭은 페이지 이동 없이 왼쪽 그래픽만 바꾼다 (js/pvtabs.js)
    out = out.replace('</body>', f'<script src="js/pvtabs.js?v={VER}"></script>' + chr(10) + '</body>', 1)
    return out


for _i, (_n, _s, _l) in enumerate(PANEL_VARIANTS):
    PAGES[_n] = (lambda i=_i: page_survey_panel(i))
PAGES["survey.html"] = lambda: page_survey_panel(0)


def page_survey_flow():
    """survey2.html — 1번은 왼쪽 패널, 2~5번은 전체 화면 인트로 → 가운데 설문 (js/pvtabs.js data-flow)"""
    out = page_survey_panel(0)
    out = re.sub(r'href="survey-p(\d)\.html"', r'href="survey2.html?g=\1"', out)
    out = out.replace('<nav class="pvtabs"', '<nav class="pvtabs" data-flow', 1)
    out = out.replace('sv--framed"', 'sv--framed sv--flow"', 1)
    out = out.replace('</main>', '<div class="sv__mini" hidden aria-hidden="true"><iframe title="TECH FIT 3D" tabindex="-1"></iframe></div>\n</main>', 1)
    return out


PAGES["survey2.html"] = page_survey_flow


def page_survey_grid():
    """survey-g.html — GRID 톤 설문 (2026-11-12). 6번 '부위 사진' 그래픽 하나만, 흰 바탕·세로선·오렌지.
    문항·리포트 내용은 그대로, 디자인은 css/grid-survey.css"""
    out = page_survey_panel(5)
    out = out.replace('<nav class="pvtabs"', '<nav class="pvtabs" hidden', 1)   # 탭은 숨기고 그래픽 전환 로직만 쓴다
    out = out.replace('<main class="sv sv--stem sv--framed"', '<main class="sv sv--stem sv--framed sv--grid sv--auto"', 1)
    out = out.replace('</head>', f'<link rel="stylesheet" href="css/grid-survey.css?v={VER}">\n</head>', 1)
    return out


PAGES["survey-g.html"] = page_survey_grid


def page_survey_chat():
    """survey-c.html — AI 상담 대화형 설문 + 진단서 리포트 (2026-11-12 B안).
    문항·결과 내용은 survey.js · report.js 그대로, 대화는 js/survey-chat.js, 모양은 css/survey-chat.css"""
    body = """<main class="sv sv--chat">
  <div class="svc-wrap">
    <aside class="svc-face" aria-hidden="true"><iframe src="lab/left-7-zone-photo.html?embed=loop&amp;v=""" + VER + """" title="Aging Map 22 얼굴 부위" tabindex="-1" loading="eager"></iframe></aside>
    <section class="svc">
      <div class="svc__head">
        <span class="svc__agent"><i class="svc__orb" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 2.2 14 8.4 20.2 10.4 14 12.4 12 18.6 10 12.4 3.8 10.4 10 8.4Z" fill="currentColor"/><circle cx="19.4" cy="4.2" r="1.7" fill="currentColor" opacity=".9"/><circle cx="4.8" cy="18.4" r="1.2" fill="currentColor" opacity=".7"/></svg></i><span><b><span class="lf">careCL</span> AI</b><small><i class="svc__live" aria-hidden="true"></i>상담 중 · Aging Map 22</small></span></span>
        <span class="svc__meta">노화 타입 상담</span>
      </div>
      <div class="svc__thread" id="svChat" aria-live="polite"></div>
      <nav class="svc__bar" hidden>
        <button type="button" class="svc__back" data-back>← 이전 질문</button>
        <span class="svc__track" aria-hidden="true"><i></i></span>
        <span class="svc__cnt"><b>01</b> / 18</span>
      </nav>
    </section>
  </div>
  <section class="svc__report" id="svReport"><div class="sv__form" id="svForm"></div></section>
</main>
"""
    return (head("AI 피부 상담 | Aging Map 22 — careCL 케어클", "AI 피부 에이전트와 대화하며 나의 노화 타입과 먼저 관리할 부위를 확인하세요",
                 css=("css/bridge.css", "css/checkup-result.css", "css/report.css"), body_cls="survey survey--chat")
            + header("aging-types.html") + body + FOOTER
            + tail(three=False, js=("js/report-data.js", "js/report.js", "js/radar.js", "js/survey.js", "js/survey-chat.js"), fab=False)
            ).replace('</head>', f'<link rel="stylesheet" href="css/survey-chat.css?v={VER}">' + chr(10) + '</head>', 1)   # grid.css 뒤에 오게


PAGES["survey-c.html"] = page_survey_chat


def page_survey_chat_result():
    """survey-c-result.html — 대화형 설문이 끝나면 넘어오는 리포트 전용 화면 (2026-11-12 요청: 설문과 리포트를 별도 화면으로)"""
    out = page_survey_chat()
    out = out.replace('<main class="sv sv--chat">', '<main class="sv sv--chat sv--result">', 1)
    out = re.sub(r'  <div class="svc-wrap">.*?\n  </div>\n', '', out, count=1, flags=re.S)
    out = out.replace('<title>AI 피부 상담 |', '<title>AI 진단 리포트 |', 1)
    return out


PAGES["survey-c-result.html"] = page_survey_chat_result
   # 시안 확인용 사이트 — 기본 설문에도 그래픽 탭 6개
PAGES["report.html"] = page_report

# ── AI 피부 진단 공개 여부 ──────────────────────────────
# False: 진단(survey.html) · 리포트(report.html)로 가는 링크를 모든 페이지에서 뗀다.
#        두 페이지 파일은 그대로 만들되 검색에 안 잡히게 한다(주소를 아는 사람만 열 수 있음).
# True : 작업이 끝나면 이 값만 바꾸면 버튼 · 메뉴 · 푸터 · 본문 링크가 모두 다시 붙는다.
AI_TEST_PUBLIC = False
# 비공개 동안 진단·리포트 화면은 이 접두어가 붙은 주소로만 만든다 (예: lab-410bf9f9c6-survey.html)
# survey.html · report.html 같은 짐작 가능한 주소는 지워서 열리지 않게 한다.
AI_SECRET = "lab-410bf9f9c6"


_LF_SKIP = ("script", "style", "title", "textarea", "svg")
def logo_font(html):
    """본문에 보이는 careCL 글자는 모두 로고 서체(.lf)로 감싼다 — 태그 속성·head·script 안은 건드리지 않음"""
    parts = re.split(r"(<[^>]+>)", html)
    stack = []; out = []; inbody = False
    for i, p in enumerate(parts):
        if p.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", p)
            if m:
                tag = m.group(2).lower()
                if tag == "body": inbody = not m.group(1)
                if tag in _LF_SKIP and not p.endswith("/>"):
                    if m.group(1):
                        if stack and stack[-1] == tag: stack.pop()
                    else: stack.append(tag)
            out.append(p)
        elif inbody and not stack and ("careCL" in p or "care Clinical Level" in p) and not (out and out[-1].startswith('<span class="lf"')):
            out.append(re.sub(r"care Clinical Level|careCL", lambda m: '<span class="lf">' + m.group(0) + '</span>', p))
        else:
            out.append(p)
    return "".join(out)

def hide_ai_test(html):
    html = re.sub(r'<a class="aifab".*?</a>\n?', '', html, flags=re.S)                       # 오른쪽 아래 버튼
    html = re.sub(r'<div class="foot__side">.*?</div>\s*(?=</div>\s*<div class="foot__row")', '', html, flags=re.S)  # 푸터 진단 안내
    html = re.sub(r'<div class="core__cta">.*?</div>', '', html, flags=re.S)                   # 메인 '나의 Aging Type 알아보기'
    html = re.sub(r'<a[^>]*href="(?:survey|report)\.html[^"]*"[^>]*>.*?</a>', '', html, flags=re.S)  # 나머지 링크
    html = re.sub(r'<p>\s*</p>', '', html)
    return html


def is_ai_page(name):
    return name.startswith("survey") or name.startswith("report")


def secret_links(html):
    """비공개 화면끼리 거는 링크를 비밀 주소로 바꾸고, 스크립트가 만드는 링크에도 접두어를 알려준다."""
    html = re.sub(r'(href=")((?:survey|report)[\w-]*\.html)', lambda m: m.group(1) + AI_SECRET + "-" + m.group(2), html)
    return html.replace("</head>", f'<script>window.CL_AI_PREFIX="{AI_SECRET}-";</script>\n</head>', 1)


def ai_cleanup():
    """공개 여부에 맞지 않는 진단 파일을 지운다 (비공개: 원래 주소, 공개: 비밀 주소)."""
    for f in os.listdir(ROOT):
        if not f.endswith(".html"):
            continue
        secret = f.startswith(AI_SECRET + "-")
        if (not AI_TEST_PUBLIC and is_ai_page(f)) or (AI_TEST_PUBLIC and secret):
            os.remove(os.path.join(ROOT, f))


if __name__ == "__main__":
    # 결과지 개선 시안 — 원본은 content/report-preview.src. 비공개면 비밀 주소로, 공개면 report-preview.html로 만든다
    ai_cleanup()
    preview_src = io.open(os.path.join(ROOT, "content", "report-preview.src"), encoding="utf-8").read()
    if AI_TEST_PUBLIC:
        io.open(os.path.join(ROOT, "report-preview.html"), "w", encoding="utf-8").write(preview_src)
    else:
        io.open(os.path.join(ROOT, AI_SECRET + "-report-preview.html"), "w", encoding="utf-8").write(secret_links(preview_src))
    for name, fn in PAGES.items():
        out = fn()
        if name.startswith("survey-p") or name == "survey2.html":   # 왼쪽 그래픽 비교용 시안 페이지는 공개 후에도 검색에서 뺀다
            out = out.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex, nofollow">', 1)
        elif not AI_TEST_PUBLIC:
            if name.startswith("survey") or name == "report.html":
                out = out.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="noindex, nofollow">', 1)
            else:
                out = hide_ai_test(out)
        if not AI_TEST_PUBLIC and is_ai_page(name):
            out = secret_links(out)
            name = AI_SECRET + "-" + name
        out = logo_font(out)
        io.open(os.path.join(ROOT, name), "w", encoding="utf-8").write(out)
        print("built", name)
    print("v=" + VER)
