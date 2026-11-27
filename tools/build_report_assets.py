# -*- coding: utf-8 -*-
"""리포트 이미지 일괄 생성 — assets/img/report/ 아래에 개발용 파일로 떨어뜨린다 (2026-11-27)

리포트 글은 DB에서 불러오지만 그림은 미리 파일로 있어야 하므로,
유형 · 부위 · 모드 · 관리 단계 · 생활습관 키마다 파일 하나씩 만든다.
  python tools/build_report_assets.py
"""
import io, json, os, re, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(IMG, "report")
JS = io.open(os.path.join(ROOT, "js", "report.js"), encoding="utf-8").read()


def mk(*p):
    d = os.path.join(OUT, *p)
    os.makedirs(d, exist_ok=True)
    return d


# ── 1. 6가지 유형 아이콘 (상세페이지 6 Aging Types 아이콘) — 기본(회색) / 내 유형(주황) ──
TYPES = ["early", "tired", "fine", "sag", "muscle", "mixed"]
icons = json.loads(re.search(r"var TYPE_ICONS = (\[.*?\]);", JS, re.S).group(1))
d = mk("types")
for key, svg in zip(TYPES, icons):
    for suffix, color in (("", "#8E847C"), ("-on", "#E0662B")):
        s = svg.replace('stroke="currentColor"', 'stroke="%s"' % color).replace('fill="currentColor"', 'fill="%s"' % color)
        s = s.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        io.open(os.path.join(d, key + suffix + ".svg"), "w", encoding="utf-8").write(s)

# ── 2. 22개 관리 부위 확대 사진 — t-face-clean.jpg(1672×941) 위 좌표(px) 중심 정사각 ──
#    U·M·L은 메인 v2 Aging Map 22 좌표와 같은 점. B3 손등 · B4 팔뚝 · B5 무릎은 사진에 없어 비워 둔다(제작 필요).
AREA = {
    "U1": (835, 222), "U2": (761, 315), "U3": (839, 275), "U4": (911, 336), "U5": (844, 366), "U6": (843, 308), "U7": (971, 290),
    "M1": (910, 410), "M2": (940, 522), "M3": (866, 496), "M4": (1012, 490),
    "L1": (802, 510), "L2": (873, 576), "L3": (819, 636), "L4": (961, 592), "L5": (1100, 420), "L6": (873, 682),
    "B1": (905, 755), "B2": (870, 835),
}
face = Image.open(os.path.join(IMG, "t-face-clean.jpg")).convert("RGB")
d = mk("area")
HALF = 135
for code, (x, y) in AREA.items():
    box = (x - HALF, y - HALF, x + HALF, y + HALF)
    tile = Image.new("RGB", (HALF * 2, HALF * 2), face.getpixel((min(max(x, 0), face.width - 1), face.height - 1)))
    src = face.crop((max(box[0], 0), max(box[1], 0), min(box[2], face.width), min(box[3], face.height)))
    tile.paste(src, (max(0, -box[0]), max(0, -box[1])))
    tile.resize((360, 360), Image.LANCZOS).save(os.path.join(d, code + ".jpg"), quality=86)

# ── 3. 모드별 사용 방법 그림 (TECH FIT 사용 가이드북 12~14쪽) ──
d = mk("guide")
for k in ("eye", "face", "body", "glow", "ems"):
    shutil.copyfile(os.path.join(IMG, "rx-guide-%s.jpg" % k), os.path.join(d, k + ".jpg"))
shutil.copyfile(os.path.join(IMG, "rx-ill-ems.png"), os.path.join(d, "ems-side.png"))

# ── 4. 관리 순서 — 세안·기초·마스크는 선 아이콘, 모드 단계는 기기 사진 ──
d = mk("steps")
order = dict(re.findall(r"(\w+): '(<[^']+)'", re.search(r"var ORDER_ICONS = \{(.*?)\};", JS, re.S).group(1)))
for k, body in order.items():
    io.open(os.path.join(d, k + ".svg"), "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#E0662B" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>")
for k in ("eye", "face", "body", "glow", "ems"):
    shutil.copyfile(os.path.join(IMG, "m-mode-%s.jpg" % k), os.path.join(d, k + ".jpg"))

# ── 5. 생활습관 아이콘 ──
d = mk("life")
life = dict(re.findall(r"(\w+): '(<[^']+)'", re.search(r"var LIFE_ICONS = \{(.*?)\};", JS, re.S).group(1)))
for k, body in life.items():
    io.open(os.path.join(d, k + ".svg"), "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#E0662B" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>")

# ── 6. 고정 사진 (유형과 관계없이 같은 자리) ──
d = mk("common")
for src, dst in (("rx-homecare.jpg", "care.jpg"), ("g-why-stamp.jpg", "rf-stamp.jpg"),
                 ("c-techfit-case.jpg", "coupon-techfit.jpg"), ("rx-mask-set.jpg", "coupon-consumables.jpg")):
    shutil.copyfile(os.path.join(IMG, src), os.path.join(d, dst))

print("ok", sum(len(f) for _, _, f in os.walk(OUT)), "files")
