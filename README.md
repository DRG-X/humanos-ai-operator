# HumanOS

HumanOS is an experimental AI operator that uses large language models
and visual perception to control a computer and execute tasks autonomously.

This project explores human-like automation beyond rule-based RPA systems.

## Status
⚠️ Experimental / Research Prototype (Active Development)

The system can perform basic tasks but may occasionally hallucinate actions.
Improving reliability and validation is an active area of work.

## What Works
- High-level task interpretation using LLMs
- Vision-based screen understanding (OCR / UI detection)
- Modular agent architecture (planner, executor, validator)
- OS-level action execution (keyboard / mouse)

## Architecture (High Level)
- Core: loop controller, state manager
- Vision: screen capture, OCR, UI detection
- Planner: prompt logic, action schema
- Executor: mouse, keyboard, system actions
- Validator: success / failure detection

## Tech Stack
- Python
- LLM APIs
- OpenCV / OCR
- OS automation tools

## Roadmap
- Reduce hallucinations with stricter action constraints
- Improve state grounding and validation
- Add better logging and failure recovery

---
Built as a learning-driven systems project.
