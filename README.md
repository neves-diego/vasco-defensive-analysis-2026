# Vasco Defensive Analysis 2026

Análise da evolução defensiva do Vasco da Gama em 2026, comparando os períodos de Fernando Diniz, Renato Gaúcho e Pedro Emanuel, com foco no Campeonato Brasileiro e dados do FBref.

> Projeto em desenvolvimento. A coleta, o tratamento e as visualizações serão estruturados de forma reproduzível em Python.

## Pergunta de análise

**O sistema defensivo do Vasco melhorou sob o comando de Pedro Emanuel?**

A proposta é testar essa percepção com dados, evitando comparar apenas totais brutos. Como os treinadores comandaram quantidades diferentes de partidas, o projeto prioriza métricas por jogo, taxas e evolução temporal.

## Recorte

- Clube: Vasco da Gama
- Temporada: 2026
- Análise principal: Campeonato Brasileiro
- Técnicos comparados: Fernando Diniz, Renato Gaúcho e Pedro Emanuel
- Jogos de treinadores interinos serão mantidos separados para não contaminar os recortes.

## Métricas

Sempre que disponíveis na fonte:

- gols sofridos por jogo;
- clean sheets e taxa de clean sheets;
- finalizações sofridas;
- finalizações no alvo sofridas;
- eficiência defensiva;
- desempenho em casa e fora;
- evolução partida a partida;
- médias móveis.

## Estrutura planejada

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── images/
├── README.md
└── requirements.txt
```

## Metodologia

1. Coleta dos jogos e estatísticas disponíveis no FBref.
2. Padronização de datas, adversários, mando e resultados.
3. Associação de cada partida ao treinador responsável.
4. Separação do Brasileirão das demais competições.
5. Cálculo de métricas normalizadas por partida e percentuais.
6. Construção de visualizações comparativas e séries temporais.
7. Interpretação dos resultados com atenção ao tamanho das amostras e ao contexto competitivo.

## Fonte principal

Dados esportivos: FBref / Sports Reference.

Os dados brutos não serão tratados como propriedade do projeto. O repositório prioriza código reproduzível, dados derivados necessários à análise e indicação clara das fontes.

## Autor

Diego Neves
