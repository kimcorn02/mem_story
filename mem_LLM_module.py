import re
from mem_prompt import *
import ast
import random

### LLM modules

def make_persona(client, model, domain=str):
    response = client.models.generate_content(model=model, 
                                              contents=PERSONA_PROMPT.format(domain=domain))
    return response.text

def make_episode_w_relation(model, episode_dict = dict, agent_list=list):
    rel_dict = {}
    relation_list = []

    days = list(episode_dict.keys())
    for day in days:
        eps = episode_dict[day]
        mem_evidence = " ".join(eps['memory_evidences'])

        eps_tmp = eps.copy()
        response = model.generate_content(RELATION_PROMPT.format(agent_list=", ".join(agent_list), 
                                                                 memory_evidence=mem_evidence))
        
        found_sets = re.findall(r'\{(.*?)\}', response.text)
        if not found_sets:
            print(f"Wrong answer format: no sets are found. (LLM Response: {response.text[:50]}...)")
            raise ValueError("")
        
        current_eps_relations = []
        for s in found_sets:
            elements = [e.strip() for e in s.split(',')]
            current_eps_relations.append(elements)
            relation_list.append(elements)
        eps_tmp['triplets'] = current_eps_relations

        rel_dict[day] = eps_tmp
    
    return rel_dict, relation_list

# def reverse_triplet()