- council of wisdom
  - ler sempre o agents.md que esta no obsidian
  - todos os githubs devem ter um branch de dev. Ele deverá ser updated sempre que o projecto estiver funcional. Apenas se faz merge para o branch principal quando eu aprovar. Novas funcionalidades deverao ser separadas. Isto é gerido por um agente de devops, um dos nossos personagens será esse devops!
  - precisamos de um agente orquestrador
  - antes de tudo, precisamos de entender o contexto dos projectos, obter os seus objectivos e estrutura.
    - Se o projecto for um negócio, é IMPERATIVO fazer análise PROFUNDA de plano de negócio:
      * ESTUDO DE MERCADO: Tamanho, trends, crescimento, segmentos, geografias
      * ANÁLISE COMPETITIVA: Competidores diretos/indiretos, market share, posicionamento deles
      * VANTAGENS COMPETITIVAS: O que nos diferencia? Por que ganhar?
      * AMEAÇAS: Barreiras à entrada, disrupção, mercado saturado?
      * VIABILIDADE FINANCEIRA: Modelo de receita, unit economics, tempo para break-even?
      * RECOMENDAÇÃO: Prosseguir ou descartar? (com razões claras)
    - O plano deve ser discutido entre agentes como CONSULTORES!
      * Lyra (Analyst) = Métricas de mercado, trends, dados
      * Iorek (Architect) = Estrutura do negócio, escalabilidade
      * Marisa (Developer) = Viabilidade técnica, execução
      * Serafina (Researcher) = Competitive intelligence, market deep-dive
      * Lee (Writer) = Positioning, estratégia de go-to-market
      * Pantalaimon (Tester) = Risk assessment, validação de suposições
      * Philip (Coordinator) = Viabilidade geral, consenso final
    - OUTPUT FINAL: Relatório executivo com recomendação (GO/NO-GO) 
  - precisamos de pesquisar na internet, preferencialmente no github e em reddits relevantes (pode ser feito atraves do mcp do reddit e/ou do mcp do duckduckgo que estao no mcp toolkit do reddit ou atraves do perplexity) por projectos semelhantes, para entendermos estruturas comprovadas que funcionam e/ou ferramentas uteis para o projecto. O inicio é aqui!  Essa informaçao deve ser guardada num ficheiro, cada projecto tem o seu ficheiro .md
  - nao quero que os agentes analisem somente o codigo. Quero que analisem a estrutura. Quero que analisem a estrutura e a comparem com benchmark projects que encontrem na internet, para isso precisam de procurar projectos com estruturas semelhantes ou criados para o mesmo objectivo. Quero que procurem ferramentas que aumentem eficiencia e qualidade do projecto. Precisam de propor actionable insights e melhorias! 
  - a analise precisa de demorar mais tempo, o llm local nem sequer esta a ser chamado. 
  - o llm local é um 14b ou um 8b. Para correr o 14b precisamos de confirmar que existe ram livre suficiente para o correr. Caso nao exista, precisamos de emitir um aviso para fechar programas. 
  - cada agente aborda o problema de acordo com a sua personalidade! 
  - precisa ser acessivel um pequeno resumo do conhecimento de cada agente
  - cada agente trabalha com o seu daemon para gerar a resposta. A resposta nao pode ser instantanea!
  - quando o qwen 3 code for chamado, o 14b e o 8b deverao ter sido encerrados previamente!
  - precisamos ter no terminal (cli) menus para aceder a war room e para mandar os agentes colaborarem entre si.
  - a memoria deverá evoluir, devera aprender. Poderemos usar sistema rag