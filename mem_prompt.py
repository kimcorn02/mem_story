PERSONA_PROMPT = """캐릭터 3명에 대한 자기소개를 아래에 맞춰 파이썬 리스트 형식으로 생성해줘.

도메인: {domain}

## 페르소나
이름, 성별, 나이, 직업, 성격, 주요 관심사를 포함한 간략한 자개소개 한 문단.

## 예시
[{{"김민준": "안녕하세요! 경영학과 24학번, 20살 김민준입니다. 저는 단순히 먹는 즐거움을 넘어 식당의 서비스 프로세스와 가성비, 그리고 식재료의 조화까지 데이터베이스화하는 것을 즐기는 분석적인 성격의 소유자예요. 평소 파인 다이닝의 플레이팅과 미슐랭 가이드 탐독이 주요 관심사이며, 우리 동아리에서도 객관적이고 날카로운 맛 평가를 통해 최고의 맛집 지도를 완성하는 데 기여하고 싶습니다.",
"박소희": "반갑습니다! 체육교육과에 재학 중인 21살 박소희라고 해요. 저는 한 번 꽂힌 메뉴가 있으면 왕복 4시간 거리라도 마다하지 않고 달려가는 에너지 넘치는 행동파입니다. 힙한 노포 맛집을 찾아내고 그곳의 활기찬 분위기를 즐기는 것이 제 인생의 낙이며, 최근에는 전국 팔도 전통주와 안주의 페어링에 푹 빠져 있어요. 동아리원들과 함께라면 세상 끝에 있는 맛집이라도 앞장서서 안내할 준비가 되어 있습니다!",
"이서윤": "반가워요, 시각디자인과 20살 이서윤입니다. 저는 낯을 조금 가리지만 사람들의 이야기를 들어주는 것을 좋아하는 차분하고 다정한 성격이에요. 음식이 나왔을 때의 그 따뜻한 색감을 카메라에 담고 기록하는 푸드 사진 촬영과 브이로그 제작이 제 가장 큰 관심사입니다. 우리 동아리의 미식 활동을 예쁘게 기록해서 모두에게 소중한 추억으로 남겨드리는 '공식 기록원' 역할을 톡톡히 해내고 싶어요."}}]"""

EPISODE_DICT_PROMPT = """아래의 규칙에 맞는 시나리오 목록을 생성해줘. 주요 인물들이 주어지고, 필요시 다른 조연들이 들어가도 돼.

## 규칙
- 아래 유형의 시나리오들을 생성한다.
1. 각자의 페르소나를 잘 보여줄 수 있는 시나리오
2. ToM (1, 2차)에 영향을 받는 시나리오
3. 메모리 업데이트 (e.g., 고양이를 키운다 -> (1년 후) -> 고양이를 키우지 않는다)를 보여주는 시나리오
- 에이전트가 대화할 때 자신이 기억하고 있는 것에 영향을 받아야 함 (기존 대화 후 인터뷰와 같은 데이터셋과 차별화).
- 메모리를 동적으로 활용할 시나리오를 scenario_objectives에 포함시킨다.
- 대화에 영향을 주는 각자의 객관적인 메모리 단서는 memory_evidences에 넣는다.
- 예시와 유사한 형태로 생성하되, 다른 도메인으로 생성한다.
- JSON List 형태로 답한다. 그 외의 내용은 언급하지 않는다.

## 주요 인물들
{persona_list}

## 예시
[ {{ "date": 1, "agents": ["Minho", "Jiwoo", "Sophia"], "scenario": "동아리 신입 부원 환영회", "scenario_objectives": [ "각자 취미와 근황 소개", "Jiwoo가 현재 카페 아르바이트를 하고 있음을 언급", "Sophia가 민트초코를 세상에서 제일 싫어한다고 강하게 발언" ], "memory_evidences": [ "Jiwoo는 '별빛 카페'에서 파트타임으로 일한다.", "Sophia는 민트초코를 극도로 혐오한다." ] }}, {{ "date": 15, "agents": ["Minho", "Sophia"], "scenario": "도서관에서 시험 공부 중 휴식", "scenario_objectives": [ "Minho가 Jiwoo에게 간식을 사주려는데 어디 있는지 Sophia에게 질문", "Sophia가 Jiwoo의 아르바이트 장소를 기억하여 답변" ], "memory_evidences": [ "Minho는 오늘 파란색 줄무늬 셔츠를 입었다." ] }}, {{ "date": 45, "agents": ["Jiwoo", "Sophia"], "scenario": "카페에서의 수다", "scenario_objectives": [ "Jiwoo가 최근 아르바이트를 그만두고 학원 등록을 했다고 알림", "Sophia가 축하하며 본인의 근황 공유" ], "memory_evidences": [ "Jiwoo는 더 이상 카페에서 일하지 않으며, 대신 토익 학원을 다닌다." ] }}, {{ "date": 100, "agents": ["Minho", "Jiwoo", "Sophia"], "scenario": "종강 기념 아이스크림 가게 방문", "scenario_objectives": [ "Minho가 키오스크에서 주문을 담당", "Minho가 Sophia의 취향을 착각하여 민트초코를 고르려 할 때 Jiwoo가 제지", "Minho가 Jiwoo에게 '알바 늦지 않겠냐'고 물어보고 Jiwoo가 업데이트된 상황(퇴사)을 정정" ], "memory_evidences": [ "Sophia는 여전히 민트초코를 싫어하며, Jiwoo가 이를 정확히 기억하고 있다." ] }}, {{ "date": 365, "agents": ["Minho", "Jiwoo"], "scenario": "1년 만의 재회", "scenario_objectives": [ "과거 환영회 때의 추억 회상", "Minho가 1년 전 그날 자신이 무슨 옷을 입었는지 기억나냐고 묻지만 Jiwoo는 사소해서 기억하지 못함", "Sophia가 당시 민트초코 때문에 화냈던 사건을 ToM 관점에서 대화" ], "memory_evidences": [ "Minho는 1년 전 첫 만남 때 파란색 줄무늬 셔츠를 입었으나, 이는 매우 사소한 디테일이다." ] }} ]
"""

