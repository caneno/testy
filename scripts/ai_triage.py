import json
import sys
import os
from anthropic import Anthropic

def triage_with_claude(file_path):
    # Initialize the Anthropic client
    # It automatically looks for the ANTHROPIC_API_KEY env var
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    with open(file_path, 'r') as f:
        data = json.load(f)

    for finding in data.get('results', []):
        code_snippet = finding['extra']['lines']
        issue_desc = finding['extra']['message']
        
        # Claude excels at technical reasoning
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620", # Or the latest 2026 version
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Review this security finding:\nIssue: {issue_desc}\nCode: {code_snippet}\n\nAssess if this is a True Positive and suggest a fix."
                }
            ]
        )
        print(f"--- CLAUDE ANALYSIS ---")
        print(message.content[0].text)

if __name__ == "__main__":
    triage_with_claude(sys.argv[1])