# 🖥️ Setup em Outro Computador - Guia Completo

## 📋 O que você PRECISA para cada tarefa?

### 1️⃣ **Apenas VISUALIZAR/EDITAR o site Hugo**
✅ Arquivos necessários (JÁ NO GITHUB):
```
content/          ← Artigos formatados (.md)
layouts/          ← Templates Hugo
static/           ← Imagens, CSS, JS
themes/           ← Tema PaperMod
hugo.toml         ← Configuração
```

❌ NÃO precisa:
- `.env` (API key)
- `data/dossies/` (dossiês de pesquisa)
- `*_raw.md` (arquivos temporários)
- `.venv/` (ambiente virtual Python)

**Comandos:**
```bash
git clone <seu-repo>
cd Geode
hugo server  # Pronto! Site rodando
```

---

### 2️⃣ **GERAR NOVAS análises de ferramentas**
✅ Arquivos necessários:
```
scripts/gerador_artigos_v2.py  ← Script principal
requirements.txt               ← Dependências Python
.env (criar novo)              ← API key do Gemini
fila_processamento.txt         ← Lista de ferramentas
```

❌ NÃO precisa:
- `data/dossies/` antigos (gerará novos)
- Artigos existentes (gerará novos)

**Setup:**
```bash
git clone <seu-repo>
cd Geode
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Criar .env
copy .env.example .env
# Editar .env e adicionar sua GEMINI_API_KEY

# Processar ferramentas
python scripts/gerador_artigos_v2.py
```

---

### 3️⃣ **FORMATAR artigos já gerados pelo Gemini**
✅ Arquivos necessários:
```
scripts/formatar_artigo.py     ← Script formatador
content/**/*_raw.md            ← Artigos brutos (SE EXISTIREM)
requirements.txt               ← Para PyYAML
```

❌ NÃO precisa:
- `.env`
- `data/dossies/`

**Comandos:**
```bash
.venv\Scripts\activate
python scripts/formatar_artigo.py
```

---

### 4️⃣ **AUDITAR/VERIFICAR fontes das análises**
✅ Arquivos necessários:
```
data/dossies/*/site_*.txt           ← Textos dos sites
data/dossies/*/youtube_video_*.txt  ← Transcrições
data/dossies/*/metadata.json        ← Info da coleta
```

❌ NÃO precisa (mas é bom ter):
```
data/dossies/*/audios/              ← Áudios originais (GRANDES!)
```

**Problema:** Dossiês estão no `.gitignore`!

**Soluções:**
- **Opção A:** Backup manual (Google Drive/OneDrive)
- **Opção B:** Usar Git LFS (ver abaixo)
- **Opção C:** Commitar dossiês (repo ficará grande)

---

## 🔄 Como Baixar Dossiês em Outro PC

### Método 1: Backup Manual (Atual)
```bash
# No PC original
# Compactar dossiês
tar -czf dossies_backup.tar.gz data/dossies/
# Subir para Google Drive/OneDrive

# No PC novo
# Baixar do Drive
tar -xzf dossies_backup.tar.gz
```

### Método 2: Git LFS (Recomendado)
```bash
# Setup uma única vez
git lfs install
git lfs track "data/dossies/**/*.webm"
git lfs track "data/dossies/**/*.mp3"
git add .gitattributes
git commit -m "feat: adicionar Git LFS para áudios"

# Em outro PC
git lfs pull  # Baixa arquivos grandes
```

### Método 3: Commitar Tudo (Simples mas pesado)
```bash
# Remover do .gitignore
# Commitar normalmente
git add data/dossies/
git commit -m "chore: adicionar dossiês de pesquisa"
git push
```

---

## 📊 Análise de Tamanho dos Arquivos

| Tipo | Tamanho Aprox. | No GitHub? | Necessário para? |
|------|---------------|------------|------------------|
| Artigos `.md` | ~50KB cada | ✅ SIM | Hugo (site) |
| `*_raw.md` | ~30KB cada | ❌ NÃO | Apenas reprocessamento |
| Transcrições `.txt` | ~20KB cada | ✅ **SIM** | Auditoria |
| Áudios `.mp3/.webm` | ~5-50MB cada | ❌ NÃO | Nada (pode deletar) |
| `metadata.json` | ~5KB | ✅ **SIM** | Auditoria |

**Recomendação:** Commitar textos e metadata, ignorar áudios.

---

## ✅ Checklist de Setup

### PC Novo - Setup Básico (Hugo apenas)
- [ ] `git clone <repo>`
- [ ] `hugo server`
- [ ] ✅ Pronto!

### PC Novo - Setup Completo (Gerar análises)
- [ ] `git clone <repo>`
- [ ] `python -m venv .venv`
- [ ] `.venv\Scripts\activate`
- [ ] `pip install -r requirements.txt`
- [ ] Criar `.env` com `GEMINI_API_KEY`
- [ ] Baixar dossiês (se necessário)
- [ ] ✅ Pronto!

---

## 🔐 Segurança

**NUNCA commitar:**
- `.env` (API keys)
- Senhas, tokens, certificados
- `.venv/` (ambiente virtual)

**SEMPRE commitar:**
- `.env.example` (template sem dados sensíveis)
- Scripts Python
- `requirements.txt`
- Artigos finais `.md`

---

## 🆘 Troubleshooting

**"Hugo não encontra artigos"**
- Verifique se `content/` tem arquivos `.md`
- Rode `hugo server -D` (com drafts)

**"Script Python dá erro"**
- Ativou o `.venv`?
- Instalou dependências? `pip install -r requirements.txt`
- Criou `.env` com API key?

**"Dossiês não existem"**
- Normal! Estão no `.gitignore`
- Baixe backup manual ou use Git LFS
- Ou gere novos dossiês processando ferramentas

---

## 📝 Notas Importantes

1. **Dossiês são OPCIONAIS** para rodar o site
2. **Dossiês são ESSENCIAIS** para auditar análises
3. **API key é necessária** apenas para gerar NOVAS análises
4. **Hugo funciona independente** de Python/Gemini

---

**Dúvidas?** Consulte [README.md](README.md) para setup detalhado.
