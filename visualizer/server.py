import os
import json
import asyncio
import re
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Elite Squad 2D Live Visualizer")

# Global connected websocket clients
connected_clients: List[WebSocket] = []

# Paths
VISUALIZER_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_PATH = r"C:\Users\pouri\.gemini\antigravity\brain\b000682f-33d6-4b58-80d4-3403c75196b4\.system_generated\logs\transcript.jsonl"

def detect_agent_from_entry(entry: Dict[str, Any]) -> Dict[str, str]:
    """Analyze a transcript step to detect which agent is active."""
    thinking = entry.get("thinking", "") or ""
    content = entry.get("content", "") or ""
    tool_calls = entry.get("tool_calls", []) or []
    
    combined_text = f"{thinking} {content}".lower()
    
    # Check tool calls
    tool_names = [tc.get("name", "") for tc in tool_calls] if isinstance(tool_calls, list) else []
    tool_summaries = [tc.get("summary", "") for tc in tool_calls] if isinstance(tool_calls, list) else []
    tools_str = " ".join(tool_names + tool_summaries).lower()
    full_haystack = f"{combined_text} {tools_str}"

    # Agent Detection Heuristics
    if any(k in full_haystack for k in ["akbar", "seo", "lighthouse", "core web vitals", "inp", "lcp", "cls", "sitemap", "robots.txt", "schema"]):
        return {
            "id": "seo-specialist",
            "name": "اکبر (Akbar)",
            "role": "Lead Technical & Local SEO Architect",
            "icon": "🐺",
            "color": "sky"
        }
    elif any(k in full_haystack for k in ["asghar", "geo", "aeo", "perplexity", "chatgpt", "gemini", "claude", "llms.txt", "princeton", "rag"]):
        return {
            "id": "geo-specialist",
            "name": "اصغر (Asghar)",
            "role": "AI Engine Optimization Architect",
            "icon": "🧠",
            "color": "teal"
        }
    elif any(k in full_haystack for k in ["siroos", "revenue", "cro", "wbso", "paul", "tondeur", "hormozi", "deal", "cash", "money", "hunter"]):
        return {
            "id": "revenue-advisor",
            "name": "سیروس (Siroos)",
            "role": "Chief Revenue Officer & Hunter",
            "icon": "💼",
            "color": "amber"
        }
    elif any(k in full_haystack for k in ["jafar", "copy", "cro-copy", "nextdoor", "hans", "buurtapp", "cialdini", "baymard"]):
        return {
            "id": "cro-copywriter",
            "name": "جعفر (Jafar)",
            "role": "Behavioral Copywriting Architect",
            "icon": "✍️",
            "color": "orange"
        }
    elif any(k in full_haystack for k in ["ghasem", "pricing", "contract", "offerte", "bw", "burgerlijk wetboek", "snn subsidie"]):
        return {
            "id": "pricing-strategist",
            "name": "قاسم (Ghasem)",
            "role": "Pricing & Contracts Strategist",
            "icon": "⚖️",
            "color": "violet"
        }
    elif any(k in full_haystack for k in ["taghi", "qa", "audit", "wcag", "avg", "gdpr", "touch target", "fitts", "nielsen"]):
        return {
            "id": "qa-auditor",
            "name": "تقی (Taghi)",
            "role": "Lead QA & Privacy Auditor",
            "icon": "🔍",
            "color": "rose"
        }
    elif any(k in full_haystack for k in ["jamshid", "ui-ux", "bento", "60fps", "rail", "ogl", "motion", "framer motion", "shader"]):
        return {
            "id": "ui-ux-architect",
            "name": "جمشید (Jamshid)",
            "role": "Design Systems & 60fps Motion",
            "icon": "🎨",
            "color": "fuchsia"
        }
    elif any(k in full_haystack for k in ["azadbakht", "linkedin", "viral", "post", "hook", "storytelling"]):
        return {
            "id": "linkedin-strategist",
            "name": "آقای آزادبخت (Azadbakht)",
            "role": "B2B Growth & Viral Storytelling",
            "icon": "🚀",
            "color": "blue"
        }
    else:
        return {
            "id": "orchestrator",
            "name": "هوشنگ خان (Houshang)",
            "role": "Chief Executive & Orchestrator",
            "icon": "👑",
            "color": "indigo"
        }

