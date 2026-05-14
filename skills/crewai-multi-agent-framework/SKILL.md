---
name: crewai-multi-agent-framework
description: "CrewAI ile çoklu AI ajan orkestrasyonu — roller, hedefler, geçmişler, Flows, bellek sistemi, YAML yapılandırma"
version: 1.0
category: autonomous-ai-agents
source: https://youtu.be/hJuPoffsGdc
tags: [crewai, multi-agent, orchestration, python, agents, llm, autonomous]
platforms: [linux, macos, windows]
---

# CrewAI Multi-Agent Framework

Kaynak: https://youtu.be/hJuPoffsGdc

CrewAI: Python'da çoklu AI ajanların takım olarak çalışması için framework. 48K GitHub yıldızı, 100K+ sertifikalı geliştirici.

## Kurulum

```bash
pip install crewai crewai-tools
# Python 3.10+ gerekli
```

## Temel Konseptler

- Agent: rol, hedef, geçmiş, araçlar, LLM
- Crew: ajanların takımı, görevler, süreç
- Task: açıklama, beklenen çıktı, hangi ajan
- Process: sequential, hierarchical, autonomous
- Flow: event-driven orchestration (@start, @listen, @router)
- Memory: short-term, long-term, entity memory

## Basit Ornek

```python
from crewai import Agent, Task, Crew, Process

# Ajanlari tanimla
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find comprehensive information on given topics",
    backstory="You are an expert research analyst with 15 years of experience",
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging content from research findings",
    backstory="You are a skilled technical writer who explains complex topics clearly",
    verbose=True
)

# Gorevleri tanimla
research_task = Task(
    description="Research the latest trends in AI agents for 2026",
    expected_output="A comprehensive research report with key findings",
    agent=researcher
)

writing_task = Task(
    description="Write a blog post based on the research",
    expected_output="A 1000-word blog post ready for publication",
    agent=writer
)

# Crew olustur
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential  # sirayla calisir
)

# Calistir
result = crew.kickoff(inputs={"topic": "AI agent frameworks"})
print(result)
```

## YAML Yapilandirma

```yaml
# agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Find comprehensive information"
  backstory: "Expert research analyst"
  verbose: true

writer:
  role: "Content Writer"
  goal: "Create engaging content"
  backstory: "Skilled technical writer"
  verbose: true
```

```yaml
# tasks.yaml
research_task:
  description: "Research the latest trends in {{topic}}"
  expected_output: "Comprehensive research report"
  agent: researcher

writing_task:
  description: "Write a blog post about {{topic}}"
  expected_output: "1000-word blog post"
  agent: writer
```

## CLI Kullanimi

```bash
# Proje olustur
crewai create crew my_project

# Calistir
crewai run

# Scaffold: agents.yaml, tasks.yaml, crew.py, tools/, .env
```

## Flows (Event-Driven Orchestration)

```python
from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel

class MyState(BaseModel):
    result: str = ""

class MyFlow(Flow[MyState]):
    @start()
    def begin(self):
        self.state.result = "starting"
        return "research"

    @listen(begin)
    def research_phase(self, input_data):
        self.state.result = f"Researching: {input_data}"
        return "write"

    @router(research_phase)
    def check_quality(self):
        if "good" in self.state.result:
            return "publish"
        return "revise"

flow = MyFlow()
flow.kickoff()
```

## Bellek Sistemi

```python
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # short-term + long-term + entity memory
    memory_config={
        "short_term": {"retention": 10},
        "long_term": {"enabled": True},
        "entity_memory": {"enabled": True}
    }
)
```

## Process Turleri

| Process | Aciklama |
|---------|----------|
| sequential | Gorevler sirayla calisir, her biri oncekinin ciktisini kullanir |
| hierarchical | Yonetici ajan plan yapar, digerlerine delege eder |
| autonomous | Ajanlar kendi stratejilerini belirler |

## Enterprise (CrewAI AMP)

- Free: 50 execution/ay
- Pro: $25/ay
- Enterprise: ozel fiyatlandirma
- Gercek zamanli tracing ve observability
- VPC secenegi
- Cloud deployment

## Ipuclari

- Backstory onemli: ajanin kararlarini sekillendirir
- Task'ler birbirine context olarak referans verebilir
- Flow'lar Crew'lerden daha detayli kontrol saglar
- Yaml ile developer olmayanlar da ajan tanimlayabilir
- Benchmark: rakiplerinden 2-3x daha hizli
- MIT lisansi
