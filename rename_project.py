import os

target_dir = r"C:\Users\HP\.gemini\antigravity-ide\scratch\medismart-ai"
extensions = [".html", ".py", ".md", ".txt", ".json", ".css"]

modified_files = []

for root, dirs, files in os.walk(target_dir):
    # Skip .venv and .git
    if any(skip in root for skip in [".venv", ".git", "__pycache__", ".pytest_cache"]):
        continue
    for file in files:
        if file in ["rename_project.py", "convert_to_word.py"]:
            continue
        ext = os.path.splitext(file)[1].lower()
        if ext in extensions:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                if "MediSmart" in content or "medismart" in content:
                    new_content = content
                    # Exact brand replacements
                    new_content = new_content.replace('MediSmart<span class="brand-ai-badge">AI</span>', 'Pharma<span class="brand-ai-badge">AI</span>')
                    new_content = new_content.replace('MediSmart <span style="color: var(--emerald-400);">AI</span>', 'Pharma<span style="color: var(--emerald-400);">AI</span>')
                    new_content = new_content.replace("MediSmart AI", "PharmaAI")
                    new_content = new_content.replace("MediSmart", "PharmaAI")
                    
                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        modified_files.append(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"Successfully updated {len(modified_files)} files with PharmaAI:")
for mf in modified_files:
    print(" -", os.path.relpath(mf, target_dir))