def extract_clean_thought(entry: Dict[str, Any]) -> str:
    """Extract a concise 1-line thought or action summary."""
    tool_calls = entry.get("tool_calls", [])
    if tool_calls and isinstance(tool_calls, list) and len(tool_calls) > 0:
        tc = tool_calls[0]
        summary = tc.get("summary") or tc.get("name") or "Executing tool"
        return f"Executing: {summary}"
    
    thinking = entry.get("thinking", "")
    if thinking:
        # Take first sentence or first 120 chars
        first_line = thinking.strip().split("\n")[0]
        if len(first_line) > 130:
            first_line = first_line[:127] + "..."
        return first_line
    
    content = entry.get("content", "")
    if content:
        first_line = content.strip().split("\n")[0]
        if len(first_line) > 130:
            first_line = first_line[:127] + "..."
        return first_line
        
    return "Analyzing operational context..."

@app.get("/")
async def get_index():
    index_file = os.path.join(VISUALIZER_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>Visualizer index.html not found</h1>")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"[WebSocket] Client connected! Total clients: {len(connected_clients)}")

    # Send initial snapshot of last 5 historical events
    try:
        if os.path.exists(TRANSCRIPT_PATH):
            with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            recent_lines = lines[-6:]
            for line in recent_lines:
                try:
                    entry = json.loads(line)
                    agent_info = detect_agent_from_entry(entry)
                    thought = extract_clean_thought(entry)
                    payload = {
                        "type": "agent_history",
                        "stepIndex": entry.get("step_index", 0),
                        "timestamp": entry.get("created_at", ""),
                        "agent": agent_info,
                        "thought": thought,
                        "status": "completed"
                    }
                    await websocket.send_text(json.dumps(payload))
                except Exception:
                    pass
    except Exception as e:
        print("[WebSocket] Error sending historical backlog:", e)

    try:
        while True:
            # Keep connection open and receive any ping from client
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"[WebSocket] Client disconnected. Remaining: {len(connected_clients)}")

async def transcript_tailer():
    """Background task continuously tailing transcript.jsonl and broadcasting events."""
    print("[Tailer] Starting transcript.jsonl monitor...")
    last_pos = 0
    
    # Initialize file pointer to near end
    if os.path.exists(TRANSCRIPT_PATH):
        last_pos = max(0, os.path.getsize(TRANSCRIPT_PATH) - 4000)

    while True:
        try:
            if os.path.exists(TRANSCRIPT_PATH):
                current_size = os.path.getsize(TRANSCRIPT_PATH)
                if current_size > last_pos:
                    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
                        f.seek(last_pos)
                        new_lines = f.readlines()
                        last_pos = f.tell()

                    for line in new_lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                            agent_info = detect_agent_from_entry(entry)
                            thought = extract_clean_thought(entry)
                            
                            payload = {
                                "type": "agent_live_event",
                                "stepIndex": entry.get("step_index", 0),
                                "timestamp": entry.get("created_at", ""),
                                "agent": agent_info,
                                "thought": thought,
                                "status": "active"
                            }
                            msg_str = json.dumps(payload)
                            
                            # Broadcast to all connected clients
                            for client in connected_clients:
                                try:
                                    await client.send_text(msg_str)
                                except Exception:
                                    pass
                        except Exception as parse_err:
                            pass
                elif current_size < last_pos:
                    # File was truncated/rotated
                    last_pos = 0
        except Exception as e:
            print("[Tailer] Error reading transcript:", e)

        await asyncio.sleep(0.5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(transcript_tailer())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
