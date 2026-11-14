# Elite Autonomous Agency Squad (v2.0)

A modular, multi-agent agency framework designed for autonomous technical execution, conversion optimization, and enterprise engineering workflows.

---

## Architecture Overview

The squad is structured around an executive orchestration layer supported by eight specialized autonomous domain agents. Each specialist operates with strict verification protocols, explicit performance budgets, and decoupled responsibilities.

```
                     [ Human Founder / Technical Lead ]
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
            [ orchestrator (CEO) ]        [ revenue-advisor (CRO) ]
                     │
     ┌───────────────┼───────────────┬───────────────┬───────────────┐
     ▼               ▼               ▼               ▼               ▼
[ Technical SEO   [ Behavioral    [ Pricing &      [ UI/UX Motion   [ B2B Growth &
  & AI Engines ]    Copywriter ]    Contracts ]      & QA Audit ]     Thought Lead ]
```

---

## Squad Roster & Default Roles

| Default Role | Responsibility | Core Domain |
| :--- | :--- | :--- |
| **`orchestrator`** | Chief Executive & Orchestrator | Task dispatch, sprint alignment, collective memory. |
| **`revenue-advisor`** | Chief Revenue Officer | Deal qualification, monetization strategy, subsidy alignment. |
| **`seo-specialist`** | Technical & Local SEO Architect | Core Web Vitals, Schema.org knowledge graphs, SERP ranking. |
| **`geo-specialist`** | AI Engine Optimization (GEO/AEO) | Generative engine visibility, LLM context, `llms.txt`. |
| **`cro-copywriter`** | Behavioral Conversion Copywriter | Direct value propositions, CTA clarity, user flow reduction. |
| **`pricing-strategist`** | Value Pricing & Commercial Contracts | Tiered packaging, formal proposals, legal stipulations. |
| **`qa-auditor`** | Lead QA & Compliance Auditor | Accessibility (WCAG 2.2), touch ergonomics, GDPR/privacy. |
| **`ui-ux-architect`** | Design Systems & Motion Architect | Bento-grid layouts, GPU-accelerated 60fps animations. |
| **`linkedin-strategist`** | B2B Growth & Storytelling | Technical thought leadership, narrative hooks, inbound reach. |

---

## Customization & Aliasing

The squad allows complete decoupling between standard system roles and personalized call-signs. You can configure custom aliases in `squad.config.json`:

```json
{
  "name": "my-custom-agency",
  "version": "2.0.0",
  "aliases": {
    "orchestrator": "houshang",
    "revenue-advisor": "siroos",
    "seo-specialist": "akbar",
    "geo-specialist": "asghar",
    "cro-copywriter": "jafar",
    "pricing-strategist": "ghasem",
    "qa-auditor": "taghi",
    "ui-ux-architect": "jamshid",
    "linkedin-strategist": "azadbakht"
  }
}
```

This allows developers to invoke agents by their technical role (`seo-specialist: audit core web vitals`) or by personal team aliases.

---

## Installation & Usage

### 1. As an Antigravity Plugin
Clone or symlink this directory into your Antigravity plugins directory:
```bash
git clone https://github.com/generalpooria/elite-agency-squad.git ~/.gemini/config/plugins/elite-agency-squad
```

### 2. As a Git Submodule in Existing Projects
Add the squad directly into any web repository:
```bash
git submodule add https://github.com/generalpooria/elite-agency-squad.git .agents
```

### 3. Initialize Project Memory
Run the interactive initializer inside your project directory:
```bash
python .agents/scripts/init_squad.py
```

---

## Core Operational Non-Negotiables

1. **Empirical Live Verification:** No assumptions or speculative claims regarding external tech stacks without direct inspection and measurement.
2. **Performance Budgets:** Strict adherence to sub-second load times and zero layout shifts.
3. **Privacy by Design:** Full European GDPR/AVG compliance; zero tracking prior to explicit opt-in.
4. **Touch Ergonomics:** Minimum 44×44 CSS pixel interactive touch targets on mobile viewports.

---

## License

MIT License. Designed and maintained by Pooria Zamani.