RELATION_PROMPT = """Your task is to transform the given memory evidence into a semantic graph represented as a list of relational triplets.
- Extract all explicitly stated, text-supported relationships between entities, without omitting any valid relations mentioned in the input.
- Ensure that each extracted triplet captures a single and contextually accurate relation, using concise and unambiguous relationship phrases faithful to the semantics expressed in the text.
- Avoid inferred, explanatory, or implicit relations that are not explicitly stated.
- 문장에 등장하는 구체적인 수식어나 조건(예: 대상, 장소, 기종명)을 생략하지 마세요.
    - (나쁜 예: {{Minsu, 선언한다, 패셔니스타}})
    - (좋은 예: {{Minsu, 선언한다, 자신이 패셔니스타라고}})
- triplet으로 의미를 전달하기 어려운 경우 추출하지 않는다.
- 가능한 한 하나의 triplet만으로도 문장의 기존 의미가 100% 전달되도록 목적어(Entity2)를 상세히 적으세요.
- 필요 시 하나의 문장에서 여러 개의 triplet을 추출할 수 있다.
- Present the triplets in the format {{Entity1, Relationship (clear term, verb or adjective if possible), Entity2}}.
- agent list {agent_list}에 포함된 인물만 triplet의 entity1로 사용한다.
- 문장이 호불호(좋아한다/싫어한다)를 내포하는 경우 기존 문장과 표현이 다르더라도 relation으로 추출한다.
In your answer, output only the list of triplets and do not include any additional text.

### memory evidence
{memory_evidence}"""

# https://arxiv.org/pdf/2601.15037

