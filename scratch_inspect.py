import json

transcript_path = r"C:\Users\mateu\.gemini\antigravity\brain\9959051c-a021-497c-adbe-fc1640507f10\.system_generated\logs\transcript.jsonl"
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        idx = d.get('step_index', 0)
        if 71 <= idx <= 120:
            tc = d.get('tool_calls', [])
            if tc:
                for c in tc:
                    print(f"Step {idx}: {c['name']}")
                    if c['name'] == 'run_command':
                        print(f"   Cmd: {c['args'].get('CommandLine')[:120]}")
