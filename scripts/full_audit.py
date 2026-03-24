import os
import sys
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def audit_repository(root_dir):
    # Extensions that need to be Scanned
    valid_extensions = ('.go', '.py', '.yaml', '.yml', '.json')
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden folders like .git
        if '.git' in root: continue

        for file in files:
            if file.endswith(valid_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()

                print(f"--- AUDITING FILE: {file} ---")
                
                # THE DISCOVERY PROMPT
                prompt = f"""
                You are a Lead Security Architect. Review the following file: {file}
                
                CONTENT:
                {content}
                
                TASK:
                Ignore standard syntax. Look for LOGICAL VULNERABILITIES:
                1. Broken Access Control.
                2. Insecure Data Handling.
                3. Business Logic Flaws.
                If the file is clean, just say 'File is Secure'.
                """

                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                print(response.content[0].text)

if __name__ == "__main__":
    # In GitHub Actions, the current directory is the root of the repo
    audit_repository(".")