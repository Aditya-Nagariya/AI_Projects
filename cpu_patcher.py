import os

file_path = r"custom_nodes\ComfyUI_NTCosyVoice\cosyvoice\cli\model.py"

def fix_indentation_error():
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"🔧 Repairing syntax in {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    fixed_count = 0
    
    for i, line in enumerate(lines):
        # Check if this line is one of our commented-out FP16 lines
        # and if it is indented (part of a block)
        if line.strip().startswith("# ") and ".half()" in line:
            # We found a commented out line. 
            # We need to check if the PREVIOUS line was an 'if' statement
            if i > 0 and "if " in lines[i-1] and ":" in lines[i-1]:
                # Found the broken structure!
                # Inject 'pass' with the same indentation
                indentation = line[:line.find("#")]
                new_lines.append(f"{indentation}pass  # Fixed IndentationError\n")
                fixed_count += 1
        
        new_lines.append(line)

    if fixed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Fixed {fixed_count} syntax errors.")
    else:
        # Fallback: Just replace the specific known broken strings globally
        print("   Complex scan found nothing, trying force replacement...")
        content = "".join(lines)
        
        replacements = [
            ("# llm_embedding = llm_embedding.half()", "pass # llm_embedding = llm_embedding.half()"),
            ("# speech_embedding = speech_embedding.half()", "pass # speech_embedding = speech_embedding.half()"),
            ("# flow_embedding = flow_embedding.half()", "pass # flow_embedding = flow_embedding.half()"),
        ]
        
        for old, new in replacements:
            if old in content and "pass" not in content.split(old)[0][-10:]:
                content = content.replace(old, new)
                fixed_count += 1
                
        if fixed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {fixed_count} syntax errors (Force Method).")
        else:
            print("⚠️ No syntax errors found to fix.")

if __name__ == "__main__":
    fix_indentation_error()
