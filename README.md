# Vasco Defensive Analysis 2026

Análise de dados sobre a evolução defensiva do Vasco da Gama no Campeonato Brasileiro de 2026, comparando os períodos de Fernando Diniz, Renato Gaúcho e Pedro Emanuel com dados do FBref.

## A pergunta

**O sistema defensivo do Vasco melhorou sob o comando de Pedro Emanuel?**

O projeto nasceu de uma percepção assistindo aos jogos. Em vez de partir da conclusão, a proposta foi transformar essa impressão em uma pergunta mensurável e deixar os dados responderem.

## Primeiros achados

No recorte validado do Brasileirão, a comparação de gols sofridos e clean sheets mostra uma mudança relevante de perfil defensivo:

| Treinador | Jogos | Gols sofridos | GA/jogo | Clean sheets | CS% |
|---|---:|---:|---:|---:|---:|
| Fernando Diniz | 3 | 4 | 1,33 | 0 | 0,0% |
| Renato Gaúcho | 14 | 22 | 1,57 | 1 | 7,1% |
| Pedro Emanuel | 9 | 12 | 1,33 | 2 | 22,2% |

Pedro Emanuel reduz a média de gols sofridos em aproximadamente **15% em relação ao período de Renato Gaúcho** (1,57 → 1,33). A mudança mais evidente, porém, aparece na frequência de jogos sem sofrer gols: **7,1% → 22,2%**.

O resultado também exige cautela. Sete dos 12 gols sofridos no período de Pedro estão concentrados em apenas duas derrotas, contra Santos e Palmeiras. Isso faz com que a média de gols sofridos esconda parte da distribuição dos resultados.

Por isso, a análise não termina no placar. O pipeline também incorpora métricas de goalkeeping do FBref para investigar quantos chutes no alvo o Vasco permite e quanto do resultado pode estar associado à eficiência das defesas.

## O que estamos medindo

- **GA/jogo:** gols sofridos por partida;
- **Clean sheet rate:** percentual de jogos sem sofrer gols;
- **SoTA/jogo:** chutes no alvo sofridos por partida;
- **Saves/jogo:** defesas realizadas por partida;
- **Save% agregado:** `defesas / chutes no alvo`, calculado pelos totais e não pela média simples dos percentuais jogo a jogo;
- **SoTA por gol sofrido:** quantos chutes no alvo adversários são necessários, em média, para produzir um gol;
- **média móvel:** comportamento dos gols sofridos ao longo das partidas, reduzindo o peso visual de um único resultado.

## Recorte metodológico

A análise principal usa somente a Série A de 2026. Partidas de treinadores interinos permanecem na base, mas ficam fora da comparação entre os três técnicos.

| Treinador | Recorte usado |
|---|---|
| Fernando Diniz | jogos até 22/02/2026 |
| Renato Gaúcho | da estreia em 12/03/2026 até 18/06/2026 |
| Pedro Emanuel | desde a estreia em 16/07/2026 |

O critério considera quem efetivamente comandou a equipe na partida, não apenas a data de anúncio ou contratação.

## Um problema interessante de qualidade de dados

Durante a coleta, surgiu uma armadilha importante no HTML do FBref: a página de goalkeeping contém tabelas semanticamente opostas — **For Vasco da Gama** e **Against Vasco da Gama** — além de colunas com nomes repetidos em diferentes blocos.

Uma seleção ingênua da primeira tabela encontrada poderia inverter o significado das métricas. O coletor foi ajustado para identificar explicitamente a tabela do Vasco, e o pipeline passou a validar duplicidades, partidas sem resultado e totais antes de produzir os indicadores.

Esse cuidado é parte central do projeto: um gráfico pode estar tecnicamente correto e ainda assim responder à pergunta errada se a semântica da fonte não for validada.

## Pipeline

```text
FBref — Série A 2026
        ↓
partidas + goalkeeping
        ↓
limpeza e padronização
        ↓
validações de qualidade
        ↓
classificação por treinador
        ↓
métricas normalizadas
        ↓
visualizações + interpretação
```

Para reproduzir:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

O `run_pipeline.py` coleta as duas tabelas da Série A, processa os dados, calcula os indicadores e recria as visualizações.

## Visualizações geradas

O projeto produz automaticamente, quando as colunas necessárias estão disponíveis:

1. gols sofridos por jogo;
2. taxa de clean sheets;
3. chutes no alvo sofridos por jogo;
4. Save% agregado;
5. chutes no alvo necessários por gol sofrido;
6. evolução dos gols sofridos com média móvel de três partidas.

Os arquivos são gravados em `images/`.

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

## O que os dados dizem até aqui?

Os números sustentam uma leitura mais cuidadosa do que simplesmente afirmar que o Vasco passou a sofrer menos gols.

No período de Pedro Emanuel, a média de gols sofridos é menor que no período de Renato, mas o sinal mais forte está na **maior frequência de partidas sem ser vazado**. Ao mesmo tempo, duas goleadas têm peso elevado sobre a média do período de Pedro.

A próxima camada — SoTA, Saves e Save% — ajuda a separar duas perguntas diferentes: **o Vasco passou a permitir menos chegadas perigosas ou passou a sobreviver melhor às finalizações que permitiu?**

Essa distinção é importante porque gols sofridos são resultado; volume de finalizações no alvo e eficiência das defesas ajudam a explicar como esse resultado foi construído.

## Limitações

A análise descreve desempenho observado e não demonstra causalidade. Força dos adversários, mando, escalações, lesões, reforços, expulsões, calendário e tamanho desigual das amostras podem afetar os indicadores.

Além disso, SoTA não mede sozinho a qualidade das chances. Uma evolução futura natural seria incorporar xG/xGOT ou localização das finalizações, caso uma fonte consistente permita esse nível de detalhe.

## Fonte

Dados esportivos: FBref / Sports Reference.

O HTML bruto não é versionado. O repositório prioriza código reproduzível, validações e arquivos derivados necessários à análise.

## Autor

**Diego Neves**  
Jornalismo, Marketing e Análise de Dados
