# Vasco Defensive Analysis 2026

Análise da evolução defensiva do Vasco da Gama em 2026, comparando Fernando Diniz, Renato Gaúcho e Pedro Emanuel, com foco no Campeonato Brasileiro e dados do FBref.

## Pergunta

**O sistema defensivo do Vasco melhorou sob o comando de Pedro Emanuel?**

A ideia nasceu de uma percepção de quem acompanha futebol: em vez de aceitar a impressão visual, transformar a pergunta em dados. O projeto compara períodos com tamanhos diferentes de amostra usando principalmente métricas por partida e percentuais.

## Recorte metodológico

A análise principal usa apenas a Série A de 2026. Jogos de interinos ficam fora da comparação entre os três treinadores.

| Treinador | Recorte usado |
|---|---|
| Fernando Diniz | jogos até 22/02/2026 |
| Renato Gaúcho | da estreia em 12/03/2026 até 18/06/2026 |
| Pedro Emanuel | desde a estreia em 16/07/2026 |

A escolha considera quem efetivamente comandou a equipe na partida, e não apenas a data de anúncio/contratação.

## Métricas

- gols sofridos por jogo;
- clean sheets;
- taxa de clean sheets;
- chutes no alvo sofridos por jogo, quando disponíveis;
- percentual de defesas, quando disponível;
- evolução jogo a jogo.

## Pipeline

```text
FBref
  ↓
coleta das partidas + goalkeeping
  ↓
limpeza e padronização
  ↓
filtro Série A
  ↓
classificação por treinador
  ↓
métricas normalizadas
  ↓
gráficos
```

Para reproduzir:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

O `run_pipeline.py` busca os dados no FBref, processa a base, calcula os indicadores e recria as visualizações. Também existe um workflow manual em GitHub Actions (`Update defensive analysis`) para atualizar o projeto sem executar o código localmente.

## Estrutura

```text
.
├── .github/workflows/
├── data/
│   ├── raw/
│   └── processed/
├── images/
├── src/
│   ├── collect_fbref.py
│   ├── collect_goalkeeping.py
│   ├── analyze.py
│   └── visualize.py
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## Validação externa

Os resultados produzidos pelo pipeline serão confrontados com referências jornalísticas para detectar possíveis erros de coleta ou recorte. Essa validação não substitui os cálculos do projeto.

Referências de contexto:

- FBref — Vasco da Gama 2026 match logs;
- ge — Fernando Diniz deixou o Vasco em 22/02/2026;
- ge — Renato Gaúcho estreou contra o Palmeiras em 12/03/2026;
- ge — Renato deixou o clube em 18/06/2026;
- ge — Pedro Emanuel estreou contra o Vitória em 16/07/2026.

## Limitações

A análise mede desempenho observado, não causalidade. Mudanças de adversário, mando, escalação, lesões, reforços, calendário e tamanho da amostra podem afetar os números. Por isso, a conclusão deve ser lida como comparação de desempenho entre períodos, e não como prova isolada de efeito do treinador.

## Fonte de dados

FBref / Sports Reference. O HTML bruto não é versionado; o projeto prioriza código reproduzível e arquivos derivados necessários à análise.

## Autor

Diego Neves