REL_TWIST_PROMPT = """## Task
Generate "Antonym Relations" by semantically reversing the meaning of the given relation triplets.

## Guidelines:
1. **Semantic Inversion**:
   - For actions: Find a strong antonym (e.g., "accepts" -> "rejects").
   - For change of state: If the relation describes a change (e.g., "changed", "upgraded"), the reversal should imply **sticking to the original state** or **reverting** (e.g., "maintains original", "remains unchanged").
2. **Clarity in Reversal**:
   - If a simple antonym makes the context ambiguous (e.g., "changed to X" -> "maintained X"?), explicitly state that the **original/former state is preserved**.
   - Example: [{{A, changed, from Phone to Camera}}] -> [{{A, keeps using, the Phone}}] or [{{A, refuses to switch, to Camera}}].
3. **Contextual Consistency**:
   - You may modify the object or the verb phrase to ensure the "meaningful opposite" is clear.
4. **Strict Formatting**:
   - Output ONLY the list: [{{Subject, Reversed_Verb, Object}}].
   - No additional text or explanations.

## Relation to Process:
{relation_list}

## Examples:
Input: [{{Sophia, hates, mint-choco}}]
Output: [{{Sophia, adores, mint-choco}}]

Input: [{{John, builds, a castle}}]
Output: [{{John, destroys, a castle}}]

Input: [{{They, remember, the promise}}]
Output: [{{They, forget, the promise}}]
"""

TWIST_PROMPT = """## Task
입력된 문장의 핵심 의미를 정반대로 반전시킨 "대조적 문장(Antonym Sentences)"을 생성하세요.

## Guidelines:
1. **의미적 반전 (Semantic Inversion)**:
   - 단순히 단어 하나를 바꾸는 것이 아니라, 문장 전체가 나타내는 '상태'나 '사건'의 결과를 정반대로 만드세요.
   - 예: "들었다고 주장한다" -> "들리지 않았다고 확신한다" 또는 "환청임을 인정한다"
2. **심리 및 상태 반전**:
   - 우려/걱정 -> 안심/방관
   - 믿음/주장 -> 부정/의구심
   - 유지/변화 -> 복구/거부
3. **자연스러운 문체 유지**:
   - 반전된 문장도 원래 문장처럼 자연스러운 한국어 문어체 혹은 구어체를 유지해야 합니다.
4. **시제**
   - '오늘', '어제'와 같은 모호한 시제 표현을 사용하지 않는다.
   - 과거 사실을 반박하는 경우에만 Day 00같은 날짜 표현을 사용한다.

5. **출력 형식**:
   - JSON 리스트 형식으로 출력하세요. 
   - 다른 설명 없이 오직 결과 리스트만 반환하세요.

## Input Date:
{date}

## Input Sentences:
{memory_evidences}

## Examples:
Input: Day 40, ["소피는 민트초코를 혐오한다"]
Output: ["소피는 민트초코를 좋아한다"]

Input: Day 12, ["지수는 오늘 프로젝트 결과가 나쁘게 나올까 봐 몹시 불안해하고 있다."]
Output: ["지수는 프로젝트가 완벽하게 마무리되었다고 확신하며 매우 여유로운 태도를 보이고 있다."]

Input: Day 31, ["민지는 오늘 수진이와 밥을 먹었다고 주장한다."]
Output: [민지는 Day 31에 수진이와의 식사 약속을 거절하고 하루 종일 혼자 시간을 보냈다고 말한다.]
"""

