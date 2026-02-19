# 🧙‍♂️ The Wisdom Council v2.1

**Sistema multi-agente que analisa projetos reais com especialistas de IA**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](#status)
[![Daemon Debate](https://img.shields.io/badge/Daemon_Debate-Active-gold)](#-daemon-debate-system)
[![Interactive Research](https://img.shields.io/badge/Interactive_Research-Active-blue)](#-interactive-collaborative-research-new)

**Versão**: 2.1 — Fevereiro 2026
**Status**: ✅ Operacional (Production Ready)

---

## 📖 O que é?

Wisdom Council é um **sistema inteligente de análise** que:

1. **Descobre automaticamente** projetos reais (código + documentação)
2. **Enriquecimento Estratégico (Perplexity)**: Pesquisa profunda de Mercado, Tech e Objetivos antes da análise ⭐ NEW
3. **8 Agentes Especializados** com papéis estratégicos em pipeline
4. **Daemon Debate System**: Cada agente debate com o seu daemon para auto-correção
5. **Interactive Collaborative Research**: Os agentes pedem ajuda ao humano para pesquisas em tempo real ⭐ NEW
6. **Real Analysis**: Identifica problemas específicos com line numbers
7. **Multi-Layered Learning**: Aprende através de learning scores, RAG e MCTS
8. **Auto-Documentação**: Guarda tudo no Obsidian mindpalace

---

## 🐾 Daemon Debate System

Inspirado nos livros de Philip Pullman, cada agente tem um **daemon** — a manifestação externa da sua alma — com personalidade complementar. O daemon **desafia** e **refina** o raciocínio do agente antes que este apresente ao conselho.

### Como Funciona

```
1. Agente produz análise inicial
         ↓
2. Daemon critica e desafia (perspectiva complementar)
         ↓
3. Agente consolida opinião final (incorporando feedback do daemon)
         ↓
4. Opinião consolidada vai para o conselho
```

### Porquê?

- **Self-Correction**: O daemon funciona como uma etapa de auto-correção
- **Multi-Perspective Prompting**: Força o modelo a considerar contra-argumentos
- **Redução de alucinações**: A voz complementar identifica pontos cegos
- **Fidelidade temática**: Fiel ao universo de "His Dark Materials"

---

## 👥 Os 8 Agentes + Daemons

Cada agente tem um papel específico e um daemon com personalidade **complementar**:

### Análise & Design
| Agente | Daemon | Dinâmica |
|--------|--------|----------|
| **Lyra** 📊 Analista | **Pantalaimon** (marta) | Lyra é impulsiva → Pan é cauteloso, pede dados concretos |
| **Iorek** 🏗️ Arquiteto | **Sky-Iron Intuition** (armadura) | Iorek projecta força → A armadura exige integridade real |

### Desenvolvimento & Optimização
| Agente | Daemon | Dinâmica |
|--------|--------|----------|
| **Marisa** 💻 Developer | **Golden Monkey** (macaco dourado) | Marisa é ambiciosa → O macaco revela custos ocultos |
| **Serafina** 🔬 Researcher | **Kaisa** (ganso-das-neves) | Serafina vê o presente → Kaisa traz precedentes históricos |

### Comunicação & Qualidade
| Agente | Daemon | Dinâmica |
|--------|--------|----------|
| **Lee** 📝 Writer | **Hester** (lebre) | Lee romantiza → Hester corta a gordura, exige clareza |
| **Coram** ✅ Validator | **Sophonax** (gato) | Coram confia na experiência → Sophonax lembra que cada caso é único |

### Execução & Ferramentas
| Agente | Daemon | Dinâmica |
|--------|--------|----------|
| **Asriel** 🎯 Coordinator | **Stelmaria** (leopardo-das-neves) | Asriel é grandioso → Stelmaria questiona o custo humano |
| **Mary** 🔧 Tools Manager | **Alpine Chough** (gralha) | Mary é cerebral → O daemon traz sensibilidade holística |

---

## 🚀 Quick Start

### Interactive Menu
```bash
cd ~/Desktop/Apps/His\ Dark\ Materials
python3 run.py
```

### macOS Launcher
```
Finder → Desktop → Apps → His Dark Materials → launch.command
```

---

## 🏗️ Como Funciona

### Step 1: Descoberta de Projetos
```
His Dark Materials encontra:
├── 4 apps executáveis (~/Desktop/Apps/)
│   ├── MundoBarbaroResearch (Python)
│   ├── WisdomOfReddit (Analysis)
│   └── CrystalBall (Predictions)
│
└── 5 projetos documentação (Obsidian)
    ├── Chemetil (Business)
    ├── RedditScrapper (Collection)
    └── AgentsAI (Learning)
```

### Step 2: Análise com Daemon Debate
```
Seleciona um projeto
    ↓
Agentes analisam individualmente
    ↓
Cada daemon desafia o seu agente  ⭐ NEW
    ↓
Agente consolida opinião final
    ↓
Debate colectivo no War Room
    ↓
Consenso e recomendação final
```

### Step 3: Learning
```
Experiência armazenada → Próxima análise é melhor!
```

---

## 🔧 Key Features

### 1. Real Code Analysis
- Lê código Python, JavaScript, e texto
- Identifica problemas específicos com line numbers
- Não é conselho genérico — issues reais no código

### 2. MCP Integration
```
MLX (Qwen3)      → Análise local de código (sem custos API)
Perplexity MCP   → Pesquisa web & contexto
Obsidian MCP     → Auto-save de findings
Paper Search     → Pesquisa académica
```

### 3. Multi-Layered Learning
```
O Conselho evolui em 3 níveis:
1. Seniority (Learning Score) -> Cada tarefa concluída aumenta o score (0-1)
2. Collaborative RAG Memory -> Base de dados de experiências passadas (JSONL)
3. MCTS Path Retention -> Memorização de caminhos de raciocínio bem sucedidos

Data stored in: core/memory/data/
```

### 4. Obsidian Integration
```
Resultados salvos em:
└── source mindpalace/1 - Projetos/
    ├── Chemetil/
    ├── WisdomOfReddit/
    ├── MundoBarbaroResearch/
    └── ...
```

---

## 📁 Arquitectura

```
His Dark Materials/
├── core/
│   ├── agents/                # 8 agentes + daemons
│   │   └── __init__.py        # Definições com daemon_personality
│   ├── orchestration/
│   │   ├── war_room.py        # Debate com Daemon Debate integrado
│   │   ├── orchestrator.py    # Orquestração geral
│   │   └── task_manager.py    # Gestão de tarefas
│   ├── llm/                   # MLX + RAM management
│   ├── memory/                # Learning & experiências
│   ├── research/              # Perplexity + context enrichment
│   └── INTEGRATION/           # Descoberta de projetos
│
├── council.py                 # CLI interactiva completa
├── run.py                     # Menu interactivo (legacy)
├── launch.command             # macOS launcher
└── README.md                  # Este ficheiro
```

---

## 📊 Status

### Current State
✅ 8 agentes operacionais com daemons
✅ Daemon Debate System ativo
✅ Strategic Perplexity Research integrada
✅ Interactive User Research loop funcional
✅ Multi-layered Learning system (RAG + Scores)
✅ Obsidian integration pronta

---

## 🔐 Segurança & Privacidade

- Sem uploads externos
- MLX corre localmente
- Obsidian fica no device
- API keys em .env (git-ignored)

---

## 💡 Filosofia

Wisdom Council baseia-se na ideia de que:

1. **Múltiplas perspectivas > análise singular** — 8 agentes vêem ângulos diferentes
2. **O daemon é a consciência** — Desafia antes de agir
3. **Análise real > conselho genérico** — Problemas específicos com line numbers
4. **Contexto é tudo** — Pesquisa web + análise de código + memória

---

*Wisdom Council: Real analysis for real projects.*
*8 agents. 8 daemons. 9 projects. Infinite possibilities.* 🧙‍♂️✨

*Última actualização: 19 de Fevereiro de 2026*
