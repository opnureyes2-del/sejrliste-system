# LÆRTE TIPS - Baseret på tidligere sejr

*Genereret: 2026-01-26 14:01*
*Baseret på: 39 mønstre fra 39 sejr*

## SUCCESS RATE
- SUCCESS RATE: 9/11 sejr opnår GRAND ADMIRAL (81%)
- **Optimering:** Fokusér på Pass 1 kvalitet for at reducere Pass 2-3 arbejde

## KENDTE FALDGRUBER
- BUG LÆRT: auto_learn.py fejlede fordi den ledte efter SEJR_LISTE.md i arkiver, men den fil SLETTES ved arkiver
  - **Forebyg:** Check for this issue in similar contexts

## BEDSTE WORKFLOWS
- WORKFLOW: 1. **PROJECT_BRIEF.md er essentiel** - En model skal kunne forstå projektet på <30 sekunder. Uden de
- WORKFLOW: 1. 3-pass systemet TVINGER forbedring - score SKAL stige mellem passes.
- WORKFLOW: 2. **Cross-references kræver opmærksomhed** - Når man henviser til filer i engelsk dokumentation, SK

## NYTTIGE VÆRKTØJER
- TOOL: 1. **Centraliseret script execution** via executor.py reducer duplikeret kode dramatisk
- TOOL: 1. Ved arkitekturændringer (f.eks. filnavne) → grep ALLE scripts for referencer FØRST

## TEKNISKE TIPS
- TECHNICAL: 3. Mock implementation tillader fuld test coverage uden API keys
- TECHNICAL: 4. 13 tests sikrer robusthed i alle edge cases

## GENBRUGELIGE RESSOURCER
- REUSABLE TEMPLATE: 9 identificeret
- REUSABLE SCRIPT: 9 identificeret
- REUSABLE PATTERN: 9 identificeret

## ADMIRAL VISDOM

```
1. ÉN TING AD GANGEN - Færdiggør før du starter nyt
2. BEVIS IKKE TOMME ORD - Vis kørende kode, ikke planer
3. 3-PASS TVINGER FORBEDRING - Score SKAL stige
4. 7-DNA GENNEMGANG - Check alle lag før arkivering
5. OVERRASK - Gør mere end forventet
```
