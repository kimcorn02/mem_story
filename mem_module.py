import json
import datetime
import uuid
import secrets
from dataclasses import is_dataclass, asdict
from mem_models import Episode
from typing import List, Dict, Optional

def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
        print(f"Opened {path}")
    return data

def save_dict_json(path, story_id, new_data):
    data = load_json(path)
    data[story_id] = new_data

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Successfully saved new data in {path}")


def save_episodes(path, story_id, episodes):
    """
    Episode 객체 리스트를 JSON 파일의 특정 story_id 키에 저장합니다.
    """
    # 1. Episode 객체들을 딕셔너리 형태로 변환
    # (Pydantic 모델은 .model_dump()를 사용하고, 일반 dict면 그대로 둡니다)
    serializable_episodes = [
        ep.model_dump() if hasattr(ep, 'model_dump') else ep 
        for ep in episodes
    ]

    # 2. 기존 파일 데이터 불러오기
    try:
        with open(path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    # 3. 해당 story_id 데이터 업데이트
    all_data[story_id] = serializable_episodes

    # 4. 파일 쓰기 (한글 깨짐 방지 및 들여쓰기 적용)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ {story_id} 에피소드 저장 완료! (총 {len(serializable_episodes)}개)")

def load_episodes_as_class(path, story_id):
    """
    JSON 파일에서 특정 story_id의 데이터를 읽어 Episode 객체 리스트로 변환합니다.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        # 1. 해당 story_id의 딕셔너리 리스트 가져오기
        raw_episodes = all_data.get(story_id, [])
        
        # 2. 딕셔너리를 Episode 객체로 변환
        # **ep는 딕셔너리의 키-값을 클래스의 인자로 풀어헤쳐 전달합니다.
        episode_objects = [Episode(**ep) for ep in raw_episodes]
        
        print(f"📂 {story_id} 에피소드 로드 완료! (객체 {len(episode_objects)}개)")
        return episode_objects

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ 파일 로드 실패: {e}")
        return []
    
def save_agent_memory(path: str, story_id: str, agent_mem_list: List[dict]):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}
    
    all_data[story_id] = agent_mem_list

    # 4. 파일 쓰기 (한글 깨짐 방지 및 들여쓰기 적용)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ {story_id} agent memory 저장 완료! (총 {len(agent_mem_list)}개)")

def clean_json_response(raw_text):
    clean_text = raw_text.replace("```json", "").replace("```", "").strip()
    return clean_text

def generate_story_id(prefix="story"):
    now = datetime.datetime.now().strftime("%y%m%d_%H%M")
    # 짧은 랜덤 문자열 (4글자) - 중복 방지용
    random_suffix = secrets.token_hex(2) 
    
    return f"{prefix}_{now}_{random_suffix}"