REVERSE_PROMPT = """당신은 인물의 일관성과 변화를 정교하게 설계하는 시나리오 작가입니다. 
당신의 작업은 {{day}}의 새로운 정보({{memory_evidence}})를 이전 경험({{former}})과 비교하여, [유지] 또는 [변화]의 맥락에 맞는 에피소드를 만드는 것입니다.

## 핵심 분석 지침:
1. **유지(Consistency)**: 이전에도 그랬고 지금도 그렇다면({{memory_evidence}}에 '유지' 포함), 그 취향이 얼마나 확고한지 보여주는 에피소드를 작성하세요. (ex. 변할 뻔 했지만, 취향이 확고하여 변하지 않았다)
2. **변화(Change)**: 이전 기록과 현재 상태가 다르다면, 그 사이에 어떤 [결정적 사건]이 있었는지 창조하여 개연성을 부여하세요. 
3. **재역전(Reversion)**: 만약 '변했다가 다시 원래대로 돌아온' 경우라면, 왜 일시적 변심을 끝내고 돌아왔는지 그 계기를 서술하세요.

## 시나리오 작성 규칙:
- **대화의 구조**: 등장인물들이 이전 경험({{former}})을 언급하며 "너 저번엔 이랬잖아" 혹은 "넌 역시 변함없구나" 같은 반응을 보이게 하세요.
- **인과관계 명시**: 변화가 있다면 '왜' 변했는지, 유지된다면 '왜' 여전히 고수하는지를 scenario_objectives에 포함하세요.
- **메모리 업데이트**: 변화나 확정된 사실 뒤에 반드시 "(메모리 업데이트)" 또는 "(취향 확인)" 문구를 포함하세요.
- **출력 형식**: 주어진 예시와 같이 JSON List `[ {{...}} ]` 형식만 출력하세요. 출력되는 JSON List에는 date, agents, scenario, scenario objectives, memory evidences 항목만 포함됩니다.

## 데이터:
- 도달해야 할 현재 상태(Memory Evidence): {memory_evidence}
- 발생 시점: {day}
- 이전 기록들(Former Context): {former}

## 예시:
[ {{
   'date': {day}
  'agents': ['민수', '수진'],
  'scenario': '길에서 고양이를 마주친 상황',
  'scenario_objectives': [
    "민수가 고양이를 보고 겁을 먹거나 피하는 모습을 보임",
    "수진이 '너 원래 고양이 귀여워했잖아'라며 의아해함",
    "민수가 예전에 고양이에게 할퀴어 크게 다친 이후로 고양이가 무서워졌다고 고백함 (사건으로 인한 취향 변화 반영)",
    "수진이 민수의 변화된 상태를 이해하고 메모리를 업데이트함"
  ],
  'memory_evidences': ['민수는 고양이에게 할큄 당한 이후로 다시 고양이를 무서워하게 되었다.']
}} ]
"""

AUGMENT_PROMPT = """시나리오 두 개 사이에 들어가는 서브 시나리오들을 생성해줘.

## 규칙
- 타겟 시간대 사이에 들어가는 서브 시나리오들을 생성한다.
- 시나리오 전체 목록과 모순이 있으면 안된다.
- 미래 시간대의 memory_evidences를 언급하거나 뒷받침하는 시나리오와 전혀 관련이 없는 일상 시나리오도 생성한다.
- 시나리오 전체 목록과 같은 JSON List 형태로 답한다. 그 외의 내용은 언급하지 않는다.

## 주요 인물들
### 김민준
안녕하세요! 경영학과 24학번, 20살 김민준입니다. 저는 단순히 먹는 즐거움을 넘어 식당의 서비스 프로세스와 가성비, 그리고 식재료의 조화까지 데이터베이스화하는 것을 즐기는 분석적인 성격의 소유자예요. 평소 파인 다이닝의 플레이팅과 미슐랭 가이드 탐독이 주요 관심사이며, 우리 동아리에서도 객관적이고 날카로운 맛 평가를 통해 최고의 맛집 지도를 완성하는 데 기여하고 싶습니다.
### 박소희
반갑습니다! 체육교육과에 재학 중인 21살 박소희라고 해요. 저는 한 번 꽂힌 메뉴가 있으면 왕복 4시간 거리라도 마다하지 않고 달려가는 에너지 넘치는 행동파입니다. 힙한 노포 맛집을 찾아내고 그곳의 활기찬 분위기를 즐기는 것이 제 인생의 낙이며, 최근에는 전국 팔도 전통주와 안주의 페어링에 푹 빠져 있어요. 동아리원들과 함께라면 세상 끝에 있는 맛집이라도 앞장서서 안내할 준비가 되어 있습니다!
### 이서윤
반가워요, 시각디자인과 20살 이서윤입니다. 저는 낯을 조금 가리지만 사람들의 이야기를 들어주는 것을 좋아하는 차분하고 다정한 성격이에요. 음식이 나왔을 때의 그 따뜻한 색감을 카메라에 담고 기록하는 푸드 사진 촬영과 브이로그 제작이 제 가장 큰 관심사입니다. 우리 동아리의 미식 활동을 예쁘게 기록해서 모두에게 소중한 추억으로 남겨드리는 '공식 기록원' 역할을 톡톡히 해내고 싶어요.

## 타겟 시간대
time Day {start_date}와 time Day {end_date} 사이

## 시나리오 전체 목록
{scenario_list}"""

