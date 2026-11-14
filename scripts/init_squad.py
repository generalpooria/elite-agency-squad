#!/usr/bin/env python3
"""
Elite Autonomous Agency Squad — Project Initializer (CLI)
Installs and configures the 9-specialist multi-agent agency framework into any project.
"""

import os
import sys
import json
import shutil

def main():
    print("=======================================================")
    print("   ELITE AUTONOMOUS AGENCY SQUAD — INITIALIZER v2.0    ")
    print("=======================================================")
    
    target_dir = os.getcwd()
    print(f"\nInitializing in: {target_dir}")
    
    # Prompt user for project basics
    proj_name = input("Enter Project / Business Name (e.g., Acme Agency): ").strip() or "My Agency"
    founder_name = input("Enter Founder / Lead Engineer Name: ").strip() or "Lead Developer"
    domain = input("Enter Primary Domain (e.g., acme.com): ").strip() or "example.com"
    
    # Target paths
    agents_dir = os.path.join(target_dir, ".agents")
    os.makedirs(agents_dir, exist_ok=True)
    
    # Copy template memory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    template_memory = os.path.join(repo_root, "templates", "TEAM_MEMORY.template.md")
    target_memory = os.path.join(agents_dir, "TEAM_MEMORY.md")
    
    if os.path.exists(template_memory) and not os.path.exists(target_memory):
        with open(template_memory, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("[Your Business / Agency Name]", proj_name)
        content = content.replace("[Your Name]", founder_name)
        content = content.replace("https://[your-domain.com]", f"https://{domain}")
        with open(target_memory, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Initialized long-term memory at: {target_memory}")
    
    # Create squad.config.json in project root if missing
    config_path = os.path.join(target_dir, "squad.config.json")
    if not os.path.exists(config_path):
        example_config = os.path.join(repo_root, "squad.config.example.json")
        if os.path.exists(example_config):
            shutil.copy(example_config, config_path)
            print(f"✓ Created squad configuration at: {config_path}")
            
    print("\n[SUCCESS] Elite Autonomous Agency Squad is ready for duty!")
    print("Run your preferred AI agent environment (Antigravity, Claude Code) and prompt:")
    print("  'orchestrator: initiate agency sprint and align all specialists'")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
