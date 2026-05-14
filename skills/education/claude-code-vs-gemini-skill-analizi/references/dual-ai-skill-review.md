# Dual-AI Skill Review Workflow

## When to Use
After collecting multiple skill outputs (from video analysis, research, etc.), send the same context to two different local models for independent evaluation. Compare outputs, merge insights.

## Workflow

### 1. Prepare the context
Collect all SKILL.md content into a single document. Strip YAML frontmatter (keep only the body). Keep under ~8000 chars per model (Qwen context window).

### 2. Create two payloads
Use `json.dumps()` to serialize prompts. Never use manual string concatenation in Python when the Turkish text contains apostrophes.

```python
payload1 = json.dumps({
    'model': 'qwen2.5-coder:7b',
    'prompt': 'Sen CLAUDE CODE'sun... ' + context,
    'stream': False
})
```

**Pitfall:** `'Claude Code'sun'` causes SyntaxError. Always use `json.dumps()`.

### 3. Send to two models
Run sequentially (same GPU) or parallel (if separate GPUs). Qwen2.5-coder:7b handles both prompts in ~30s each.

```python
# Run for model A (Claude Code perspective)
resp1 = urllib.request.urlopen(req1, timeout=180)
# Run for model B (Gemini perspective)
resp2 = urllib.request.urlopen(req2, timeout=180)
```

### 4. Compare outputs
Look for:
- **Agreement**: topics both models emphasized
- **Differences**: what one saw that the other missed
- **Errors**: models confusing Hermes features with their own
- **Coverage gaps**: topics neither addressed

### 5. Synthesize into a master skill
Create a new skill that captures:
- What both agreed on (core knowledge)
- What each contributed uniquely
- What both missed (you add this)

## Known Model Behavior

| Model | Strength | Weakness |
|-------|----------|----------|
| Claude Code (Qwen-simulated) | Deeper analysis, practical suggestions, AIOS understanding | Confuses IDE tools with search engines |
| Gemini (Qwen-simulated) | Feature listing, multi-platform focus, self-awareness of limits | Confuses own capabilities with Hermes features, Turkish quality drops with long input |
