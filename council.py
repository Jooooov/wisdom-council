#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════╗
║          HIS DARK MATERIALS — WISDOM COUNCIL v3                       ║
║          council.py — Unified CLI entry point                         ║
╚═══════════════════════════════════════════════════════════════════════╝

Double-click launch.command to open in Terminal.
Or run directly: python3 council.py
"""

import os
# Fix OpenMP duplicate lib conflict (numpy + mlx on macOS)
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import asyncio
import json
import re
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Project root on sys.path ─────────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  COLOURS & FORMATTING                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

GOLD   = "\033[33m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
RED    = "\033[31m"
BLUE   = "\033[34m"
GREY   = "\033[90m"
WHITE  = "\033[97m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

W = 72   # menu width


def clr():
    os.system("clear")


def _bar(title, width=W):
    return f"\n  {GOLD}{BOLD}{title}{RESET}"


def _sep(width=W):
    print(f"  {GREY}{'·' * (width - 2)}{RESET}")


def _line(char="─", width=W):
    print(f"  {GREY}{char * (width - 2)}{RESET}")


def _opt(key, icon, name, desc=""):
    key_str  = f"{GREY}[{key}]{RESET}"
    name_str = f"{CYAN}{BOLD}{name}{RESET}"
    desc_str = f"  {GREY}{desc}{RESET}" if desc else ""
    print(f"  {key_str}  {icon}  {name_str}{desc_str}")


def _ask(prompt, default=None):
    hint = f" {GREY}(Enter for: {default}){RESET}" if default else ""
    try:
        raw = input(f"\n  {CYAN}›{RESET} {prompt}{hint}: ").strip()
        return raw if raw else default
    except (KeyboardInterrupt, EOFError):
        return None


def _pause():
    try:
        input(f"\n  {GREY}Press ENTER to continue…{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


def _ok(msg):    print(f"\n  {GREEN}✓  {msg}{RESET}")
def _err(msg):   print(f"\n  {RED}✗  {msg}{RESET}")
def _info(msg):  print(f"\n  {BLUE}ℹ  {msg}{RESET}")
def _warn(msg):  print(f"\n  {GOLD}⚠  {msg}{RESET}")
def _agent(name, msg): print(f"\n  {CYAN}{name}{RESET}  {msg}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MOTIVATIONAL CONTENT                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

QUOTES = [
    ("Lyra",        "Every answer opens another question. Keep going."),
    ("Iorek",       "True strength is moving forward even when the outcome is uncertain."),
    ("Mrs. Coulter","The greatest risk is not taking one."),
    ("Will",        "You do what needs to be done. No more, no less."),
    ("Lord Asriel", "We are building something that has never existed before."),
    ("Mary Malone", "Pay attention to the signal. The pattern will emerge."),
    ("Serafina",    "See far. The horizon is always further than you think."),
    ("Lee",         "Every great journey starts with one honest step forward."),
    ("Coram",       "Experience is what remains after everything else has faded."),
]

START_MESSAGES = [
    "The council is assembled. Let's build something great today.",
    "Your team is ready. Every analysis brings us closer to the goal.",
    "The Dust flows through the work. Let's make it count.",
    "Another day, another opportunity to move the needle.",
    "Small steps compound. The council is here for every one of them.",
    "Let's turn ideas into decisions, and decisions into wealth.",
    "You and the council — the world won't know what hit it.",
]

MILESTONE_MESSAGES = {
    1:   "First analysis done! The journey of a thousand insights begins here.",
    5:   "5 analyses complete. The team is finding its rhythm!",
    10:  "10 analyses. The council is learning fast.",
    25:  "25 analyses. Patterns are emerging in the data.",
    50:  "50 analyses! Half-century. The council is battle-hardened.",
    100: "100 analyses. The council has seen almost everything.",
}


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  STATUS HELPERS (no model loading)                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def _get_ram() -> str:
    try:
        import psutil
        gb = psutil.virtual_memory().available / (1024 ** 3)
        pct = psutil.virtual_memory().percent
        if gb >= 6:   c = GREEN
        elif gb >= 3.5: c = GOLD
        else:           c = RED
        return f"{c}● RAM {gb:.1f}GB free ({pct:.0f}% used){RESET}"
    except Exception:
        return f"{GREY}● RAM n/a{RESET}"


def _get_analyses_count() -> int:
    p = Path.home() / ".mcts_reasoning" / "explored_paths.jsonl"
    if not p.exists():
        return 0
    try:
        return sum(1 for _ in open(p))
    except Exception:
        return 0


def _get_status_bar() -> str:
    ram = _get_ram()
    count = _get_analyses_count()
    mem_str = f"{CYAN}📚 {count} analyses{RESET}"
    agent_str = f"{GREEN}⚡ 8 agents{RESET}"
    return f"  {ram}   {agent_str}   {mem_str}"


def _check_milestone(count: int):
    if count in MILESTONE_MESSAGES:
        print(f"\n  {GOLD}★  {MILESTONE_MESSAGES[count]}{RESET}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  BANNER                                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def print_banner(quote=True):
    clr()
    q_agent, q_text = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %b %Y  %H:%M")

    print(f"\n{GOLD}{BOLD}")
    print("  ╔═══════════════════════════════════════════════════════════════════╗")
    print("  ║                                                                   ║")
    print("  ║        ✦   HIS DARK MATERIALS — WISDOM COUNCIL v3   ✦            ║")
    print("  ║                                                                   ║")
    print("  ║   Qwen3-8B/4B · MCTS Reasoning · 8 Agents · Built for YOU         ║")
    print("  ║                                                                   ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════════╝{RESET}")

    if quote:
        print(f"\n  {GREY}❝ {q_text} ❞{RESET}")
        print(f"  {GREY}      — {q_agent}{RESET}")

    msg = random.choice(START_MESSAGES)
    print(f"\n  {GOLD}{msg}{RESET}")
    print(f"  {GREY}{now}{RESET}")
    print()
    print(_get_status_bar())
    _line()

    count = _get_analyses_count()
    _check_milestone(count)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MAIN MENU                                                               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def show_main_menu():
    print_banner()

    print(_bar("  MISSION CONTROL"))
    _opt("1", "⚡", "Quick Analysis",    "— describe any idea → full MCTS tree in ~30 min")
    _opt("2", "⚔️ ", "War Room",          "— 8 agents debate a real project (LLM-powered)")
    _opt("3", "📁", "My Projects",       "— list + deep-analyse an existing project")

    print()
    print(_bar("  DEEP REASONING ENGINE"))
    _opt("4", "🎯", "Business Viability","— go/no-go · financial model · risk map")
    _opt("5", "🧠", "Validate an Idea",  "— quick feasibility + confidence score")
    _opt("6", "🌲", "Continue Analysis", "— resume a tree search from previous session")

    print()
    print(_bar("  TEAM & KNOWLEDGE"))
    _opt("7", "👥", "Meet the Team",     "— agent profiles · roles · learning progress")
    _opt("8", "📊", "Memory & Patterns", "— what the council has learned together")
    _opt("9", "🔍", "Search Analyses",   "— find insights from past sessions")

    print()
    print(_bar("  SYSTEM"))
    _opt("s", "💻", "System Status",     "— RAM · model · storage · agent scores")
    _opt("h", "📖", "Help",              "— how to use the council")
    _opt("q", "🚪", "Exit",              "")

    _line()
    return _ask("Choose")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  1 — QUICK ANALYSIS                                                      ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_quick_analysis():
    clr()
    print(f"\n{GOLD}{BOLD}  ⚡ QUICK ANALYSIS{RESET}")
    _line()
    print(f"  {GREY}The council will generate 4 strategic approaches, score each one,")
    print(f"  expand the best 2, and give you a GO/NO-GO with financial projections.{RESET}\n")

    idea = _ask("Describe your idea (be specific — the more detail, the better)")
    if not idea:
        _err("No idea entered. Returning to menu.")
        _pause()
        return

    btype = _ask("Business type", "SaaS")
    budget = _ask("Available budget", "$50,000")

    print(f"\n  {CYAN}Starting MCTS analysis…{RESET}")
    print(f"  {GREY}This takes 20-60 min depending on tree depth. Model loads first.{RESET}\n")

    _run_mcts(idea=idea, business_type=btype, budget=budget, reset=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  2 — WAR ROOM                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_war_room_menu():
    clr()
    print(f"\n{GOLD}{BOLD}  ⚔️  WAR ROOM — 8 Agents Debate Your Project{RESET}")
    _line()
    print(f"  {GREY}The council will analyse your project with deep LLM reasoning.")
    print(f"  Each agent speaks in character. You get a consensus + recommendation.{RESET}\n")

    try:
        from run import WisdomCouncil
        council = WisdomCouncil()
    except Exception as e:
        _err(f"Could not load WisdomCouncil: {e}")
        _pause()
        return

    projects = council.project_finder.find_all_projects(merge_duplicates=True)

    if not projects:
        _err("No projects found.")
        print(f"  {GREY}Ensure you have projects in ~/Obsidian-Vault/ or ~/Desktop/apps/{RESET}")
        _pause()
        return

    print(f"  {GREEN}Found {len(projects)} project(s):{RESET}\n")
    for i, p in enumerate(projects, 1):
        src = p.get("source", "?")
        tag = f"{GREY}[{src}]{RESET}"
        print(f"  [{i}] {CYAN}{p['title']}{RESET} {tag}")
        desc = p.get("description", p.get("obsidian_project", {}).get("description", ""))
        if desc:
            print(f"       {GREY}{str(desc)[:65]}{RESET}")

    print(f"  [0] {GREY}↩ Back{RESET}\n")

    choice = _ask("Select project number")
    if not choice or choice == "0":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            project = projects[idx]
            print(f"\n  {GOLD}Launching War Room for: {project['title']}{RESET}")
            print(f"  {GREY}Agents assembling…{RESET}\n")
            council.work_on_project(project)
            _ok(f"Analysis of '{project['title']}' complete.")
        else:
            _err("Invalid number.")
    except ValueError:
        _err("Enter a number.")

    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  3 — MY PROJECTS                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_projects_menu():
    clr()
    print(f"\n{GOLD}{BOLD}  📁 MY PROJECTS{RESET}")
    _line()

    try:
        from run import WisdomCouncil
        council = WisdomCouncil()
    except Exception as e:
        _err(f"Could not load WisdomCouncil: {e}")
        _pause()
        return

    while True:
        clr()
        print(f"\n{GOLD}{BOLD}  📁 MY PROJECTS{RESET}")
        _line()

        projects = council.project_finder.find_all_projects(merge_duplicates=True)

        if not projects:
            _err("No projects found.")
            _pause()
            return

        merged  = [p for p in projects if p["source"] == "MERGED"]
        obsidian= [p for p in projects if p["source"] == "Obsidian"]
        apps    = [p for p in projects if p["source"] == "Apps"]

        counter = 1
        all_listed = []

        if merged:
            print(f"  {GREEN}★ MERGED (Obsidian + Code — fully enriched){RESET}")
            for p in merged:
                out = "  📊" if p.get("has_outputs") else ""
                print(f"  [{counter}]  {CYAN}{p['title']}{RESET}{out}")
                desc = p.get("obsidian_project", {}).get("description", "")
                if desc:
                    print(f"         {GREY}{str(desc)[:60]}{RESET}")
                all_listed.append(p)
                counter += 1

        if obsidian:
            print(f"\n  {BLUE}📖 OBSIDIAN ONLY{RESET}")
            for p in obsidian:
                print(f"  [{counter}]  {CYAN}{p['title']}{RESET}")
                if p.get("description"):
                    print(f"         {GREY}{p['description'][:60]}{RESET}")
                all_listed.append(p)
                counter += 1

        if apps:
            print(f"\n  {GREY}💻 CODE ONLY{RESET}")
            for p in apps:
                out = "  📊" if p.get("has_outputs") else ""
                print(f"  [{counter}]  {CYAN}{p['title']}{RESET}{out}")
                if p.get("description"):
                    print(f"         {GREY}{p['description'][:60]}{RESET}")
                all_listed.append(p)
                counter += 1

        print(f"\n  [0]  {GREY}↩ Back to main menu{RESET}")
        _line()

        choice = _ask("Select project number to analyse")
        if not choice or choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_listed):
                project = all_listed[idx]
                _project_actions(council, project)
            else:
                _err("Invalid number.")
                time.sleep(1)
        except ValueError:
            _err("Enter a number.")
            time.sleep(1)


def _project_actions(council, project):
    while True:
        clr()
        print(f"\n{GOLD}{BOLD}  📁 {project['title'].upper()}{RESET}")
        _line()
        src = project.get("source", "?")
        print(f"  {GREY}Source: {src}{RESET}")
        if project.get("description"):
            print(f"  {GREY}{str(project['description'])[:80]}{RESET}")
        print()

        has_manual = project.get("has_manual_input") or project.get("obsidian_project", {}).get("has_manual_input")
        _opt("1", "⚔️ ", "War Room Analysis",    "— 8 agents deep-dive with LLM reasoning")
        _opt("2", "⚡", "MCTS Quick Analysis",   "— tree search on this project's core idea")
        _opt("3", "📊", "View Past Outputs",     "— browse previous analysis results")
        if has_manual:
            _opt("4", "✂️ ", "Optimise Context",  "— compress Manual Inputs to save tokens (LLM rewrites)")
        _opt("0", "↩ ", "Back",                  "")
        _line()

        choice = _ask("Choose")

        if choice == "1":
            print(f"\n  {GOLD}Launching War Room…{RESET}")
            council.work_on_project(project)
            _ok("Analysis complete.")
            _pause()

        elif choice == "2":
            # Use content_sample as the base idea; full project passed so _run_mcts
            # can prepend Manual Inputs and tag the output file with the project name.
            idea = (
                project.get("content_sample")
                or project.get("obsidian_project", {}).get("content_sample")
                or project.get("apps_project", {}).get("content_sample")
                or project.get("description")
                or project["title"]
            )
            _run_mcts(idea=str(idea)[:300], business_type="project",
                      budget="Unknown", reset=True, project=project)

        elif choice == "3":
            _browse_outputs(project)

        elif choice == "4" and has_manual:
            _optimise_project_context(project)

        elif choice == "0" or choice is None:
            return
        else:
            _err("Invalid choice.")


def _optimise_project_context(project):
    """Use the LLM to compress Manual Inputs into dense, token-efficient bullet points."""
    # Resolve manual input text and its source file
    obs = project.get("obsidian_project") or project
    manual_text = obs.get("manual_input", "")
    if not manual_text:
        _info("No Manual Inputs found for this project.")
        _pause()
        return

    obs_path = Path(obs.get("path", ""))
    manual_file = None
    for dir_name in ["Manual Inputs", "manual_inputs", "manual inputs"]:
        candidate = obs_path / dir_name
        if candidate.is_dir():
            files = sorted(candidate.glob("*.md"))
            if files:
                manual_file = files[0]
            break

    clr()
    print(f"\n{GOLD}{BOLD}  ✂️  OPTIMISE CONTEXT — {project['title'].upper()}{RESET}")
    _line()
    print(f"\n  {GREY}Current Manual Inputs ({len(manual_text)} chars):{RESET}")
    print(f"  {GREY}{manual_text[:300]}...{RESET}\n")
    print(f"  The LLM will rewrite this as concise bullet points,")
    print(f"  preserving every key fact but eliminating prose.")
    print(f"  Original file kept as .bak before overwriting.\n")

    confirm = _ask("Proceed? [y/N]")
    if confirm and confirm.lower() == "y":
        async def _compress():
            from advanced_reasoning import AdvancedReasoningSystem
            system = AdvancedReasoningSystem(reset_tree=False)
            print(f"\n  {GREY}Loading model…{RESET}")
            if not await system.initialize():
                _err("Could not load model.")
                return None
            prompt = (
                "<|im_start|>system\n"
                "You are a context compressor. Rewrite the input as dense, "
                "token-efficient bullet points. Preserve every fact, number, name "
                "and decision. Remove all prose, greetings, and repetition. "
                "Output plain text bullets only, no JSON, no markdown headers."
                "<|im_end|>\n"
                f"<|im_start|>user\n{manual_text}\n\n"
                "Compress this to the shortest form that retains all information. /no_think"
                "<|im_end|>\n"
                "<|im_start|>assistant\n"
            )
            raw = await system.llm_loader.generate(prompt, max_tokens=600)
            return raw.strip()

        compressed = asyncio.run(_compress())
        if compressed:
            clr()
            print(f"\n{GOLD}{BOLD}  ✅ COMPRESSED VERSION ({len(compressed)} chars vs {len(manual_text)} original){RESET}")
            _line()
            print(f"\n{compressed}\n")
            _line()
            save = _ask("Save this version? [y/N]")
            if save and save.lower() == "y" and manual_file:
                # Back up original
                bak = manual_file.with_suffix(".md.bak")
                bak.write_text(manual_file.read_text())
                manual_file.write_text(compressed)
                _ok(f"Saved → {manual_file.name}  (original → {bak.name})")
                # Invalidate project finder cache so next scan picks up new content
                import core.INTEGRATION.file_sync as _fs
                _fs._project_finder = None
            elif save and save.lower() == "y":
                _warn("Could not find source file to overwrite — copy the text above manually.")
        _pause()


def _browse_outputs(project):
    project_title = project.get("title", "")
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', project_title).strip('_') if project_title else ""

    # Always look in ROOT/outputs — that's where all MCTS results land.
    # Filter by project slug in filename (fast) or "project" field in JSON (fallback).
    outputs_dir = ROOT / "outputs"
    outputs = []
    if outputs_dir.exists():
        for f in sorted(outputs_dir.glob("mcts_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            if slug and slug.lower() in f.name.lower():
                outputs.append(f)
            elif not slug:
                outputs.append(f)

        # Fallback: check JSON content for untagged old files
        if not outputs and slug:
            for f in sorted(outputs_dir.glob("mcts_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
                try:
                    data = json.loads(f.read_text())
                    if data.get("project", "").lower() == project_title.lower():
                        outputs.append(f)
                except Exception:
                    pass

    if not outputs:
        _info("No saved outputs found for this project.")
        _pause()
        return

    clr()
    print(f"\n{GOLD}{BOLD}  📊 PAST OUTPUTS — {project['title']}{RESET}")
    _line()
    for i, f in enumerate(outputs[:10], 1):
        size = f.stat().st_size // 1024
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y %H:%M")
        print(f"  [{i}]  {CYAN}{f.name}{RESET}  {GREY}{size}KB · {mtime}{RESET}")

    print(f"  [0]  {GREY}↩ Back{RESET}")
    _line()

    choice = _ask("View file number")
    if not choice or choice == "0":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(outputs):
            data = json.loads(outputs[idx].read_text())
            clr()
            print(f"\n{GOLD}{BOLD}  📄 {outputs[idx].name}{RESET}")
            _line()

            if "meta_daemon" in data:
                meta = data["meta_daemon"]
                icon = {"GO": "✅", "NO_GO": "❌", "NEEDS_MORE_INFO": "⚠️"}.get(
                    meta.get("decision", ""), "❓"
                )
                print(f"\n  {icon} Decision:    {BOLD}{meta.get('decision')}{RESET}")
                print(f"  Confidence:  {meta.get('confidence', 0):.2f}")
                best = "  →  ".join(data.get("best_path", []))
                print(f"  Best path:   {best}")
                if meta.get("rationale"):
                    print(f"\n  Rationale:\n  {GREY}{str(meta['rationale'])[:300]}{RESET}")
                for step in meta.get("recommended_next_steps", [])[:4]:
                    print(f"  {GREEN}➜{RESET} {step}")
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])
    except Exception as e:
        _err(f"Could not read file: {e}")

    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  4 — BUSINESS VIABILITY                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_business_viability():
    clr()
    print(f"\n{GOLD}{BOLD}  🎯 BUSINESS VIABILITY ANALYSIS{RESET}")
    _line()
    print(f"  {GREY}Complete go/no-go analysis with:")
    print(f"  • MCTS tree (4 branches × 3 levels)")
    print(f"  • Will validates feasibility")
    print(f"  • Mrs. Coulter finds the risks you're missing")
    print(f"  • Iorek models financials (ROI + scenarios)")
    print(f"  • Meta-Daemon gives the final verdict{RESET}\n")

    idea   = _ask("Business idea (be detailed — more detail = better analysis)")
    if not idea:
        return

    btype  = _ask("Business type (e.g. SaaS / Marketplace / B2B / App)", "SaaS")
    budget = _ask("Available budget (e.g. €30k / $50k)", "$50,000")

    print(f"\n  {CYAN}Launching full viability analysis…{RESET}")
    _run_mcts(idea=idea, business_type=btype or "SaaS", budget=budget or "$50,000", reset=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  5 — VALIDATE AN IDEA                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_idea_validator():
    clr()
    print(f"\n{GOLD}{BOLD}  🧠 IDEA VALIDATOR — Quick Feasibility Check{RESET}")
    _line()
    print(f"  {GREY}Will + Mrs. Coulter give you a rapid first-pass assessment.")
    print(f"  No full MCTS tree — just the core signal in ~5-10 min.{RESET}\n")

    idea = _ask("Describe the idea")
    if not idea:
        return

    budget = _ask("Budget range (optional)", "Unknown")

    print(f"\n  {CYAN}Loading model…{RESET}")

    async def _validate():
        from core.llm.ram_manager import RAMManager
        from core.reasoning.reasoning_agent import Qwen3Loader, ReasoningAgent

        ram = RAMManager()
        loader = Qwen3Loader(ram)
        ok, msg = loader.check_ram_availability()
        print(f"  {msg}")
        if not ok:
            _err("Insufficient RAM.")
            return

        if not await loader.load():
            _err("Model failed to load.")
            return

        agent = ReasoningAgent(loader)

        print(f"\n  {CYAN}Will is checking feasibility…{RESET}")
        will_out = await agent.will_validate(idea, idea)

        print(f"  {CYAN}Mrs. Coulter is finding the risks…{RESET}")
        coulter_out = await agent.coulter_assess_risks(idea, will_out or {})

        clr()
        print(f"\n{GOLD}{BOLD}  🧠 QUICK VALIDATION RESULT{RESET}")
        _line()

        if will_out:
            verdict = will_out.get("verdict", "?")
            fscore  = will_out.get("feasibility_score", 0)
            icon    = "✅" if "FEASIBLE" in str(verdict) else "⚠️"
            print(f"\n  {icon}  Will says: {BOLD}{verdict}{RESET}  (score {fscore:.2f})")
            print(f"\n  {CYAN}Timeline:{RESET} {will_out.get('timeline_estimate', '?')}")
            blockers = will_out.get("blockers", [])
            if blockers:
                print(f"\n  {GOLD}Blockers:{RESET}")
                for b in blockers[:4]:
                    print(f"    • {b}")
            reqs = will_out.get("requirements", [])
            if reqs:
                print(f"\n  {GREEN}What you need:{RESET}")
                for r in reqs[:4]:
                    print(f"    • {r}")

        if coulter_out:
            rscore = coulter_out.get("risk_score", 0)
            print(f"\n  {RED}Mrs. Coulter says{RESET} (risk score {rscore:.2f} — higher is safer):")
            risks = coulter_out.get("risks", [])
            for r in risks[:3]:
                if isinstance(r, dict):
                    print(f"    ⚠️  {r.get('risk')}  {GREY}[{r.get('impact','?')} impact]{RESET}")
                    if r.get("mitigation"):
                        print(f"       {GREY}↳ {r['mitigation'][:80]}{RESET}")

            challenged = coulter_out.get("challenged_assumptions", [])
            if challenged:
                print(f"\n  {RED}Challenged assumptions:{RESET}")
                for c in challenged[:3]:
                    print(f"    • {c}")

        print(f"\n  {GREY}For a full analysis (financials + tree), use option [4].{RESET}")
        loader.unload()

    try:
        asyncio.run(_validate())
    except Exception as e:
        _err(f"Analysis failed: {e}")

    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  6 — CONTINUE ANALYSIS                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_continue_analysis():
    clr()
    print(f"\n{GOLD}{BOLD}  🌲 CONTINUE / RESUME ANALYSIS{RESET}")
    _line()

    tree_file = Path.home() / ".mcts_reasoning" / "tree_structure.json"

    if not tree_file.exists():
        _warn("No saved tree found.")
        _info("Start a new analysis with option [1] or [4].")
        _pause()
        return

    try:
        data = json.loads(tree_file.read_text())
        saved_at = data.get("saved_at", "unknown")
        node_count = len(data.get("nodes", []))
        root_id = data.get("root_id")
        root_desc = ""
        for n in data.get("nodes", []):
            if n["id"] == root_id:
                root_desc = n.get("description", "")[:80]
                break

        print(f"  {GREEN}Found a saved analysis:{RESET}")
        print(f"  {GREY}Saved at:  {saved_at}{RESET}")
        print(f"  {GREY}Nodes:     {node_count}{RESET}")
        print(f"  {GREY}Idea:      {root_desc}{RESET}\n")

        _opt("1", "▶️ ", "Resume this analysis",  "— continue expanding from where it stopped")
        _opt("2", "🗑 ", "Clear and start fresh",  "— delete the saved tree")
        _opt("0", "↩ ", "Back",                    "")
        _line()

        choice = _ask("Choose")

        if choice == "1":
            print(f"\n  {CYAN}Resuming analysis…{RESET}\n")
            _run_mcts(idea=root_desc, business_type="general", budget="Unknown", reset=False)
        elif choice == "2":
            tree_file.unlink()
            _ok("Saved tree deleted.")
            _pause()
    except Exception as e:
        _err(f"Could not read saved tree: {e}")
        _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MCTS RUNNER (shared by multiple menus)                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def _run_mcts(idea: str, business_type: str, budget: str, reset: bool, project: dict = None):
    async def _go():
        from advanced_reasoning import AdvancedReasoningSystem

        # Enrich idea with Manual Inputs (ground-truth context written by owner)
        project_title = project.get("title", "") if project else ""
        manual = ""
        if project:
            manual = (
                project.get("manual_input")
                or project.get("obsidian_project", {}).get("manual_input")
                or project.get("apps_project", {}).get("manual_input")
                or ""
            )
        if manual:
            full_idea = f"[Manual Context — written by owner]\n{manual}\n\n[Analysis topic]\n{idea}"
        else:
            full_idea = idea

        system = AdvancedReasoningSystem(reset_tree=reset)

        if not await system.initialize():
            import psutil as _ps
            free_gb = _ps.virtual_memory().available / (1024**3)
            print(f"\n  {RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            if system.init_error == "ram":
                print(f"  {RED}✗  Not enough RAM (need 3.5 GB free for Qwen3-4B, 5.5 GB for Qwen3-8B){RESET}")
                print(f"  {RED}   You have {free_gb:.1f} GB free right now.{RESET}")
                print(f"\n  {GOLD}To free RAM, close:{RESET}")
                print(f"  {GREY}  • Browser tabs (biggest consumer){RESET}")
                print(f"  {GREY}  • Slack / Discord / Teams{RESET}")
                print(f"  {GREY}  • VS Code / Cursor / other IDEs{RESET}")
                print(f"  {GREY}  • Spotify / streaming apps{RESET}")
                print(f"  {GREY}  • Any other open applications{RESET}")
                print(f"\n  {GOLD}Then come back and try again.{RESET}")
            else:
                print(f"  {RED}✗  Failed to load Qwen3-4B model.{RESET}")
                print(f"  {GREY}  Check the error above for details.{RESET}")
                print(f"  {GREY}  Common causes:{RESET}")
                print(f"  {GREY}  • First run: model not yet downloaded (~2.3 GB needed){RESET}")
                print(f"  {GREY}  • No internet connection for first-time download{RESET}")
                print(f"  {GREY}  • HuggingFace token required (run: huggingface-cli login){RESET}")
                print(f"  {GOLD}  Model ID: mlx-community/Qwen3-4B-4bit{RESET}")
            print(f"  {RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            return

        result = await system.run_analysis(
            business_idea=full_idea,
            business_type=business_type,
            budget=budget,
            reset=reset,
        )

        # Print a tight summary
        meta = result.get("meta_daemon", {})
        decision = meta.get("decision", "?")
        conf = meta.get("confidence", 0.0)
        icon = {"GO": "✅", "NO_GO": "❌", "NEEDS_MORE_INFO": "⚠️"}.get(decision, "❓")

        clr()
        print(f"\n{GOLD}{BOLD}  🔮 ANALYSIS COMPLETE — COUNCIL VERDICT{RESET}")
        _line()
        print(f"\n  {icon}  {BOLD}Decision: {decision}{RESET}   (confidence {conf:.2f} / 1.00)")
        best = "  →  ".join(result.get("best_path", []))
        print(f"\n  Best path:  {CYAN}{best}{RESET}")

        rationale = meta.get("rationale", "")
        if rationale:
            print(f"\n  Rationale:")
            print(f"  {GREY}{str(rationale)[:300]}{RESET}")

        factors = meta.get("key_success_factors", [])
        if factors:
            print(f"\n  {GREEN}Key success factors:{RESET}")
            for f in factors[:4]:
                print(f"    • {f}")

        steps = meta.get("recommended_next_steps", [])
        if steps:
            print(f"\n  {CYAN}Recommended next steps:{RESET}")
            for s in steps[:4]:
                print(f"    ➜ {s}")

        fin = result.get("financial_projection", {})
        if fin:
            rev = fin.get("revenue_projection", {})
            roi = fin.get("roi_estimate")
            cost = fin.get("dev_cost_estimate")
            if any([rev, roi, cost]):
                print(f"\n  {GOLD}Financial snapshot:{RESET}")
                if cost:      print(f"    Dev cost:   {cost}")
                if roi:       print(f"    ROI est.:   {roi:.1f}×")
                for yr, val in list(rev.items())[:3]:
                    print(f"    {yr}:  {val}")

        risks = result.get("key_risks", [])
        if risks:
            print(f"\n  {RED}Top risks:{RESET}")
            for r in risks[:2]:
                if isinstance(r, dict):
                    print(f"    ⚠️  {r.get('risk','?')}  {GREY}[{r.get('impact','?')}]{RESET}")
                else:
                    print(f"    ⚠️  {r}")

        # Tag result with project and save with project slug in filename
        if project_title:
            result["project"] = project_title
        slug = re.sub(r'[^a-zA-Z0-9]+', '_', project_title).strip('_') if project_title else ""
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = f"mcts_{slug}_{ts}.json" if slug else f"mcts_{ts}.json"
        out_path = ROOT / "outputs" / fname
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n  {GREY}Full JSON saved → {out_path.name}{RESET}")

        # Milestone check
        count = _get_analyses_count()
        _check_milestone(count)

        _agent("Lyra:", f"The tree has {len(result.get('full_tree', []))} nodes. Every branch taught us something.")
        _agent("Will:", "We did what needed to be done.")

    try:
        asyncio.run(_go())
    except KeyboardInterrupt:
        _warn("Analysis interrupted. Partial tree saved to ~/.mcts_reasoning/")
    except Exception as e:
        _err(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()

    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  7 — MEET THE TEAM                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

AGENT_INTROS = {
    "Lyra": {
        "icon": "🌟",
        "title": "Explorer & Analyst",
        "daemon": "Pantalaimon (shape-shifting marten — adapts to any situation)",
        "mission": "Generates bold ideas, finds patterns, seeks truth in data.",
        "quote": "The alethiometer doesn't lie. Neither does good analysis.",
        "mcts_role": "Generates the 4 initial reasoning branches.",
    },
    "Will": {
        "icon": "⚔️ ",
        "title": "Executor & Feasibility Check",
        "daemon": "None (the subtle knife cuts to the heart of the matter)",
        "mission": "Validates whether ideas can actually be built with real constraints.",
        "quote": "You do what needs to be done.",
        "mcts_role": "Assesses practical feasibility (score 0-1).",
    },
    "Marisa": {
        "icon": "👑",
        "title": "Developer & Executor",
        "daemon": "Golden Monkey (precise, commanding, relentless)",
        "mission": "Turns decisions into code and action plans.",
        "quote": "Ambition, properly channelled, is the most powerful force.",
        "mcts_role": "Supports Will with execution detail.",
    },
    "Iorek": {
        "icon": "🐻",
        "title": "Analyst & Financial Modeller",
        "daemon": "None (armored bears cannot be deceived)",
        "mission": "Numbers don't lie. Models ROI, costs, and scenarios with steel precision.",
        "quote": "A bear's strength is in his armour. Yours is in knowing the numbers.",
        "mcts_role": "Models financials: ROI, dev cost, 3-year revenue (score 0-1).",
    },
    "Serafina": {
        "icon": "🧙",
        "title": "Researcher & Strategist",
        "daemon": "Aerial perspective (witches see the whole board)",
        "mission": "Researches market context, best practices, and competitive landscape.",
        "quote": "See far. The horizon is always further than you think.",
        "mcts_role": "Provides market context and research support.",
    },
    "Mrs. Coulter": {
        "icon": "⚠️ ",
        "title": "Critic & Risk Analyst",
        "daemon": "Golden Monkey (finds what's hidden beneath the surface)",
        "mission": "Devil's advocate. Finds every risk, challenge, and hidden assumption.",
        "quote": "The greatest danger is the risk you haven't named yet.",
        "mcts_role": "Adversarial risk assessment (risk_score 0-1, higher = safer).",
    },
    "Lee": {
        "icon": "✍️ ",
        "title": "Writer & Communicator",
        "daemon": "Hester (hare — fast, aware, communicative)",
        "mission": "Turns insights into clear, actionable documents and stories.",
        "quote": "Every great journey starts with one honest step.",
        "mcts_role": "Documents final recommendations and reports.",
    },
    "Coram": {
        "icon": "🔍",
        "title": "Validator & Quality Check",
        "daemon": "Sophonax (careful, experienced, thorough)",
        "mission": "Validates reasoning, checks for logical errors, risk-tests conclusions.",
        "quote": "Experience is what remains after everything else has faded.",
        "mcts_role": "Validates the final tree output for consistency.",
    },
    "Mary": {
        "icon": "🔬",
        "title": "Tools Manager & Context Keeper",
        "daemon": "Dust (interconnected knowledge)",
        "mission": "Manages project context, injects temporal + technical knowledge.",
        "quote": "Pay attention to the data. The pattern will emerge.",
        "mcts_role": "Context injection — ensures the team has current information.",
    },
}


def run_meet_the_team():
    clr()
    print(f"\n{GOLD}{BOLD}  👥 MEET THE TEAM — His Dark Materials Wisdom Council{RESET}")
    _line()
    print(f"  {GREY}8 agents, each a character from Philip Pullman's world.")
    print(f"  Each has a unique daemon, a role, and a purpose: your success.{RESET}\n")

    # Try to get real learning scores
    try:
        from core.agents import list_agents
        agents_data = {a.name: a for a in list_agents()}
    except Exception:
        agents_data = {}

    names = list(AGENT_INTROS.keys())
    for i, name in enumerate(names, 1):
        info = AGENT_INTROS[name]
        score = 0.0
        if name in agents_data:
            score = agents_data[name].learning_score
        bar_filled = int(score * 10)
        bar = f"{GREEN}{'█' * bar_filled}{GREY}{'░' * (10 - bar_filled)}{RESET}"

        print(f"  [{i}] {info['icon']}  {CYAN}{BOLD}{name}{RESET}  —  {GOLD}{info['title']}{RESET}")
        print(f"       {GREY}Daemon:{RESET} {info['daemon']}")
        print(f"       {GREY}Mission:{RESET} {info['mission']}")
        print(f"       {GREY}MCTS role:{RESET} {info['mcts_role']}")
        print(f"       {GREY}Learning:{RESET} {bar} {score:.2f}")
        print(f"       {GREY}❝ {info['quote']} ❞{RESET}")
        print()

    print(f"  {GOLD}Together:{RESET} {GREY}8 specialists, 1 mission — to make you financially free.{RESET}")
    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  8 — MEMORY & PATTERNS                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_memory_menu():
    while True:
        clr()
        print(f"\n{GOLD}{BOLD}  📊 MEMORY & PATTERNS — Collective Intelligence{RESET}")
        _line()

        # MCTS memory stats
        from core.reasoning.reasoning_memory import ReasoningMemory
        mem = ReasoningMemory()
        stats = mem.get_stats()

        print(f"\n  {GREEN}MCTS Reasoning Memory{RESET}")
        print(f"  Total analyses stored: {CYAN}{stats['total_analyses']}{RESET}")
        if stats["decisions"]:
            for d, c in stats["decisions"].items():
                icon = {"GO": "✅", "NO_GO": "❌", "NEEDS_MORE_INFO": "⚠️"}.get(d, "❓")
                print(f"  {icon}  {d}: {c}")
        print(f"  Storage: {GREY}{stats['storage_path']}{RESET}")

        # Hybrid memory stats
        try:
            from core.memory.hybrid_memory import create_hybrid_memory
            hm = create_hybrid_memory()
            hm_stats = hm.get_learning_summary()
            print(f"\n  {GREEN}Hybrid Memory (RAG + Graph){RESET}")
            print(f"  Analyses: {CYAN}{hm_stats['total_analyses']}{RESET}")
            print(f"  Known project types: {CYAN}{', '.join(hm_stats['known_project_types'][:6]) or 'none yet'}{RESET}")
            print(f"  Graph nodes: {CYAN}{hm_stats['graph_nodes']}{RESET}")
        except Exception:
            pass

        print()
        _opt("1", "🔍", "Search past analyses",    "")
        _opt("2", "📈", "Agent learning progress", "")
        _opt("3", "🎓", "Discovered patterns",     "")
        _opt("4", "🗑 ", "Clear MCTS tree cache",  "— frees ~/.mcts_reasoning/tree_structure.json")
        _opt("0", "↩ ", "Back", "")
        _line()

        choice = _ask("Choose")

        if choice == "1":
            _search_analyses()
        elif choice == "2":
            _show_agent_learning()
        elif choice == "3":
            _show_patterns()
        elif choice == "4":
            _clear_tree_cache()
        elif choice == "0" or choice is None:
            return


def _search_analyses():
    clr()
    print(f"\n{GOLD}{BOLD}  🔍 SEARCH PAST ANALYSES{RESET}")
    _line()

    query = _ask("Search for (keyword or topic)")
    if not query:
        return

    from core.reasoning.reasoning_memory import ReasoningMemory
    mem = ReasoningMemory()
    results = mem.retrieve_similar(query, min_confidence=0.0, limit=10)

    if not results:
        _info("No matching analyses found.")
        _pause()
        return

    print(f"\n  {GREEN}Found {len(results)} result(s):{RESET}\n")
    for i, r in enumerate(results, 1):
        decision = r.get("final_decision", "?")
        icon = {"GO": "✅", "NO_GO": "❌", "NEEDS_MORE_INFO": "⚠️"}.get(decision, "❓")
        conf = r.get("confidence", 0)
        ts = r.get("timestamp", r.get("stored_at", "?"))[:16]
        idea = r.get("input_description", "")[:65]
        print(f"  [{i}] {icon} {CYAN}{r.get('business_type','?')}{RESET}  conf={conf:.2f}  {GREY}{ts}{RESET}")
        print(f"       {GREY}{idea}{RESET}")

    _pause()


def _show_agent_learning():
    clr()
    print(f"\n{GOLD}{BOLD}  📈 AGENT LEARNING PROGRESS{RESET}")
    _line()

    try:
        from core.agents import list_agents
        from core.memory.rag_memory import create_rag_memory

        agents = list_agents()
        rag = create_rag_memory()

        print()
        for a in agents:
            score = a.learning_score
            tasks = a.completed_tasks
            bar_filled = int(score * 20)
            bar = f"{GREEN}{'█' * bar_filled}{GREY}{'░' * (20 - bar_filled)}{RESET}"

            try:
                insights = rag.get_agent_insights(a.name)
                trajectory = insights.get("learning_trajectory", "Growing")
            except Exception:
                trajectory = "Growing"

            print(f"  {CYAN}{a.name:14s}{RESET} {bar} {score:.3f}  tasks={tasks}  {GREY}{trajectory}{RESET}")

    except Exception as e:
        _err(f"Could not load agent data: {e}")

    _pause()


def _show_patterns():
    clr()
    print(f"\n{GOLD}{BOLD}  🎓 DISCOVERED PATTERNS{RESET}")
    _line()

    try:
        from core.memory.hybrid_memory import create_hybrid_memory
        hm = create_hybrid_memory()

        if not hm.patterns:
            _info("No patterns discovered yet. Run more analyses to build the pattern library.")
            _pause()
            return

        for ptype, data in hm.patterns.items():
            count = data.get("count", 0)
            print(f"\n  {CYAN}{ptype.upper()}{RESET}  ({count} analyses)")
            risks = data.get("common_risks", [])[:3]
            if risks:
                print(f"  {RED}Common risks:{RESET}")
                for r in risks:
                    print(f"    • {r}")
            patterns = data.get("decision_patterns", [])[:2]
            if patterns:
                print(f"  {GREEN}Common recommendations:{RESET}")
                for p in patterns:
                    print(f"    ➜ {str(p)[:70]}")
    except Exception as e:
        _err(f"Could not load patterns: {e}")

    _pause()


def _clear_tree_cache():
    tree_file = Path.home() / ".mcts_reasoning" / "tree_structure.json"
    if tree_file.exists():
        tree_file.unlink()
        _ok("Tree cache cleared. Next analysis will start fresh.")
    else:
        _info("No tree cache found.")
    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  9 — SEARCH ANALYSES                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_search():
    _search_analyses()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  S — SYSTEM STATUS                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_system_status():
    clr()
    print(f"\n{GOLD}{BOLD}  💻 SYSTEM STATUS{RESET}")
    _line()

    # RAM
    try:
        import psutil
        mem = psutil.virtual_memory()
        total = mem.total / (1024 ** 3)
        avail = mem.available / (1024 ** 3)
        used  = mem.used / (1024 ** 3)
        pct   = mem.percent

        print(f"\n  {GREEN}Memory{RESET}")
        print(f"  Total:     {total:.1f} GB")
        print(f"  Available: {avail:.1f} GB  ({100 - pct:.0f}% free)")
        print(f"  Used:      {used:.1f} GB  ({pct:.0f}% used)")

        qwen4b_ok = avail >= 3.5
        qwen8b_ok = avail >= 5.5
        if qwen8b_ok:
            status  = "✅ Qwen3-8B-4bit  (best quality)"
            quality = "🏆 Excellent"
        elif qwen4b_ok:
            status  = "✅ Qwen3-4B-4bit  (fallback)"
            quality = "✅ Good"
        else:
            status  = "❌ Need 3.5 GB+ free"
            quality = "⚠️ Low"
        print(f"\n  Model readiness: {quality}  —  {status}")
    except Exception:
        _warn("Could not read memory info.")

    # Model info
    print(f"\n  {GREEN}Model Configuration{RESET}")
    print(f"  Primary:  Qwen3-8B-4bit  (~4.5 GB RAM)  — if ≥ 5.5 GB free")
    print(f"  Fallback: Qwen3-4B-4bit  (~2.3 GB RAM)  — always fits")
    print(f"  Framework: MLX (Apple Silicon optimised)")

    cache = Path.home() / ".cache" / "huggingface" / "hub"
    if cache.exists():
        q8b_cached = any("Qwen3-8B" in str(p) for p in cache.iterdir() if p.is_dir())
        q4b_cached = any("Qwen3-4B" in str(p) for p in cache.iterdir() if p.is_dir())
        print(f"\n  Qwen3-8B-4bit cached:  {'✅ Yes' if q8b_cached else '⬇️  Will download on first use (~4.5 GB)'}")
        print(f"  Qwen3-4B-4bit cached:  {'✅ Yes' if q4b_cached else '⬇️  Will download on first use (~2.3 GB)'}")

    # MCTS state
    print(f"\n  {GREEN}MCTS State{RESET}")
    tree_file = Path.home() / ".mcts_reasoning" / "tree_structure.json"
    paths_file = Path.home() / ".mcts_reasoning" / "explored_paths.jsonl"

    if tree_file.exists():
        data = json.loads(tree_file.read_text())
        print(f"  Active tree:  {len(data.get('nodes', []))} nodes  (saved {data.get('saved_at','?')[:16]})")
    else:
        print(f"  Active tree:  none")

    if paths_file.exists():
        count = sum(1 for _ in open(paths_file))
        size  = paths_file.stat().st_size // 1024
        print(f"  Memory log:  {count} entries  ({size} KB)")
    else:
        print(f"  Memory log:  empty")

    # Python + mlx-lm
    print(f"\n  {GREEN}Environment{RESET}")
    print(f"  Python: {sys.version.split()[0]}")
    try:
        import mlx_lm
        print(f"  mlx-lm: ✅ installed")
    except ImportError:
        print(f"  mlx-lm: ❌ NOT installed  →  pip install mlx-lm")
    try:
        import psutil as _p
        print(f"  psutil: ✅ installed")
    except ImportError:
        print(f"  psutil: ❌ NOT installed  →  pip install psutil")

    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  H — HELP                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def run_help():
    clr()
    print(f"\n{GOLD}{BOLD}  📖 HOW TO USE THE WISDOM COUNCIL{RESET}")
    _line()

    sections = [
        ("GETTING STARTED",
         "1. Double-click launch.command to open in Terminal\n"
         "   2. First run: model downloads automatically (2.3–4.5 GB)\n"
         "   3. Choose an option from the main menu"),

        ("QUICK ANALYSIS [1]",
         "Type any business idea. The council runs a full MCTS tree:\n"
         "   • Lyra generates 4 approaches\n"
         "   • Will checks feasibility (0-1 score)\n"
         "   • Mrs. Coulter finds hidden risks (0-1 score)\n"
         "   • Iorek models ROI + costs (0-1 score)\n"
         "   • Top-2 branches expanded 2 more levels\n"
         "   • Meta-Daemon gives GO/NO-GO + next steps\n"
         "   Duration: 20-60 min depending on complexity"),

        ("WAR ROOM [2]",
         "Select an existing project from ~/Obsidian-Vault/ or ~/Desktop/apps/\n"
         "   All 8 agents discuss it in depth using LLM reasoning.\n"
         "   Uses Qwen3-8B-4bit (5.5 GB+ free) or Qwen3-4B-4bit (3.5 GB+ free)."),

        ("VALIDATE AN IDEA [5]",
         "Quick check in 5-10 min.\n"
         "   Will + Mrs. Coulter give you the core feasibility signal.\n"
         "   No full tree — just enough to decide if it's worth a full run."),

        ("MEMORY & PATTERNS [8]",
         "The team learns with every analysis.\n"
         "   Past reasoning paths are stored in ~/.mcts_reasoning/\n"
         "   Lyra uses them to generate better branches next time."),

        ("RAM TIPS",
         "Qwen3-8B-4bit: needs 5.5 GB free RAM — auto-selected if available\n"
         "   Qwen3-4B-4bit: needs 3.5 GB free RAM — fallback, always fits\n"
         "   Close browser tabs and other apps before a long analysis.\n"
         "   System checks RAM on startup and selects the best model automatically."),

        ("RESULTS",
         "JSON results saved automatically in outputs/ folder.\n"
         "   View them with option [3] → My Projects → View Past Outputs."),
    ]

    for title, body in sections:
        print(f"\n  {GOLD}{BOLD}{title}{RESET}")
        for line_text in body.split("\n"):
            stripped = line_text.strip()
            if stripped.startswith(("•", "→", "➜", "*", "-")):
                print(f"  {GREY}  {stripped}{RESET}")
            elif stripped:
                print(f"  {stripped}")

    print(f"\n  {GOLD}Mission:{RESET} {GREY}You + the council, building financial freedom together.{RESET}")
    print(f"  {GOLD}Contact:{RESET} {GREY}github.com/anthropics/claude-code/issues{RESET}")
    _pause()


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  MAIN LOOP                                                               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

MENU_MAP = {
    "1": run_quick_analysis,
    "2": run_war_room_menu,
    "3": run_projects_menu,
    "4": run_business_viability,
    "5": run_idea_validator,
    "6": run_continue_analysis,
    "7": run_meet_the_team,
    "8": run_memory_menu,
    "9": run_search,
    "s": run_system_status,
    "h": run_help,
}


def main():
    while True:
        choice = show_main_menu()

        if choice is None or choice.lower() in ("q", "exit", "quit", "bye"):
            clr()
            q_agent, q_text = random.choice(QUOTES)
            print(f"\n  {GOLD}Until next time.{RESET}")
            print(f"\n  {GREY}❝ {q_text} ❞{RESET}")
            print(f"  {GREY}      — {q_agent}{RESET}\n")
            sys.exit(0)

        handler = MENU_MAP.get(choice.lower())
        if handler:
            handler()
        else:
            _err(f"Unknown option: '{choice}'")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
