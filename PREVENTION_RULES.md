# 🛡️ PREVENTION RULES - OBLIGATORISK FOR AI

> **DENNE FIL SKAL LÆSES FØR ENHVER ÆNDRING I SEJRLISTE SYSTEMET**

---

## ⛔ FORBUDTE HANDLINGER

### 1. ALDRIG ændre CSS/design uden eksplicit ordre
**Problem:** AI lavede CSS-ændringer der ødelagde designet
**Prevention:**
- [ ] CSS-ændringer kræver eksplicit "ændr CSS" ordre fra Rasmus
- [ ] ALDRIG "fix" noget visuelt uden at vise FØR/EFTER screenshot

### 2. ALDRIG ændre kode der virker
**Problem:** AI ændrede fungerende kode til noget værre
**Prevention:**
- [ ] Før ændring: Dokumentér HVAD der er galt (specifikt problem)
- [ ] Før ændring: Få godkendelse fra Rasmus
- [ ] Efter ændring: Bevis at det stadig virker + forbedring

### 3. ALTID læs eksisterende dokumentation først
**Problem:** AI ignorerede SESSION-filer der forklarede design-beslutninger
**Prevention:**
- [ ] Læs CLAUDE.md i sejr-mappen
- [ ] Læs SESSION_*.md filer i _CURRENT/
- [ ] Læs SEJR_LISTE.md for at forstå hvad der er gjort

### 4. ALTID verificer FUNKTION ikke bare KODE
**Problem:** AI verificerede at kode eksisterede, ikke at det virkede
**Prevention:**
- [ ] Test HVAD knapper gør (ikke bare at de eksisterer)
- [ ] Test HVAD skærme viser (ikke bare at de renderer)
- [ ] Dokumentér FAKTISKE resultater

---

## ✅ OBLIGATORISKE HANDLINGER FØR KODEÆNDRING

```bash
# 1. Check git status først
git status

# 2. Læs eksisterende state
cat 10_ACTIVE/*/CLAUDE.md
cat _CURRENT/SESSION*.md

# 3. Forstå HVAD der skal ændres og HVORFOR
# Dokumentér dette INDEN du begynder

# 4. Lav backup
git stash  # eller commit current state

# 5. Lav ændring

# 6. Test ændring
python3 -m py_compile [fil]
curl http://localhost:PORT

# 7. Verificer FUNKTIONALITET (ikke bare syntax)
# Beskriv hvad der er ændret og BEVIS det virker

# 8. Commit med beskrivende besked
git add . && git commit -m "ÆNDRING: [beskrivelse]"
```

---

## 🚨 HVIS DU ER I TVIVL

1. **STOP** - Lav INGEN ændringer
2. **SPØRG** - Beskriv hvad du vil ændre og hvorfor
3. **VENT** - Få godkendelse før du fortsætter

---

## 📋 ÆNDRING CHECKLISTE

Før ENHVER kodeændring:

- [ ] Jeg har læst CLAUDE.md i sejr-mappen
- [ ] Jeg har forstået HVORFOR ændringen er nødvendig
- [ ] Rasmus har EKSPLICIT bedt om denne ændring
- [ ] Jeg har dokumenteret FØR-state
- [ ] Jeg har en REVERT plan (git checkout)

Efter ændring:

- [ ] Syntax check passed
- [ ] App kører (HTTP 200)
- [ ] FUNKTIONALITET verificeret (ikke bare kode)
- [ ] Git committed med beskrivende besked
- [ ] EFTER-state dokumenteret med BEVIS

---

**Oprettet:** 2026-01-26
**Årsag:** AI lavede CSS-ændringer der ødelagde web_app.py uden godkendelse
**Løsning:** Denne fil SKAL læses før enhver ændring

