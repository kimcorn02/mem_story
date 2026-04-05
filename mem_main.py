from mem_prompt import *
from mem_LLM_module import *
from mem_module import *
from mem_models import *
from google import genai
from dotenv import load_dotenv
import os, json

# import model
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model = 'gemini-2.0-flash'

# Settings
# story_id = generate_story_id("sports_car")
story_id = "sports_car_260405_1938_b394"
domain="스포츠카 드라이빙 모임"
max_time_passed = 10
add_twist = False

# custom models
generator = StoryGenerator(client, model, story_id)
QA_generator = QAGenerator(client, model)

# paths
persona_path = f"output/persona.json"
episode_path = f"output/episode.json"
agent_memory_path = f"output/agent_memory.json"
qa_path = f"output/qa.json"

# load persona
persona_data = load_json(persona_path)

if story_id not in persona_data:
    persona_dict = generator.generate_persona(persona_path, domain)
    
else:
    persona_dict = persona_data[story_id]

persona_class_list = generator.generate_persona_class(persona_dict)

# load initial episodes
episode_data = load_json(episode_path)

if story_id not in episode_data:
    episode_list = generator.generate_initial_episode(persona_dict)
    episode_class_list = generator.generate_episode_class(episode_list)
    generator.update_agent_memory_per_episode(episode_class_list, persona_class_list)
    save_episodes(episode_path, story_id, episode_class_list)
else:
    episode_class_list = load_episodes_as_class(episode_path, story_id)
    generator.update_agent_memory_per_episode(episode_class_list, persona_class_list)

# agent memory before twist
agent_mem_list = [{persona.name: persona.memory}for persona in persona_class_list]
save_agent_memory(agent_memory_path, story_id=story_id, agent_mem_list=agent_mem_list)

# add twisted plot
if add_twist == True:
    twisted_date, twisted_episode_class_list = generator.generate_twist(episode_class_list, max_time_passed=max_time_passed)
    generator.reset_agent_memory_after_twist(twisted_date, persona_class_list)
    generator.update_agent_memory_per_episode(twisted_episode_class_list, persona_class_list)
    save_episodes(episode_path, story_id+f"_twisted_{twisted_date}", twisted_episode_class_list)

    # agent memory after twist
    agent_mem_list = [{persona.name: persona.memory}for persona in persona_class_list]
    save_agent_memory(agent_memory_path, story_id=story_id+f"_twisted_{twisted_date}", agent_mem_list=agent_mem_list)
else:
    pass


# QA generation
twisted_story_id = "sports_car_260405_1938_b394_twisted_7"
# twisted_story_id = story_id+f"_twisted_{twisted_date}"
twisted_episode_class_list = load_episodes_as_class(episode_path, twisted_story_id)

qa_list = QA_generator.generate_qa(persona_class_list, twisted_episode_class_list)
save_dict_json(qa_path, story_id, qa_list)