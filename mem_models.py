from mem_prompt import *
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import uuid
import random
import re

class Persona(BaseModel):
    story_id: str
    persona_id: str
    name: str
    traits: str
    memory: List = []

    def update_memory(self, timestamp: int, new_memory: List):
        exists = any(timestamp in m for m in self.memory)
        
        if not exists:
            self.memory.append({timestamp: new_memory})

    def reset_memory(self, target_timestamp: int):
        self.memory = [
            m for m in self.memory 
            if list(m.keys())[0] <= target_timestamp
        ]

class Episode(BaseModel):
    story_id: str
    date: int
    scenario: str
    agents: List = []
    scenario_objectives: List = []
    memory_evidences: List = []
    reversed_from: Optional[int] = None

class StoryGenerator:
    def __init__(self, client, model, story_id):
        self.client = client
        self.model = model
        self.story_id = story_id

    def json_parser(self, raw_text):
        if raw_text[:7] == "```json":
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        elif raw_text[:9] == "```python":
            clean_text = raw_text.replace("```python", "").replace("```", "").strip()
        else:
            clean_text = raw_text
        
        try:
            data_list = json.loads(clean_text)
            return data_list
        except (json.JSONDecodeError, IndexError):
            print("JSON parsing err")
            return []   

    def generate_persona(self, persona_path: str, domain: str, max_retries: int = 3):
        from mem_module import save_dict_json
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=PERSONA_PROMPT.format(domain=domain)
                )
                persona_dict = self.json_parser(response.text)[0]
                save_dict_json(persona_path, self.story_id, persona_dict)
                return persona_dict
            
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    print(f"Final failure for story_id: {self.story_id}")
                    return None
        
    
    def generate_persona_class(self, persona_dict):
        personas = []
        for name, traits in persona_dict.items():
            # print('n',name,'t',traits)
            new_persona = Persona(
                story_id=self.story_id,
                persona_id=f"{self.story_id}_{uuid.uuid4().hex[:6]}",
                name=name,
                traits=traits,
                memory=[])
            personas.append(new_persona)
        return personas

    def generate_initial_episode(self, agent_list):
        response = self.client.models.generate_content(
            model=self.model, 
            contents=EPISODE_DICT_PROMPT.format(persona_list=agent_list)
        )

        episode_list = self.json_parser(response.text)

        return episode_list
    
    def generate_episode_class(self, episode_list: List[dict]) -> List[Episode]:
        episodes = []

        for ep_dict in episode_list:
            new_episode = Episode(
                story_id=self.story_id,
                date=int(ep_dict.get('date', 0)),
                scenario=ep_dict.get('scenario', ''),
                agents=ep_dict.get('agents', []),
                scenario_objectives=ep_dict.get('scenario_objectives', []),
                memory_evidences=ep_dict.get('memory_evidences', []),
                reversed_from=None
            )
            episodes.append(new_episode)

        return episodes
    
    def update_agent_memory_per_episode(self, episode_class_list: List[Episode], agent_class_list: List[Persona]):
        for episode in episode_class_list:
            timestamp = episode.date
            active_agents = episode.agents
            memory_evidences = episode.memory_evidences

            for agent in agent_class_list:
                if agent.name in active_agents:
                    agent.update_memory(timestamp, memory_evidences)
                else:
                    pass

    def reset_agent_memory_after_twist(self, target_timestamp: int, agent_class_list: List[Persona]):
        for agent in agent_class_list:
            agent.reset_memory(target_timestamp)
    
    def generate_twist(self, episodes, max_time_passed):
        target_episode = random.choice(episodes)
        target_memory = random.choice(target_episode.memory_evidences)

        truncated_episodes = episodes.copy()
        truncated_episodes = [episode for episode in truncated_episodes if episode.date <= target_episode.date]

        response = self.client.models.generate_content(
            model=self.model, 
            contents=TWIST_PROMPT.format(date=target_episode.date,
                                         memory_evidences=target_memory)
        )
        reversed_mem = self.json_parser(response.text)

        # generating new twisted data
        time_passed = random.randint(1, max_time_passed)

        response = self.client.models.generate_content(
            model=self.model, 
            contents=REVERSE_PROMPT.format(memory_evidence = reversed_mem,
                                           day = target_episode.date + time_passed,
                                           former = truncated_episodes
                                           )
        )
        twisted_episode = self.json_parser(response.text)

        print('tw',twisted_episode)

        twisted_episode_class = self.generate_episode_class(twisted_episode)
        twisted_episode_class[0].reversed_from = target_episode.date

        truncated_episodes.extend(twisted_episode_class)
        return target_episode.date, truncated_episodes
    
class QAGenerator:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def json_parser(self, raw_text):
        if raw_text[:7] == "```json":
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        elif raw_text[:9] == "```python":
            clean_text = raw_text.replace("```python", "").replace("```", "").strip()
        else:
            clean_text = raw_text
        
        try:
            data_list = json.loads(clean_text)
            return data_list
        except (json.JSONDecodeError, IndexError):
            print("JSON parsing err")
            return []   
    
    def generate_qa(self, agent_list: List[Persona], twisted_episode_class_list: List[Episode]):
        qa_list = []

        episode_bf = twisted_episode_class_list[-2]
        episode_af = twisted_episode_class_list[-1]
        
        set_bf = episode_bf.agents
        set_af = episode_af.agents
        
        for agent in agent_list:
            # print('name',agent.name)
            name = agent.name
            
            # A. 둘 다 참여 안 한 경우 (bf에도 없고 af에도 없음)
            if name not in set_bf and name not in set_af:
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=QA_PROMPT_NOTHING.format(agent_name = name,
                                                        memory_evidence = episode_bf.memory_evidences,
                                                        twisted_memory_evidence = episode_af.memory_evidences,
                                                        target_evidence = episode_af.memory_evidences)
                )

                tmp_qa = self.json_parser(response.text)
                # print('tmp', tmp_qa)
                tmp_qa[0]["type"] = "none"
                tmp_qa[0]["evidence"] = episode_af.memory_evidences

                qa_list.append(tmp_qa)
                
                
            # B. 이전 사건에는 있었으나, 이후(twist) 사건에는 없는 경우
            elif name in set_bf and name not in set_af:
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=QA_PROMPT_BF.format(agent_name = name,
                                                        memory_evidence = episode_bf.memory_evidences,
                                                        twisted_memory_evidence = episode_af.memory_evidences,
                                                        target_evidence = episode_af.memory_evidences)
                )

                tmp_qa = self.json_parser(response.text)
                # print('tmp', tmp_qa)
                tmp_qa[0]["type"] = "bf"
                tmp_qa[0]["evidence"] = episode_af.memory_evidences

                qa_list.append(tmp_qa)
                
            # C. 이전 사건과 이후 사건 모두 참여한 경우
            elif name in set_bf and name in set_af:
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=QA_PROMPT_BOTH.format(agent_name = name,
                                                        memory_evidence = episode_bf.memory_evidences,
                                                        twisted_memory_evidence = episode_af.memory_evidences)
                )

                tmp_qa = self.json_parser(response.text)
                # print('tmp', tmp_qa)
                tmp_qa[0]["type"] = "both"
                tmp_qa[0]["evidence"] = episode_af.memory_evidences

                qa_list.append(tmp_qa)
                
                
            # D. (예외 케이스) 만약 이전엔 없었는데 이후(twist)에만 나타난 경우
            elif name not in set_bf and name in set_af:
                pass
        
        # print(qa_list)
        return qa_list

        

        