QA_PROMPT_NOTHING = """당신은 AI 에이전트의 '마음 이론(Theory of Mind)'과 '기억 갱신 능력'을 측정하기 위한 QA 데이터셋 생성기입니다. 
제공되는 에피소드 리스트를 분석하여, 각 에이전트가 어떤 시점에 어떤 정보를 습득했는지 파악하고 질문을 생성하세요.

### 데이터
1. 캐릭터: {agent_name}
2. 이전 메모리(A): {memory_evidence}
3. 반전된 메모리(B): {twisted_memory_evidence}

### 지침
**중요: {agent_name}은/는 두 사건(A, B) 모두에 참여하지 않았으므로, A와 B에 대한 어떠한 정보도 모릅니다.**

1. 질문 생성: {target_evidence}에 대해 묻는 질문을 생성할 것.
2. 기대 답변 작성: **반드시 {agent_name}의 지식 부재 상태를 반영할 것.**
   (예: "모릅니다", "그에 대해 아는 바가 없습니다"...등)
3. 만약 기대 답변에 A나 B의 내용이 포함되면 평가 실패로 간주함.
4. JSON List 형식으로 반드시 단 1개의 질문과 답변 쌍만을 생성할 것.

### 출력 형식
[{{
      "agent_name": {agent_name},
      "question": "...",
      "expected_answer": "..."
}}]
"""

QA_PROMPT_BF = """당신은 AI 에이전트의 '마음 이론(Theory of Mind)'을 측정하기 위한 QA 데이터셋 생성기입니다.

### 데이터
1. 캐릭터: {agent_name}
2. 이전 메모리(A): {memory_evidence}
3. 반전된 메모리(B): {twisted_memory_evidence}

### 지침
**중요: {agent_name}은/는 이전 사건(A)에는 참여했으나, 반전된 사건(B)에는 참여하지 않았습니다.**
1. 지식 상태: {agent_name}은 오로지 A의 내용만 알고 있으며, B의 내용은 전혀 모르는 상태여야 합니다.
2. 질문 생성: {target_evidence}와 관련된 최신 근황에 대해 질문을 생성할 것.
3. 기대 답변 작성: **반드시 {agent_name}이 업데이트된 정보(B)를 모른다는 전제하에, 과거의 지식(A)을 바탕으로 답변을 작성할 것.**
   (예: "여전히 민트초코를 좋아하는 것으로 압니다", "그만뒀다니 무슨 소리인가요?" 등)
4. 만약 답변에 B(그만둠)의 내용이 포함되면 평가 실패(ToM 능력 부족)로 간주함.
5. 반드시 단 1개의 질문과 답변 쌍만을 JSON List 형식으로 생성할 것.

### 출력 형식
[{{
      "agent_name": "{agent_name}",
      "question": "...",
      "expected_answer": "...",
      "evaluation_type": "Past Memory Preservation"
}}]
"""

QA_PROMPT_BOTH = QA_PROMPT_BOTH = """당신은 AI 에이전트의 '기억 갱신 능력'을 측정하기 위한 QA 데이터셋 생성기입니다.

### 데이터
1. 캐릭터: {agent_name}
2. 이전 메모리(A): {memory_evidence}
3. 반전된 메모리(B): {twisted_memory_evidence}

### 지침
**중요: {agent_name}은/는 이전 사건(A)과 반전된 사건(B) 모두에 참여하여 모든 변화 과정을 알고 있습니다.**
1. 지식 상태: {agent_name}은 과거의 상태(A)가 최신의 상태(B)로 변화했음을 인지하고 있어야 합니다.
2. 질문 생성: 과거의 상태(A)와 현재의 상태(B) 사이의 변화나 모순점에 대해 질문을 생성할 것.
3. 기대 답변 작성: **반드시 가장 최신 정보인 B를 바탕으로 답변을 작성할 것.** 과거의 정보(A)는 현재 유효하지 않음을 명시해도 좋습니다.
   (예: "처음엔 좋아했지만, 지금은 싫어합니다", "트라우마를 겪은 뒤 싫어하게 되었습니다" 등)
4. 반드시 단 1개의 질문과 답변 쌍만을 JSON List 형식으로 생성할 것.

### 출력 형식
[{{
      "agent_name": "{agent_name}",
      "question": "...",
      "expected_answer": "...",
      "evaluation_type": "Updated Knowledge Success"
}}]
"""