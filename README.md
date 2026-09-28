# Vasco Defensive Analysis 2026

Análise da evolução defensiva do Vasco da Gama no Campeonato Brasileiro de 2026, comparando os períodos de Fernando Diniz, Renato Gaúcho e Pedro Emanuel com dados jogo a jogo do FBref.

## A pergunta

**O sistema defensivo do Vasco melhorou sob o comando de Pedro Emanuel?**

A ideia nasceu de uma percepção assistindo aos jogos. Em vez de partir da conclusão, o projeto transforma essa impressão em uma pergunta mensurável e deixa os dados responderem.

## Resultados — Série A

Recorte disponível no FBref até 12/09/2026:

| Treinador | Jogos | GA/jogo | Clean sheets | SoTA/jogo | Save% agregado | SoTA/gol |
|---|---:|---:|---:|---:|---:|---:|
| Fernando Diniz | 3 | 1,33 | 0,0% | 3,00 | 55,6% | 2,25 |
| Renato Gaúcho | 14 | 1,64 | 7,1% | 5,00 | 67,1% | 3,04 |
| Pedro Emanuel | 8 | 1,50 | 12,5% | 4,38 | 65,7% | 2,92 |

### O que mudou com Pedro Emanuel?

Comparado ao período de Renato Gaúcho, o Vasco passou de **5,00 para 4,38 chutes no alvo sofridos por jogo**, queda de aproximadamente **12,5%**. A média de gols sofridos caiu de **1,64 para 1,50 por partida**, redução de cerca de **8,7%**.

A taxa de clean sheets também subiu de **7,1% para 12,5%** no Brasileirão. Ao mesmo tempo, o Save% agregado permaneceu próximo: **67,1% com Renato e 65,7% com Pedro**.

Esse ponto é especialmente interessante: a melhora observada não aparece acompanhada de um salto na eficiência das defesas do goleiro. O sinal mais consistente está na redução do volume de chutes no alvo concedidos ao adversário.

Ainda assim, a amostra de Pedro é menor e bastante sensível a resultados extremos. As derrotas por 3 a 0 para o Santos e 4 a 1 para o Palmeiras concentram **7 dos 12 gols sofridos** no período.

Por isso, a leitura mais adequada não é que Pedro Emanuel "resolveu" a defesa, mas que **há sinais de melhora defensiva no Brasileirão, sobretudo na redução de chutes no alvo permitidos, apesar de uma oscilação ainda relevante entre partidas**.

## Métricas

- **GA/jogo:** gols sofridos por partida;
- **Clean sheet rate:** percentual de partidas sem sofrer gols;
- **SoTA/jogo:** chutes no alvo sofridos por partida;
- **Saves/jogo:** defesas realizadas;
- **Save% agregado:** `defesas / chutes no alvo`, calculado pelos totais;
- **SoTA/gol:** quantidade de chutes no alvo adversários por gol sofrido;
- **média móvel:** evolução dos gols sofridos ao longo das partidas.

## Recorte metodológico

A análise principal usa somente a Série A de 2026. Jogos de interinos permanecem fora da comparação.

| Treinador | Recorte |
|---|---|
| Fernando Diniz | até 22/02/2026 |
| Renato Gaúcho | da estreia em 12/03/2026 até 18/06/2026 |
| Pedro Emanuel | desde a estreia em 16/07/2026 |

O critério considera quem efetivamente comandou a equipe na partida.

## Qualidade dos dados

A página de goalkeeping do FBref contém duas tabelas semanticamente opostas: **For Vasco da Gama** e **Against Vasco da Gama**. O projeto usa explicitamente `For Vasco da Gama`, pois nela SoTA representa os chutes no alvo enfrentados pelo Vasco.

Essa validação corrigiu uma versão preliminar da análise que utilizava uma base externa e atribuía incorretamente 9 jogos de Série A a Pedro Emanuel. No match log do FBref disponível até 12/09 são **8 jogos de Pedro**, além de um jogo interino em 26/02. O total fecha os 26 jogos disputados: 3 Diniz + 1 interino + 14 Renato + 8 Pedro.

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

## Visualizações

O projeto gera automaticamente gráficos de gols sofridos/jogo, clean sheets, SoTA/jogo, Save% agregado, SoTA por gol e evolução dos gols sofridos com média móvel.

## Estrutura

```text
.
├── .github/workflows/
├── data/processed/
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

## Limitações

A análise descreve desempenho observado e não demonstra causalidade. Força dos adversários, mando, escalações, lesões, reforços, expulsões, calendário e tamanhos diferentes de amostra podem afetar os indicadores.

SoTA também mede volume, não a qualidade de cada oportunidade. Uma evolução futura natural é incorporar xG/xGOT ou localização das finalizações caso haja uma fonte consistente.

## Fonte

FBref / Sports Reference — match logs de goalkeeping da Série A 2026.

## Autor

**Diego Neves**  
Jornalismo, Marketing e Análise de Dados
