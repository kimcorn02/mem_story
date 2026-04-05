# mem_story

### 시작하기
```bash
conda env create -f environment.yml
conda activate [환경이름]
```

### ⚙️ Configuration

1. 핵심 환경 설정 (Settings)
코드 상단의 Settings 섹션에서 실험의 기본 조건을 설정합니다.

- story_id: 실험의 고유 식별자입니다.

  - 신규 실험: generate_story_id("주제") 함수를 사용하여 고유 ID 생성.

  - 기존 로드: 기존 생성된 ID 문자열(예: "sports_car_...")을 직접 입력.

- domain: 시나리오 배경 설명 (예: "스포츠카 드라이빙 모임", "고등학교 과학 동아리" 등).

- max_time_passed: 반전 에피소드 추가 시 기존 에피소드와 발생할 수 있는 최대 시간차를 지정합니다.

- add_twist:

  - True: '반전' 에피소드를 생성하고 에이전트의 기억을 업데이트합니다. (story id 뒤에 _twisted_N이 추가됨)

  - False: 초기 시나리오 흐름대로 진행합니다.
---

2. LLM 모델 설정
- model: gemini-2.0-flash

- .env 파일: 프로젝트 루트 디렉토리에 .env 파일을 생성하고 GOOGLE_API_KEY=your_key_here를 반드시 입력해야 합니다.

---

3. 데이터 로드 및 저장 (I/O Paths)
모든 결과물은 output/ 폴더 내에 JSON 형태로 저장됩니다.

- persona.json: 생성된 에이전트들의 성격 및 배경 정보

- episode.json: 시나리오별 에피소드 리스트 (Normal / Twisted 버전 모두 포함)

- agent_memory.json: timestamp별 에이전트들의 기억(Memory) 상태

- qa.json: 최종적으로 생성된 QA set

---
### 🚀 실행 순서
1. domain과 story_id를 설정합니다.

2. add_twist 여부를 결정합니다.

3. 터미널에서 python mem_main.py를 실행합니다