# 🚀 Geode - Plataforma de Análise de Ferramentas SaaS

Sistema automatizado de pesquisa e análise de ferramentas para PMEs brasileiras.

## 📋 Pré-requisitos

- Python 3.8+
- Node.js (para Hugo)
- Conta Google AI Studio (para API Gemini)

## 🔧 Configuração Inicial

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd Geode
```

### 2. Configure o ambiente Python
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente
```bash
# Copie o template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edite .env e adicione sua API key do Gemini
# Obtenha em: https://aistudio.google.com/app/apikey
```

Edite `.env`:
```env
GEMINI_API_KEY=sua_chave_aqui
```

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` no Git! Ele já está no `.gitignore`.

### 4. Instale dependências adicionais (se necessário)
```bash
pip install python-dotenv google-generativeai youtube-transcript-api beautifulsoup4 requests pyyaml
```

## 🎯 Como Usar

### Gerar Análises de Ferramentas
```bash
python scripts/gerador_artigos_v2.py
```

### Formatar Artigos (converter _raw.md para formato final)
```bash
python scripts/formatar_artigo.py
```

### Executar site Hugo localmente
```bash
hugo server
```

## 📁 Estrutura do Projeto

```
Geode/
├── .env                    # Variáveis de ambiente (NÃO commitar!)
├── .env.example           # Template de configuração
├── content/               # Artigos e páginas do site
│   ├── atendimento/
│   ├── marketing/
│   ├── produtividade/
│   └── vendas/
├── data/
│   └── dossies/          # Dados brutos coletados
├── scripts/
│   ├── gerador_artigos_v2.py   # Crawler + Gemini
│   └── formatar_artigo.py      # Formatador de markdown
└── public/               # Site gerado (Hugo)
```

## 🔐 Segurança

- **API Keys**: Sempre use variáveis de ambiente (`.env`)
- **Git**: Verifique `.gitignore` antes de commitar
- **Vazamento**: Se uma key vazar, revogue imediatamente no Google AI Studio

## 📊 Limites da API Gemini (Free Tier)

- 20 requests/dia
- 5 requests/minuto
- 250K tokens/minuto
- Delay automático: 12s entre requests

## 🛠️ Troubleshooting

### "API Key não encontrada"
Verifique se:
1. Arquivo `.env` existe na raiz do projeto
2. Variável `GEMINI_API_KEY` está preenchida
3. Ativou o ambiente virtual (`.venv`)

### "Limite diário atingido"
Aguarde reset às 00:00 UTC (horário do Google).

## 📝 Workflow

1. Adicione ferramentas em `fila_processamento.txt`
2. Execute `gerador_artigos_v2.py` para coletar dados e gerar análises
3. Execute `formatar_artigo.py` para formatar os artigos
4. Revise manualmente os artigos gerados
5. Publique com `hugo`

## 🤝 Contribuindo

1. Nunca commite arquivos `.env` ou API keys
2. Use `.env.example` como referência
3. Teste localmente antes de push

## 📄 Licença

[Defina sua licença aqui]
