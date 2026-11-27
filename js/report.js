/* =========================================================
   careCL — 진단 결과 리포트
   · 화면 구성·디자인: 개발 화면(Checkup.tsx · checkup.css)과 같은 마크업 → css/checkup-result.css
   · 문구: js/report-data.js (결과지 FINAL pptx 8종에서 자동 생성)
   · survey.js(설문 완료 화면)와 report.html(미리보기)이 함께 쓴다.
   ========================================================= */
(function () {
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

  /* 유형 소개(커버 아래 카드) — 비로그인에도 공개되는 요약 */
  var REPORT = {
    early: {
      en: 'Early Aging Type', name: '초기노화형',
      tagline: '주름보다 피부톤과 맑음의 변화가 먼저 오는 유형',
      desc: '아직 깊은 주름이나 뚜렷한 처짐은 크지 않지만, 피부톤이 예전보다 칙칙해지고 기미·잡티가 눈에 띄며 피부의 맑음과 광채가 감소하기 시작하는 유형입니다.',
      traits: ['피부톤 저하', '기미 · 잡티', '칙칙함', '광채 감소', '피부결 변화'],
      concern: '피부톤 저하 · 기미 · 잡티 · 칙칙함 · 광채 감소'
    },
    tired: {
      en: 'Tired Type', name: '피로형',
      tagline: '주름보다 생기와 활력이 먼저 줄어드는 유형',
      desc: '주름보다 먼저 얼굴의 생기와 활력이 줄어들며, 특히 눈밑을 중심으로 피곤하고 지쳐 보이는 인상이 나타나는 유형입니다.',
      traits: ['눈밑 변화', '다크서클', '안색 저하', '생기 부족', '입꼬리 변화'],
      concern: '눈밑 변화 · 다크서클 · 안색 저하 · 생기 부족 · 입꼬리 변화'
    },
    fine: {
      en: 'Fine-Wrinkled Type', name: '잔주름형',
      tagline: '윤곽보다 피부 표면의 잔주름이 먼저 보이는 유형',
      desc: '얼굴 윤곽의 변화보다 피부 표면의 잔주름이 먼저 두드러지는 유형입니다. 특히 눈가와 입가, 목처럼 피부가 얇거나 움직임이 많은 부위의 변화가 눈에 띄기 시작합니다.',
      traits: ['눈가 잔주름', '입가 잔주름', '목주름', '건조함', '얇아 보이는 피부'],
      concern: '눈가 잔주름 · 입가 잔주름 · 건조함 · 얇아 보이는 피부'
    },
    sag: {
      en: 'Deformational Type', name: '변형·처짐형',
      tagline: '주름보다 얼굴 윤곽과 형태의 변화가 먼저 느껴지는 유형',
      desc: '주름 자체보다 볼과 턱선 등 얼굴의 윤곽과 형태 변화가 먼저 느껴지는 유형입니다. 시간이 지나면서 중안면과 하안면의 변화가 보다 뚜렷하게 나타날 수 있습니다.',
      traits: ['볼 변화', '팔자 라인', '턱선 변화', '이중턱', '얼굴 윤곽 변화'],
      concern: '볼 변화 · 팔자 · 턱선 · 이중턱 · 얼굴 윤곽 변화'
    },
    muscle: {
      en: 'Muscular Type', name: '근육형',
      tagline: '처짐보다 표정이 얼굴에 먼저 남는 유형',
      desc: '얼굴 윤곽은 오래 유지되지만 반복 사용하는 표정 근육이 얼굴에 흔적을 남깁니다. 미간·이마·눈가에 깊고 굵은 주름이 생기고 표정을 짓지 않아도 선이 남습니다. 노화가 진행될수록 인상이 점점 강해질 수 있습니다.',
      traits: ['미간 주름 증가', '이마 주름 증가', '깊은 표정주름', '윤곽 유지', '광대 돌출 · 볼 꺼짐 동반 가능'],
      concern: '미간 주름 · 이마 주름 · 표정주름 · 광대 돌출 · 볼 꺼짐'
    },
    mixed: {
      en: 'Combined Type', name: '혼합형',
      tagline: '부위별로 노화 패턴이 다르게 나타나는 유형',
      desc: '실제 많은 사람들은 하나의 유형만으로 심플하게 노화가 진행되진 않습니다. 특히 중년 이후 노화가 가속화될 경우 혼합형 노화 유형일 가능성이 높습니다. 눈가는 잔주름형으로 진행되면서 턱과 볼 부위는 변형 처짐형으로 진행되는 경우가 가장 흔한 혼합형 중 하나입니다. 혼합형은 특정 1가지 문제가 아니라 여러 노화 패턴이 동시에 나타나는 상태를 의미하기 때문에 관리 우선 순위를 잘 정하고 체계적인 관리를 늦추지 말고 시작하는 것이 좋습니다.',
      traits: ['복합 노화 진행', '여러 유형 동시 발생', '다양한 부위 노화 신호', '관리 우선순위 설정이 중요'],
      concern: '복합 노화 · 전반적 노화 · 다중 피부 고민'
    }
  };

  /* 유형과 관계없이 늘 같은 내용 (개발 화면 resultStaticContent.ts와 동일) */
  var DEVICE_TABLE = [
    ['고주파(RF)', '고주파 에너지를 피부 속 깊이 전달해 탄력·처짐·윤곽 관리'],
    ['초음파(US·HIFU)', 'HIFU는 강한 에너지로 처짐 관리 (단, 자극이 강해 볼 꺼짐(지방 감소) 동반 가능) 초음파 미세진동 방식(예: LDM)은 피부 진정·수분 관리'],
    ['EMS', '전기 자극으로 하안부·표정 주름 관리, 고주파와 병행 사용 시 더욱 효과적'],
    ['LED·미세전류·갈바닉·EP', '빛·약한 전류로 피부 톤·광채·컨디션 관리 · EP(전기천공)는 유효성분 흡수를 도움'],
    ['진동·롤러', '마사지로 순환·부기 관리']
  ];
  var SHOT_FAQ = [
    ['① 샷(SHOT)이 뭔가요?', "한 자리에 헤드를 대고 약 5초간 밀착하는 동작(스탬핑)이 '1샷'입니다. 안내된 샷수는 한 곳을 그만큼 누르는 게 아니라, 그리드 칸을 따라 자리를 옮겨가며 그 부위를 빠짐없이 덮는 대략적인 횟수예요. 그리드 마스크팩 칸을 채운다고 생각하시면 되고, 정확히 세지 않으셔도 괜찮습니다."],
    ['② 자동 종료 타이머', 'SHOT 모드는 7분, GLOW·EMS 모드는 5분이 지나면 안전을 위해 자동으로 종료됩니다. 안내해 드린 부위를 순서대로 관리하시면 대부분 그 전에 끝나며, 관리할 부위가 많이 남았을 때만 다시 켜서 이어 진행하시면 됩니다.'],
    ['③ 강도(레벨) 조절', '레벨은 1~5단계이며, 처음 사용하실 땐 낮은 단계부터 시작하세요. 따뜻한 열감이 느껴지는 정도가 적정이고, 뜨겁게 느껴지면 레벨을 낮추면 됩니다. (그리드 마스크팩과 함께 쓸 땐 3단계부터, 콜라겐 젤·민감성 피부는 1단계부터 권장)']
  ];
  var DISCLAIMER = '본 결과는 고객님의 설문 응답을 바탕으로 현재 인식하는 노화 특성과 관리 우선순위를 안내하는 참고용 분석이며, 의료적 진단이 아닙니다. 사진 촬영·의료적 검사를 통한 진단 결과가 아니며, 실제 피부 상태와 체감 변화는 개인에 따라 다를 수 있습니다. 피부 질환이나 지속적인 이상 증상이 있는 경우 의료전문가와 상담하시기 바랍니다.';

  var AXES = [['fine', '잔주름형', 8], ['sag', '변형·처짐형', 7], ['muscle', '근육형', 9], ['tired', '피로형', 9], ['early', '초기노화형', 7]];

  /* 카드 제목 아이콘 — 개발 화면 ResultIcons.tsx와 같은 선 아이콘 */
  var ICON_PATHS = {
    reason: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.7-1.5 1.2-1.5 2.5M12 17h.01"/>',
    area: '<path d="M12 21s7-5.5 7-11a7 7 0 10-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    homecare: '<path d="M12 3c3.5 4 6 7 6 10a6 6 0 01-12 0c0-3 2.5-6 6-10z"/>',
    ingredient: '<path d="M9 3h6M10 3v6l-5 8a3 3 0 002.6 4.5h8.8A3 3 0 0019 17l-5-8V3"/>',
    lifestyle: '<path d="M20.5 13A8.5 8.5 0 1111 3.5a6.5 6.5 0 009.5 9.5z"/>',
    device: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    rf: '<path d="M2 12c2.5-4 5-4 7.5 0s5 4 7.5 0 3.5-3.4 5-1.4"/><path d="M2 18c2.5-4 5-4 7.5 0s5 4 7.5 0"/>',
    usage: '<path d="M5 4v6a4 4 0 004 4h6"/><path d="M15 11l4 3-4 3"/>',
    shot: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>',
    faq: '<path d="M21 12a8 8 0 01-8 8H8l-4 3v-5.5A8 8 0 1121 12z"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.8.6-1.5 1-1.5 2M12 16h.01"/>',
    busy: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    ai: '<path d="M21 12a8 8 0 01-8 8H8l-4 3v-5.5A8 8 0 1121 12z"/><path d="M9 11h6M9 14h4"/>',
    coupon: '<path d="M3 9V6a1 1 0 011-1h16a1 1 0 011 1v3a3 3 0 000 6v3a1 1 0 01-1 1H4a1 1 0 01-1-1v-3a3 3 0 000-6z"/><path d="M13 5v14"/>',
    review: '<path d="M16 20v-1.5a3.5 3.5 0 00-3.5-3.5h-5A3.5 3.5 0 004 18.5V20"/><circle cx="10" cy="8" r="3.2"/><path d="M20 20v-1.5a3.5 3.5 0 00-2.6-3.4M15.5 5.2a3.2 3.2 0 010 5.6"/>',
    lock: '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/>'
  };
  function icon(name) {
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (ICON_PATHS[name] || '') + '</svg>';
  }
  function title(ic, text, extra) {
    return '<h3 class="cku-card-title"><span class="cku-card-icon">' + icon(ic) + '</span>' + text + (extra || '') + '</h3>';
  }
  function card(ic, text, inner, cls) { return '<section class="cku-card' + (cls ? ' ' + cls : '') + '">' + title(ic, esc(text)) + inner + '</section>'; }
  function paras(arr, cls) { return (arr || []).filter(function (t) { return String(t).replace(/[\s.]/g, '').length > 1; }).map(function (t) { return '<p class="cku-result-desc' + (cls ? ' ' + cls : '') + '">' + esc(t) + '</p>'; }).join(''); }

  /* 추천 성분 설명 — 세라마이드는 개발 화면 문구 그대로, 나머지는 같은 말투로 쓴 초안(고객사 확인 필요) */
  var INGREDIENT_INFO = {
    '세라마이드': '피부 바깥층을 이루는 지질 성분입니다. 건조해서 당기는 피부의 수분을 붙잡아 두는 데 쓰입니다.',
    '펩타이드': '아미노산 몇 개가 이어진 작은 단백질 조각입니다. 탄력 관리 화장품에 널리 쓰입니다.',
    '콜라겐 추출물': '피부 탄력 섬유의 주성분인 콜라겐에서 얻은 성분입니다. 피부 표면을 촉촉하고 매끄럽게 가꾸는 데 쓰입니다.',
    '히알루론산': '수분을 많이 머금는 보습 성분입니다. 피부에 수분을 채워 촉촉하게 유지하는 데 쓰입니다.',
    '레티놀': '비타민 A 계열 성분으로 주름 관리 화장품에 쓰입니다. 처음에는 저녁에 소량부터 쓰는 것이 좋습니다.',
    '아데노신': '주름 개선 기능성 원료로 쓰이는 성분입니다. 탄력·주름 관리 화장품에 들어갑니다.',
    '이데베논': '항산화 성분입니다. 자외선·환경 자극으로 흐려진 피부 컨디션을 관리하는 화장품에 쓰입니다.',
    '트라넥삼산': '피부 톤 관리 화장품에 쓰이는 성분입니다. 칙칙함·잡티가 신경 쓰일 때 고르는 성분입니다.',
    'PDRN': '연어 등에서 얻은 DNA 조각 성분입니다. 피부 결과 컨디션을 가꾸는 화장품에 쓰입니다.',
    '카페인': '부기와 칙칙함이 신경 쓰이는 눈가 제품에 자주 쓰이는 성분입니다.'
  };

  /* 실제 구매 후기 — 개발 화면 결과지에 노출된 쇼핑몰 후기(원문 그대로) */
  var REVIEWS = [
    { tag: '주름 이야기 · 눈가 · 옆볼 · 꾸준히 사용 중', rating: 5, date: '2025년 3월',
      body: '피부과 갈 돈은 없고... 애키우느라 시간도 없고..ㅋㅋ요즘 홈케어가 대세라길래 요고 큰맘먹고 주문했어여. 일단 다른 뷰티기기와 다르게 써마지 처럼 스탬핑빙식이라 뭔가 효과가 남다를거 같아서요. 애 재우고 요즘 맨날하는데 늠나 좋네여 ㅋㅋ 헤드피스도 2가지라 부위별로 케어할 수 있고~ 2주? 정도 꾸준히 쓴거같은디 볼옆 눈가 주름들 신경쓰이는 부위들 좋아지는게 눈에 보여요!! 저 콜라겐젤 필수~ㅎㅋㅋ 4단계로 주로 쓰는데 저거도톰하게 발라야 참을만해여 ㅋㅋ' },
    { tag: '주름 · 탄력·처짐 이야기 · 눈가 · 팔자 · 꾸준히 사용 중', rating: 5, date: '2024년 2월',
      body: '하루 빼고 매일 사용한 후기입니다~일단 제일 좋아진건 전체적인 탄력 과 모공이네요. 눈가 잔주름도 많이 좋아졌구요. 큰주름(팔자) 눈에 띄게 좋아지진 않았어요. 미세하게 어느날은 좋아진것 같다가 어느날 많이 웃고다니면 또 줄어들고 있나 싶긴해요 ㅎ 근데 저희 언니는 명절에 만나 2번사용하고 정말 눈에띄게 팔자주름이 없어지더라구요..사람마다 조금 다른가보다 싶어요. 더 열심히 관리하면 좋아질거라 생각하고 사용중입니다. 언니는 효과보고 주변에 입소문 냈더라구요 ㅎㅎ' },
    { tag: '주름 · 탄력·처짐 이야기 · 눈가 · 꾸준히 사용 중', rating: 5, date: '2025년 3월',
      body: '요즘 들어 부쩍 축축 처지는 피부 볼살 눈가 주름까지 고민이 많았는데요. 에스테틱 가게에는 비용도 부담스럽고 홈케어에 집중하려고 케어클 고주파 뷰티 디바이스를 사용해 보았어요. 문지르는 게 아니라 콕콕 눌러주는 스탬프 방식 자극없이 피부 속까지 에너지를 깊게 전달해줘요. 꾸준히 사용하니까 피부가 예전보다 탄탄해진 게 느껴져요. 요즘 피부 탄력 떨어졌다고 고민하는 엄마한테도 하나 사드려야겠어요' }
  ];

  /* AI 맞춤 상담 — 개발 화면에서 실제 생성된 답변 예시(혼합형). 이름은 가린다. 실제는 결과마다 AI가 새로 쓴다. */
  var AI_SAMPLE = [
    '안녕하세요, 김○○ 고객님. 소중한 피부를 위해 상담을 찾아주셔서 진심으로 환영합니다. 보통 피부의 시간은 단 하나의 모습으로만 흘러가지 않고, 여러 가지 변화가 동시에 복합적으로 찾아오는 경우가 많습니다. 고객님의 피부 역시 부위마다 서로 다른 노화 신호가 함께 관찰되는 혼합형으로 나타났어요. 특히 피부 결 사이로 얇게 자리 잡기 시작하는 잔주름 신호와 전반적인 탄력 저하를 알리는 초기 노화 신호가 둘 다 가장 뚜렷하게 감지되고 있어, 어느 한 가지만 챙기기보다는 두 신호를 함께 다독여주는 체계적인 관리가 필요한 상태입니다.',
    '피부 컨디션을 조금 더 들여다보면 피로감으로 인한 푸석한 신호도 어느 정도 얼굴에 드리워져 있지만, 다행히 깊은 윤곽 처짐이나 표정 근육에 의한 굵은 라인은 아직 미미하게 나타나고 있어요. 지금 단계에서 가장 눈여겨보고 먼저 손길을 보내주어야 할 곳은 이마와 인중 주변, 그리고 얇고 연약한 눈가 부위입니다. 이마에서 시작해 입술 위쪽과 눈가로 이어지는 흐름을 따라 잔주름과 초기 탄력 고민이 자리 잡기 쉬우니, 이 세 부위를 중심으로 세심한 안티에이징 루틴을 시작해보시는 것이 좋습니다.',
    '이렇게 여러 신호가 복합적으로 나타날 때는 보습과 탄력을 동시에 채워주는 단계별 홈케어가 큰 힘이 되어줍니다. 피부 장벽을 편안하게 감싸주는 세라마이드와 속수분을 촘촘히 채우는 히알루론산으로 기초를 다져주신 후, 탄력 케어에 도움을 주는 펩타이드와 콜라겐 추출물이 담긴 화장품을 곁들여보세요. 여기에 화장품의 흡수를 돕고 미세한 결을 정돈해주는 뷰티기기 케어를 함께해 주시면, 이마와 눈가, 입가 주변의 복합적인 피부 고민을 한결 탄탄하고 매끄럽게 가꾸실 수 있습니다.',
    '일상 속의 작은 생활 습관도 안티에이징 케어에 든든한 밑거름이 됩니다. 외출 전에는 사계절 내내 자외선 차단제를 꼼꼼히 발라 피부를 보호해주시고, 하루 동안 지친 피부가 스스로 회복할 수 있도록 충분한 수면과 규칙적인 수분 섭취를 잊지 마세요. 지금처럼 피부가 보내는 신호에 귀 기울이며 차근차근 관리를 이어가신다면, 시간이 지나도 생기 넘치고 건강한 피부를 충분히 지켜나가실 수 있을 거예요.'
  ];

  /* AI 상담 글에서 눈에 먼저 들어와야 할 말 — 유형·신호, 먼저 관리할 부위, 성분, 생활 습관 */
  var AI_KEYS = ['혼합형으로 나타났어요', '잔주름 신호', '초기 노화 신호', '두 신호를 함께 다독여주는 체계적인 관리',
    '이마와 인중 주변, 그리고 얇고 연약한 눈가 부위', '세라마이드', '히알루론산', '펩타이드와 콜라겐 추출물',
    '뷰티기기 케어', '자외선 차단제', '충분한 수면과 규칙적인 수분 섭취'];
  function aiHighlight(html) {
    AI_KEYS.forEach(function (k) { html = html.split(k).join('<mark class="cku-ai-hl">' + k + '</mark>'); });
    return html;
  }

  /* 미리보기(설문 없이)용 예시 응답 — 결과 유형이 가장 높게 */
  function sample(key) {
    var c = { fine: 2, sag: 2, muscle: 2, tired: 2, early: 1 };
    if (key === 'mixed') { c.fine = 6; c.sag = 6; } else c[key] = 7;
    return c;
  }

  function dataFor(key, mixWith) {
    var all = window.ckuReportData || {};
    if (key !== 'mixed') return all[key];
    return all['mixed_' + (mixWith === 'tired' || mixWith === 'muscle' ? mixWith : 'fine')];
  }

  function cover(R, stats) {
    // 오른쪽 오각형은 그린 뒤 survey.js가 ckuRadar.mount()로 채운다
    return '<section class="cku-cover has-radar">' +
      '<p class="cku-result-eyebrow">진단 결과</p>' +
      '<h2 class="cku-result-title"><span class="cku-code">' + esc(R.en) + '</span>' + esc(R.name) + '</h2>' +
      '<p class="cku-result-tagline">' + esc(R.tagline) + '</p>' +
      '<div class="cku-cover-radar" data-radar><div class="sv__sweep" aria-hidden="true"></div>' +
        '<svg viewBox="-215 -205 430 410" role="img" aria-label="5가지 노화 유형별 신호 세기"></svg></div>' +
      (stats || '') +
    '</section>';
  }
  function intro(R) {
    return '<section class="cku-card"><p class="cku-result-desc">' + esc(R.desc) + '</p>' +
      '<ul class="cku-result-traits">' + R.traits.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>' +
      '<p class="cku-result-concern">' + esc(R.concern) + '</p></section>';
  }
  function share() {
    var ch = [['kakao', '카카오톡', '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3.5C6.5 3.5 2 7 2 11.3c0 2.8 1.9 5.2 4.7 6.6-.2.8-.7 2.8-.8 3.2 0 0 0 .3.2.4.2.1.4 0 .4 0 .5-.1 3.3-2.2 3.8-2.5.6.1 1.1.1 1.7.1 5.5 0 10-3.5 10-7.8S17.5 3.5 12 3.5z"/></svg>'],
      ['facebook', '페이스북', '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>'],
      ['x', 'X', '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.8 3h3.1l-6.8 7.8L22 21h-6.3l-4.9-6.4L5.2 21H2.1l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7.4 4.7H5.5z"/></svg>']];
    return '<section class="cku-card"><div class="cku-share"><div class="cku-share-head"><p class="cku-share-line">친구도 내 유형과 같을까요?</p>' +
      '<p class="cku-share-sub">내 결과를 보내면 친구도 1분 만에 자기 유형을 확인할 수 있어요.</p></div><div class="cku-share-icons">' +
      ch.map(function (c) { return '<a class="cku-share-ico" href="#" data-share="' + c[0] + '"><span class="cku-share-ico-btn cku-share-' + c[0] + '" aria-hidden="true">' + c[2] + '</span><span>' + c[1] + '</span></a>'; }).join('') +
      '<button type="button" class="cku-share-ico" data-copy><span class="cku-share-ico-btn" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.5.5l3-3a5 5 0 00-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 00-7.5-.5l-3 3a5 5 0 007 7l1.7-1.7"/></svg></span><span>링크 복사</span></button>' +
      '</div></div></section>';
  }
  function actions(opts) {
    return '<div class="cku-result-actions">' +
      (opts.restart ? '<button type="button" class="cku-btn cku-btn-primary cku-retry" data-restart>다시 하기</button>' : '<a class="cku-btn cku-btn-primary cku-retry" href="' + (window.CL_AI_PREFIX || '') + 'survey.html">다시 하기</a>') +
    '</div>';
  }
  function wrap(inner) { return '<div class="checkup" data-rpt><div class="cku-result">' + inner + '</div></div>'; }


  /* ── 2026-11-27 리포트 개편: 6가지 유형 띠 · 부위 확대 · 기기 움직임 ── */
  var TYPE_STRIP = [['early', '초기노화형', '전구형'], ['tired', '피로형', '너구리형'], ['fine', '잔주름형', '스카프형'],
    ['sag', '변형·처짐형', '아이스크림형'], ['muscle', '근육형', '협곡형'], ['mixed', '혼합형', '지도형']];
  var TYPE_ICONS = ["<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M17.2 29.6C14.1 27.4 12 23.8 12 19.8a12 12 0 0 1 24 0c0 4-2.1 7.6-5.2 9.8-1.1.8-1.8 2-1.8 3.4V34H19v-1c0-1.4-.7-2.6-1.8-3.4Z\"/><path d=\"M20.5 26.5c0-3 1.2-5.2 3.5-5.2s3.5 2.2 3.5 5.2M22 21.8l2-2.6 2 2.6\"/><path d=\"M19 37h10M19.5 40h9M21.5 43h5\"/><path d=\"M24 2.8v3M9.6 8.2l2.1 2.1M3.8 20h3\"/><path d=\"M38.4 8.2l-2.1 2.1M44.2 20h-3\" opacity=\".35\" stroke-dasharray=\"1.4 2\"/><path d=\"M15.6 16.4a9 9 0 0 1 4.2-4.6\" opacity=\".5\"/></svg>", "<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M13 16.6 11.4 8c-.2-1 .9-1.6 1.7-1l6.6 5M35 16.6 36.6 8c.2-1-.9-1.6-1.7-1l-6.6 5\"/><path d=\"M14.2 14.2 13.4 10l3 2.2M33.8 14.2l.8-4.2-3 2.2\" opacity=\".4\"/><path d=\"M24 11c-9 0-15 6.4-15 14.2 0 7.8 6.6 13.8 15 13.8s15-6 15-13.8C39 17.4 33 11 24 11Z\"/><path d=\"M10.6 24.2c1.8-4 7.6-5.4 11.2-2.2.6 2.8-.8 6.4-4.4 7.4-3.4 1-6.6-1.4-6.8-5.2ZM37.4 24.2c-1.8-4-7.6-5.4-11.2-2.2-.6 2.8.8 6.4 4.4 7.4 3.4 1 6.6-1.4 6.8-5.2Z\" fill=\"currentColor\" fill-opacity=\".2\"/><circle cx=\"17\" cy=\"24.6\" r=\"2.1\" fill=\"#fff\"/><circle cx=\"31\" cy=\"24.6\" r=\"2.1\" fill=\"#fff\"/><circle cx=\"17.3\" cy=\"24.8\" r=\".9\" fill=\"currentColor\" stroke=\"none\"/><circle cx=\"30.7\" cy=\"24.8\" r=\".9\" fill=\"currentColor\" stroke=\"none\"/><path d=\"M13.6 30.2c2.2 1.4 5 1.4 7 0M27.4 30.2c2 1.4 4.8 1.4 7 0\" opacity=\".7\"/><path d=\"M14.8 32.6c1.8.8 3.6.8 5 0M28.2 32.6c1.4.8 3.2.8 5 0\" opacity=\".4\"/><path d=\"M22.2 31.6h3.6L24 33.6Z\" fill=\"currentColor\" fill-opacity=\".85\"/><path d=\"M24 33.6v1.4c-.8.8-2 .9-2.8.3M24 35c.8.8 2 .9 2.8.3\"/></svg>", "<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9 10c1 8.2 7 12.8 15 12.8s14-4.6 15-12.8\"/><path d=\"M15.2 10c1 5.2 4.4 7.8 8.8 7.8s7.8-2.6 8.8-7.8\"/><path d=\"M9 10c4.6-3.4 25.4-3.4 30 0M15.2 10c4-1.8 13.6-1.8 17.6 0\" opacity=\".4\"/><path d=\"M11.6 13.4c1.8 1.2 3 2.6 3.6 4.4M36.4 13.4c-1.8 1.2-3 2.6-3.6 4.4\" opacity=\".5\"/><path d=\"M20.8 19.6c1.2-1 5.2-1 6.4 0l.8 4.6c-1.8 1.4-6.2 1.4-8 0Z\" fill=\"#fff\"/><path d=\"M20.6 24.4 14.4 38.8l7.2 2.6 4-16.6\"/><path d=\"M27.4 24.4l6.4 13.8-7 3.2-3.6-16.4\"/><path d=\"M18.4 28.8c1.4.6 1.8 2 1.2 3.6M17 33.4c1.2.4 1.6 1.4 1.2 2.6M29.8 29.2c-1.2.8-1.4 2.2-.6 3.6M31.6 33.6c-1 .6-1.2 1.6-.6 2.6\" opacity=\".55\"/><path d=\"M15 40l-.8 2.4M17.6 40.8l-.6 2.6M20.2 41.6l-.4 2.6M27.4 41.8l.4 2.6M30 40.8l.8 2.4M32.4 39.6l1 2.2\" opacity=\".7\"/></svg>", "<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M15.5 24 24 44l8.5-20\"/><path d=\"M17.2 28 28.3 34M30.8 28 19.8 34M19.8 34 25.7 40M28.3 34 22.3 40\" opacity=\".4\"/><path d=\"M35 24A11 11 0 0 0 13 24v3a2 2 0 0 0 4 0v-1.4a1.6 1.6 0 0 1 3.2 0v4.8a2 2 0 0 0 4 0v-4.8a1.6 1.6 0 0 1 3.2 0V28a2 2 0 0 0 4 0v-2.4a1.8 1.8 0 0 1 3.6 0Z\" fill=\"#fff\"/><path d=\"M17.4 18a7.6 7.6 0 0 1 4.8-3.6\" opacity=\".45\"/><path d=\"M29.4 33c0 0 1.5 1.7 1.5 2.7a1.5 1.5 0 0 1-3 0c0-1 1.5-2.7 1.5-2.7Z\"/></svg>", "<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M4 41 11.5 17l4.5 4.6 3.4-8.6L22.6 41\"/><path d=\"M44 41 37.4 15.6l-3.8 5.4-3-4.2L26.4 41\"/><path d=\"M9.4 27.6h5.4M7.6 33.6h11.6M32.2 27h8.4M30.6 33.4h11\" opacity=\".4\"/><path d=\"M22.6 41c1-3.2 3.6-4.2 3.4-7.4\" opacity=\".6\"/><path d=\"M2.5 44h43\"/><circle cx=\"24.4\" cy=\"8.4\" r=\"2.8\" opacity=\".55\"/></svg>", "<svg viewBox=\"0 0 48 48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"7\" y=\"7\" width=\"34\" height=\"34\" rx=\"5\"/><path d=\"M24 7v34M7 24h34\" /><rect x=\"9.6\" y=\"9.6\" width=\"28.8\" height=\"28.8\" rx=\"3\" stroke-dasharray=\"1.2 2\" opacity=\".35\"/><circle cx=\"15.5\" cy=\"15.5\" r=\"2.6\"/><path d=\"M15.5 9.8v1.2M15.5 20v1.2M9.8 15.5H11M20 15.5h1.2\" opacity=\".55\"/><path d=\"M27 13.2c1.5-1.2 3-1.2 4.5 0s3 1.2 4.5 0M27 17.4c1.5-1.2 3-1.2 4.5 0s3 1.2 4.5 0\" /><path d=\"M10.8 28.2h9.4v2.2a1.6 1.6 0 0 1-3.2 0v-.6a1.4 1.4 0 0 0-2.8 0v3a1.7 1.7 0 0 1-3.4 0Z\"/><path d=\"M26.6 37.4l3.6-8 2.4 3.2 2-4.4 3 9.2\"/></svg>"];
  function typesStrip(k) {
    return '<section class="rx-types" aria-label="careCL 6가지 노화 유형"><p class="rx-types__h"><b>careCL 6 Aging Types</b><span>6가지 노화 유형 가운데 고객님의 유형은 <em>' + esc(REPORT[k].name) + '</em>입니다</span></p><ol class="rx-types__list">' +
      TYPE_STRIP.map(function (t, i) {
        var me = t[0] === k;
        return '<li class="rx-type' + (me ? ' is-me' : '') + '"' + (me ? ' aria-current="true"' : '') + '><figure aria-hidden="true">' + TYPE_ICONS[i] + '</figure>' +
          '<span class="rx-type__no">' + ('0' + (i + 1)) + '</span><b>' + esc(t[1]) + '</b><small>' + esc(t[2]) + '</small>' + (me ? '<em class="rx-type__me">나의 유형</em>' : '') + '</li>';
      }).join('') + '</ol></section>';
  }

  /* 얼굴 사진(rx-face.jpg 700×881) 위 부위별 누르는 자리 — 화살표 방향 순서대로 */
  var FACE_W = 700, FACE_H = 881;
  var AREA_PTS = {
    U1: [[180, 170], [240, 150], [300, 145], [360, 160]],
    U2: [[205, 262], [212, 232], [232, 205], [265, 192]],
    U4: [[330, 262], [360, 245], [390, 225], [410, 200]],
    U5: [[265, 318], [300, 322], [335, 318], [360, 300]],
    M1: [[330, 370], [370, 350], [405, 320], [430, 285]],
    M2: [[340, 500], [365, 455], [385, 410], [395, 370]],
    M3: [[330, 385], [318, 420], [298, 445], [285, 470]],
    L1: [[200, 424], [232, 422], [262, 428], [292, 440]],
    L4: [[270, 575], [335, 550], [395, 510], [445, 455]],
    B1: [[345, 770], [345, 720], [345, 670], [345, 620]]
  };
  function areaCenter(code) {
    var p = AREA_PTS[code]; if (!p) return [FACE_W / 2, FACE_H / 2];
    var x = 0, y = 0; p.forEach(function (q) { x += q[0]; y += q[1]; });
    return [x / p.length, y / p.length];
  }
  function zoomStyle(code) {
    var c = areaCenter(code), S = 2.6, ar = FACE_H / FACE_W;
    var px = c[0] / FACE_W, py = c[1] / FACE_H;
    var bx = (S * px - 0.5) / (S - 1), by = (S * ar * py - 0.5) / (S * ar - 1);
    bx = Math.max(0, Math.min(1, bx)); by = Math.max(0, Math.min(1, by));
    return 'background-image:url(assets/img/rx-face.jpg);background-size:' + (S * 100) + '% auto;background-position:' + (bx * 100).toFixed(1) + '% ' + (by * 100).toFixed(1) + '%';
  }
  function modeKey(m) { m = String(m || '').toUpperCase(); return m.indexOf('EYE') > -1 ? 'eye' : m.indexOf('BODY') > -1 ? 'body' : m.indexOf('GLOW') > -1 ? 'glow' : m.indexOf('EMS') > -1 ? 'ems' : 'face'; }
  /* 관리 순서 사진 — 받은 사진만 넣는다 (11-27: 기초 관리 = 케어클20757 토닝 세럼) */
  function orderPhoto(t) { return /기초|토너|에멀/.test(t) ? 'rx-basic.jpg' : /마스크/.test(t) ? 'rx-mask.jpg' : ''; }
  function orderImg(t) {
    if (/EYE SHOT/.test(t)) return 'm-mode-eye.jpg';
    if (/FACE SHOT/.test(t)) return 'm-mode-face.jpg';
    if (/BODY SHOT/.test(t)) return 'm-mode-body.jpg';
    if (/GLOW/.test(t)) return 'm-mode-glow.jpg';
    if (/EMS/.test(t)) return 'm-mode-ems.jpg';
    if (/마스크|젤/.test(t)) return 'p-mask.jpg';
    if (/기초|토너|에멀/.test(t)) return 'e-serum-water-v.jpg';
    return '';
  }
  var LIFE_ICONS = {
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    water: '<path d="M7 3h10l-1.4 16.2a2 2 0 01-2 1.8h-3.2a2 2 0 01-2-1.8z"/><path d="M7.6 9h8.8"/>',
    drop: '<path d="M12 3c3.5 4 6 7 6 10a6 6 0 01-12 0c0-3 2.5-6 6-10z"/>',
    moon: '<path d="M20.5 13A8.5 8.5 0 1111 3.5a6.5 6.5 0 009.5 9.5z"/>',
    face: '<circle cx="12" cy="12" r="9"/><path d="M8.5 14.5c1.9 1.8 5.1 1.8 7 0M9 9.5h.01M15 9.5h.01"/>'
  };
  function lifeIcon(t) {
    var k = /자외선|햇빛|선크림/.test(t) ? 'sun' : /섭취|물/.test(t) ? 'water' : /보습|수분/.test(t) ? 'drop' : /수면|잠/.test(t) ? 'moon' : 'face';
    return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + LIFE_ICONS[k] + '</svg>';
  }
  var REVIEW_IMG = ['t-techfit-use.jpg', 't-model-eye.jpg', 'g-step4.jpg'];

  /* 기기 움직임 — 부위마다 자리를 옮겨 가며 한 칸씩 '꾹' 누르고, 누른 자리는 점으로 남긴다 */
  function initDemo(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('[data-demo]'), function (demo) {
      if (demo._rx) return; demo._rx = true;
      var stage = demo.querySelector('[data-stage]'), dev = demo.querySelector('[data-dev]'), marks = demo.querySelector('[data-marks]'), hud = demo.querySelector('[data-hud]');
      var btns = Array.prototype.slice.call(demo.querySelectorAll('[data-shot]'));
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      var cur = 0, run = 0, visible = false;
      function pos(p) { return [(p[0] / FACE_W * 100), (p[1] / FACE_H * 100)]; }
      function place(p) { var q = pos(p); dev.style.left = q[0] + '%'; dev.style.top = q[1] + '%'; }
      function wait(ms, id) { return new Promise(function (res, rej) { setTimeout(function () { id === run ? res() : rej(); }, ms); }); }
      function mark(p, mk) { var q = pos(p), i = document.createElement('i'); i.className = 'rx-mark rx-mark--' + mk; i.style.left = q[0] + '%'; i.style.top = q[1] + '%'; marks.appendChild(i); }
      async function play(i, id) {
        var b = btns[i], code = b.dataset.code, mk = b.dataset.mode, pts = AREA_PTS[code] || [areaCenter(code)];
        btns.forEach(function (x) { x.classList.toggle('is-on', x === b); });
        stage.dataset.mode = mk; marks.innerHTML = '';
        hud.innerHTML = '<i class="rx-led rx-led--' + mk + '"></i>' + esc(b.querySelector('b').firstChild.textContent.trim()) + ' · ' + esc(b.querySelector('em').textContent);
        dev.classList.remove('is-press'); dev.classList.add('is-away'); await wait(reduce ? 0 : 450, id);
        place(pts[0]); await wait(reduce ? 0 : 60, id); dev.classList.remove('is-away'); await wait(reduce ? 0 : 650, id);
        for (var n = 0; n < pts.length; n++) {
          if (n) { place(pts[n]); await wait(reduce ? 0 : 520, id); }
          dev.classList.add('is-press'); await wait(reduce ? 0 : 1100, id);
          mark(pts[n], mk); dev.classList.remove('is-press'); await wait(reduce ? 0 : 260, id);
        }
        await wait(1300, id);
      }
      async function loop(start) {
        var id = ++run; cur = start;
        try { while (true) { if (!visible) { await wait(400, id); continue; } await play(cur, id); cur = (cur + 1) % btns.length; } } catch (e) {}
      }
      btns.forEach(function (b, i) { b.addEventListener('click', function () { loop(i); }); });
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: .25 }).observe(stage);
      else visible = true;
      place((AREA_PTS[btns[0] && btns[0].dataset.code] || [[FACE_W * .6, FACE_H * .5]])[0]);
      if (btns.length) loop(0);
    });
  }
  /* opts: { counts, roles:{key:'대표'|'보조'}, mixWith, parts, restart, locked, loginHref } */
  function html(key, opts) {
    opts = opts || {};
    var k = REPORT[key] ? key : 'early';
    var R = REPORT[k];
    var D = dataFor(k, opts.mixWith) || {};
    var counts = opts.counts || sample(k);
    var roles = opts.roles || {};

    var areas = D.areas || [];
    var shotModes = [];
    (D.shots || []).forEach(function (s) { if (shotModes.indexOf(s.mode) < 0) shotModes.push(s.mode); });
    var freq = ((D.frequency || '').match(/주\s*\d+\s*~\s*\d+\s*회/) || [''])[0];
    var stats = '<div class="cku-stats">' +
      (areas.length ? '<div class="cku-stat"><span class="cku-stat-label">집중 관리 부위</span><span class="cku-stat-value">' + areas.length + '곳</span><span class="cku-stat-note">' + esc(areas.map(function (a) { return a.name; }).join(' · ')) + '</span></div>' : '') +
      (D.shotTotal ? '<div class="cku-stat"><span class="cku-stat-label">권장 SHOT</span><span class="cku-stat-value">' + D.shotTotal + '샷</span><span class="cku-stat-note">' + esc(shotModes.join(' · ')) + '</span></div>' : '') +
      (freq ? '<div class="cku-stat"><span class="cku-stat-label">권장 빈도</span><span class="cku-stat-value">' + esc(freq) + '</span></div>' : '') +
    '</div>';

    /* 설문 답변에서 읽힌 노화 신호 — 숫자 없이 상대 길이 (개발 화면 TypeDistribution) */
    var norm = AXES.map(function (a) { return (counts[a[0]] || 0) / a[2]; });
    var top = Math.max.apply(null, norm) || 1;
    var order = AXES.map(function (a, i) { return i; }).sort(function (a, b) { return norm[b] - norm[a]; });
    var dist = '<div class="cku-dist"><p class="cku-dist-title">설문 답변에서 읽힌 노화 신호</p><ul class="cku-dist-list">' +
      order.map(function (i) {
        var a = AXES[i], role = roles[a[0]];
        return '<li' + (role ? ' class="is-on"' : '') + '><span class="cku-dist-name">' + esc(a[1]) + (role ? '<em class="cku-dist-role">' + role + '</em>' : '') + '</span>' +
          '<span class="cku-dist-track" aria-hidden="true"><i data-w="' + Math.round(norm[i] / top * 100) + '"></i></span></li>';
      }).join('') +
      '</ul><p class="cku-dist-note">점수가 아니라 답변에서 읽힌 신호의 상대적인 세기입니다. 막대가 길수록 그 유형의 신호가 자주 나타났다는 뜻이에요.</p></div>';

    var maxShot = Math.max.apply(null, (D.shots || []).map(function (s) { return s.count; }).concat([1]));
    var ingr = D.ingredients || [];

    var shots = D.shots || [];
    var inner = (
      typesStrip(k) + cover(R, stats) + intro(R) +

      /* 집중 케어 부위 — 순위 없이 나란히 */
      (areas.length ? '<section class="cku-card" data-sec="area">' + title('area', '집중 케어가 필요한 부위') +
        (D.areaIntro ? '<p class="rx-lead">' + esc(D.areaIntro) + '</p>' : '') +
        '<div class="rx-areas" style="--n:' + areas.length + '">' + areas.map(function (a) {
          return '<article class="rx-area"><div class="rx-area__zoom" style="' + zoomStyle(a.code) + '" role="img" aria-label="' + esc(a.name) + ' 위치"><i class="rx-area__dot" aria-hidden="true"></i></div>' +
            '<div class="rx-area__txt"><code class="rx-code">' + esc(a.code) + '</code><h4 class="rx-area__name">' + esc(a.name) + '</h4>' +
            (a.pattern ? '<span class="rx-area__pat">' + esc(a.pattern) + '</span>' : '') + '</div></article>';
        }).join('') + '</div>' +
        '<p class="cku-rank-legend"><b>U · M · L · B는?</b> 얼굴을 위(U) · 중앙(M) · 아래(L) · 목(B) 구역으로 나눈 케어클 에이징맵 좌표입니다.</p>' +
        (D.areaText && D.areaText.length ? '<div class="cku-divided">' + paras(D.areaText) + '</div>' : '') +
      '</section>' : '') +

      /* 홈케어 루틴 + 추천 성분 + 생활습관 */
      '<section class="cku-card" data-sec="care">' + title('homecare', '홈케어 루틴 · 추천 성분 · 생활습관') +
        '<div class="rx-care">' +
          '<figure class="rx-care__img"><img src="assets/img/rx-mirror.jpg" alt="거울 앞에서 피부를 살피는 여성" loading="lazy"></figure>' +
          (D.homecare && D.homecare.length ? '<ol class="rx-num">' + D.homecare.map(function (t, i) {
            return '<li><span class="rx-num__no">' + (i + 1) + '</span><p>' + esc(t) + '</p></li>'; }).join('') + '</ol>' : '') +
        '</div>' +
        '<div class="rx-care__grid">' +
          '<div class="rx-care__box" data-ingredients><p class="rx-care__h"><span>추천 성분</span><small>성분을 누르면 설명이 열려요</small></p><div class="cku-chip-row">' +
            ingr.map(function (n) {
              return INGREDIENT_INFO[n]
                ? '<button type="button" class="cku-chip cku-chip-btn" data-ing="' + esc(n) + '" aria-expanded="false">' + esc(n) + '<svg class="cku-chip-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>'
                : '<span class="cku-chip">' + esc(n) + '</span>';
            }).join('') + '</div><div class="cku-chip-detail" data-ing-detail hidden></div></div>' +
          (D.lifestyle && D.lifestyle.length ? '<div class="rx-care__box"><p class="rx-care__h"><span>생활습관 포인트</span></p><ul class="rx-life">' +
            D.lifestyle.map(function (t) { return '<li><span class="rx-life__ico" aria-hidden="true">' + lifeIcon(t) + '</span>' + esc(t) + '</li>'; }).join('') + '</ul></div>' : '') +
        '</div>' +
      '</section>' +

      /* 고주파 기술 + 맞춤 사용법 + SHOT 모드 — 기기 움직임 애니메이션 */
      '<section class="cku-card" data-sec="tech">' + title('shot', '케어클 TECH FIT 맞춤 사용법') +
        (D.rf && D.rf.length ? '<div class="rx-rf rx-rf--text">' +
          '<div class="rx-rf__txt"><p class="rx-kicker">고주파(RF) 기술과 케어클</p>' + paras(D.rf) + '</div></div>' : '') +
        (shots.length ? '<div class="rx-demo" data-demo>' +
          '<div class="rx-demo__stage" data-stage><img class="rx-demo__face" src="assets/img/rx-face.jpg" alt="얼굴 위에서 TECH FIT을 옮겨 가며 누르는 순서" loading="lazy">' +
            '<div class="rx-demo__marks" data-marks aria-hidden="true"></div>' +
            '<div class="rx-demo__dev" data-dev aria-hidden="true"><i class="rx-demo__led"></i><img src="assets/img/cut-device-clean.png" alt=""></div>' +
            '<p class="rx-demo__hud" data-hud aria-live="polite"></p></div>' +
          '<div class="rx-demo__side">' +
            (D.usage && D.usage.length ? '<div class="rx-demo__usage">' + paras(D.usage) + '</div>' : '') +
            '<p class="rx-kicker">부위별 SHOT 가이드 <small>누르면 그 부위를 보여 드려요</small></p>' +
            '<ol class="rx-shots">' + shots.map(function (s, i) {
              return '<li><button type="button" class="rx-shot" data-shot="' + i + '" data-code="' + esc(s.code) + '" data-mode="' + esc(modeKey(s.mode)) + '">' +
                '<span class="rx-shot__no">' + (i + 1) + '</span><span class="rx-shot__body"><b>' + esc(s.name) + ' <code class="rx-code">' + esc(s.code) + '</code></b>' +
                '<em><i class="rx-led rx-led--' + modeKey(s.mode) + '"></i>' + esc(s.mode) + ' · ' + esc(s.dir) + '</em></span><span class="rx-shot__cnt">' + s.count + '<small>샷</small></span></button></li>';
            }).join('') + '</ol>' +
            (D.shotTotal ? '<p class="rx-total"><b>총 ' + D.shotTotal + '샷</b><span>SHOT 모드는 7분 후 자동 종료돼요. 남은 부위가 있으면 다시 켜서 이어 하세요.</span></p>' : '') +
          '</div></div>' : '') +
        (D.order && D.order.length ? '<p class="rx-kicker">관리 순서</p><ol class="rx-order" style="--n:' + D.order.length + '">' + D.order.map(function (t, i) {
          return '<li' + (orderPhoto(t) ? ' class="has-img"' : '') + '>' + (orderPhoto(t) ? '<span class="rx-order__img"><img src="assets/img/' + orderPhoto(t) + '" alt="" loading="lazy"></span>' : '') + '<span class="rx-order__no">' + (i + 1) + '</span><span class="rx-order__t">' + esc(t) + '</span></li>'; }).join('') + '</ol>' : '') +
        (D.frequency ? '<p class="rx-freq"><b>권장 빈도</b>' + esc(D.frequency) + '</p>' : '') +
      '</section>' +

      /* SHOT 이후 마무리 단계 */
      (D.modes && D.modes.length ? '<section class="cku-card">' + title('usage', 'SHOT 이후 마무리 단계') + '<div class="rx-modes">' +
        D.modes.map(function (m) {
          var badge = m.required === true ? '필수' : m.required === false ? '선택' : '';
          var mk = /EMS/.test(m.name) ? 'ems' : 'glow';
          return '<div class="rx-mode rx-mode--text"><div class="rx-mode__txt"><p class="rx-mode__head"><i class="rx-led rx-led--' + mk + '"></i>' + esc(m.name) +
            (badge ? '<span class="rx-badge">' + badge + '</span>' : '') + (m.duration ? '<span class="rx-mode__dur">권장 ' + esc(m.duration) + '</span>' : '') + '</p>' +
            (m.desc ? '<p class="rx-mode__desc">' + esc(m.desc) + '</p>' : '') + '</div></div>';
        }).join('') + '</div></section>' : '') +

      /* AI 맞춤 상담 */
      '<section class="cku-card cku-card-dark">' + title('ai', 'AI 맞춤 상담') +
        '<div class="rx-ai"><p class="rx-ai__who"><span class="rx-ai__av">AI</span><b>careCL AI 피부 에이전트</b><small>설문 결과를 읽고 고객님께 쓴 상담 글</small></p>' +
        (k === 'mixed'
          ? '<div class="cku-ai-answer">' + AI_SAMPLE.map(function (t) { return '<p>' + aiHighlight(esc(t)) + '</p>'; }).join('') + '</div>'
          : '<div class="cku-ai-answer"><p>결과를 바탕으로 AI가 고객님께 쓴 맞춤 상담 글이 이 자리에 들어갑니다. (답변은 결과마다 한 번 만들어 저장돼요.)</p></div>') +
      '</div></section>' +

      /* 혜택 */
      '<section class="cku-card">' + title('coupon', 'AI 분석 결과 고객 전용 혜택') + '<div class="rx-coupons">' +
        '<div class="rx-coupon"><figure class="rx-coupon__img"><img src="assets/img/c-techfit-case.jpg" alt="케이스에 담긴 TECH FIT" loading="lazy"></figure><div class="rx-coupon__txt"><p class="rx-coupon__k">아직 케어클이 없으시다면</p><p class="rx-coupon__t">지금 TECH FIT을 시작하기 좋은 때</p>' +
          '<p class="rx-coupon__price"><s>820,000원</s><b>518,000원</b><span>30% 할인 568,000원 + 첫 구매 쿠폰 5만원</span></p>' +
          '<a class="cku-btn cku-btn-primary" href="products.html">쿠폰 받고 TECH FIT 시작하기</a></div></div>' +
        '<div class="rx-coupon"><figure class="rx-coupon__img"><img src="assets/img/rx-mask-set.jpg" alt="그리드 마스크 TECH FIT 패키지와 낱장 마스크" loading="lazy"></figure><div class="rx-coupon__txt"><p class="rx-coupon__k">이미 케어클을 쓰고 계신다면</p><p class="rx-coupon__t">소모품을 더 알뜰하게</p>' +
          '<p class="rx-coupon__price"><b>20% 할인</b><span>그리드 마스크팩 · 콜라겐 젤 등 소모품 재구매 쿠폰</span></p>' +
          '<a class="cku-btn cku-btn-primary" href="cosmetics.html">소모품 쿠폰 받기</a></div></div>' +
      '</div></section>' +

      '<p class="cku-result-note">' + DISCLAIMER + '</p>' +

      /* 실제 후기 — TECH FIT 사진과 함께 */
      '<section class="cku-card">' + title('review', '비슷한 고민을 가진 고객의 실제 후기') + '<div class="cku-reviews">' +
        '<p class="cku-reviews-lead">케어클을 쓰신 분들이 남긴 실제 구매 후기 중에서, 고객님 결과와 맞닿은 이야기를 담은 글을 골랐습니다.</p><ul class="rx-reviews">' +
        REVIEWS.map(function (r, i) {
          return '<li class="cku-review rx-review"><div class="rx-review__img rx-ph" aria-hidden="true"><span>후기 이미지 자리</span></div><div class="rx-review__txt"><div class="cku-review-head"><span class="cku-review-tagline">' + esc(r.tag) + '</span><span class="cku-review-rating" aria-label="평점 ' + r.rating + '점"><span aria-hidden="true">★</span> ' + r.rating + '</span></div>' +
            '<p class="cku-review-body cku-review-body-clamp">' + esc(r.body) + '</p><button type="button" class="cku-review-more" hidden>더보기</button>' +
            '<p class="cku-review-date">' + esc(r.date) + '</p></div></li>';
        }).join('') +
        '</ul><p class="cku-reviews-note">쇼핑몰에 등록된 구매 후기를 그대로 옮긴 것이며, 내용을 고치지 않았습니다. 후기는 개인의 사용 경험으로 효과를 보장하지 않습니다.</p></div></section>' +

      share() + actions(opts)
    );
    if (!opts.locked) return wrap(inner);

    /* 로그인 전 — 유형 소개까지 보여주고, 그 아래 상세 카드(집중 부위·홈케어)는 흐리게 깔고 잠금 상자를 띄운다 */
    var from = inner.indexOf('<section class="cku-card" data-sec="area">');
    var to = inner.indexOf('<section class="cku-card" data-sec="tech">');
    var preview = from > -1 && to > from ? inner.slice(from, to) : '';
    return wrap(typesStrip(k) + cover(R) + intro(R) +
      '<div class="cku-lock">' +
        '<div class="cku-lock-preview" aria-hidden="true" inert>' + preview + '</div>' +
        '<div class="cku-lock-box" role="region" aria-label="로그인 안내">' +
          '<span class="cku-lock-ico">' + icon('lock') + '</span>' +
          '<p class="cku-lock-title">로그인하면 더 자세한<br>AI 피부 진단을 받을 수 있어요</p>' +
          '<p class="cku-lock-desc">고객님만을 위한 집중 케어 부위, 맞춤 홈케어 루틴, <br>TECH FIT 사용법과 AI 맞춤 상담을 확인해보세요.</p>' +
          '<ul class="cku-lock-list"><li>집중 케어 부위</li><li>홈케어 루틴 · 성분</li><li>TECH FIT 맞춤 사용법</li><li>AI 맞춤 상담</li><li>전용 혜택</li></ul>' +
          '<a class="cku-btn cku-btn-primary cku-lock-btn" href="' + esc(opts.loginHref || '#') + '">로그인하고 전체 결과 보기</a>' +
        '</div>' +
      '</div>' +
      share() + actions(opts));
  }

  /* 그린 다음: 막대 채우기, 긴 후기에만 '더보기' */
  function fillBars(root) {
    root = root || document;
    setTimeout(function () {
      Array.prototype.forEach.call(root.querySelectorAll('.cku-dist-track i'), function (b) { b.style.width = b.dataset.w + '%'; });
      Array.prototype.forEach.call(root.querySelectorAll('.cku-review-body-clamp'), function (p) {
        // line-clamp 상태에선 scrollHeight가 잘린 높이로 나오는 브라우저가 있어, 잠깐 풀어서 잰다
        var more = p.nextElementSibling, h = p.clientHeight;
        p.classList.remove('cku-review-body-clamp');
        var full = p.clientHeight;
        p.classList.add('cku-review-body-clamp');
        if (more && full > h + 1) more.hidden = false;
      });
    }, 120);
    initDemo(root);
  }

  /* 성분 칩 펼치기 · 후기 더보기 · 링크 복사 (한 번에 하나만 펼친다) */
  document.addEventListener('click', function (e) {
    var chip = e.target.closest('[data-ing]');
    if (chip) {
      var box = chip.closest('[data-ingredients]'), detail = box.querySelector('[data-ing-detail]');
      var open = chip.getAttribute('aria-expanded') !== 'true';
      Array.prototype.forEach.call(box.querySelectorAll('[data-ing]'), function (c) { c.setAttribute('aria-expanded', 'false'); c.classList.remove('is-open'); });
      if (open) {
        chip.setAttribute('aria-expanded', 'true'); chip.classList.add('is-open');
        var n = chip.dataset.ing;
        detail.innerHTML = '<p class="cku-chip-detail-name">' + esc(n) + '</p><p class="cku-chip-detail-desc">' + esc(INGREDIENT_INFO[n]) + '</p>';
      }
      detail.hidden = !open;
      return;
    }
    var more = e.target.closest('.cku-review-more');
    if (more) {
      var body = more.previousElementSibling, opened = body.classList.toggle('cku-review-body-clamp');
      more.textContent = opened ? '더보기' : '접기';
      return;
    }
    if (e.target.closest('[data-share]')) { e.preventDefault(); return; }
    var copy = e.target.closest('[data-copy]');
    if (copy && navigator.clipboard) {
      navigator.clipboard.writeText(location.origin + location.pathname).then(function () {
        var s = copy.querySelector('span:last-child'); s.textContent = '복사됐어요'; setTimeout(function () { s.textContent = '링크 복사'; }, 1600);
      });
    }
  });

  window.ckuReport = { data: REPORT, html: html, fillBars: fillBars, sample: sample };
})();
