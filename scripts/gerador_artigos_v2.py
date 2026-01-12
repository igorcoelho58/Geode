"""
GEODE SUPER CRAWLER V2.6 (Busca Inteligente + Logs Limpos)
===========================================================
ARQUITETURA: Fila é a ÚNICA fonte de verdade
- Todas as ferramentas pendentes estão em fila_processamento.txt
- Script lê EXCLUSIVAMENTE da fila (não usa lista hardcoded)
- Ferramentas são DELETADAS da fila após processamento com sucesso

FUNCIONALIDADES:
- Crawler Inteligente: Homepage + Pricing + Features + About + Extras
- Scraping Direto (SEM Google Search - Anti-Block)
- Busca Multilíngue YouTube (PT + EN + ES)
- Filtro de Qualidade: Descarta vídeos < 3.000 caracteres
- Whisper AI PRIORIZADO: Transcrição local para vídeos sem legendas
- Gemini 3.0 Flash Preview (1M tokens context)
- Sistema de Dossiê: Salva dados brutos para auditoria
- Validação rigorosa: Cross-check de preços/recursos
- Output: Markdown puro para formatação manual

FORMATO DO ARQUIVO fila_processamento.txt:
Nome da Ferramenta | Categoria

Exemplo:
Notion | produtividade
Zapier | produtividade
HubSpot CRM | vendas

MENU:
1. Processar 5 ferramentas da fila (batch - ~15 min)
2. Processar 1 ferramenta da fila (primeira)
3. Processar ferramenta específica da fila (buscar por nome)
4. Ver fila completa (ferramentas pendentes)
5. Sair
6. MODO DOSSIÊ: Criar dossiês SEM enviar ao Gemini
7. Processar 20 ferramentas da fila (batch COMPLETO - ~1h) 🔥

LIMITES (AI Studio - 28/12/2024):
- 20 requests/dia
- 5 requests/minuto
- 250K tokens/minuto
- Delay: 12s entre requests

FLUXO DE TRABALHO:
1. Edite fila_processamento.txt (adicione ferramentas no formato "Nome | Categoria")
2. Execute: python scripts/gerador_artigos_v2.py
3. Escolha opção (1, 2 ou 3)
4. Script processa e REMOVE automaticamente da fila
5. Repita até fila vazia (47 → 0)

Autor: Igor Coelho / Refinado por Gemini
Data: 27/12/2024
Última Atualização: 11/01/2026 - V2.7 (Batch 20 + Desligamento Automático)
"""

import os
import re
import time
import json
import requests
from datetime import datetime
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Bibliotecas de IA e YouTube
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Whisper (IA local para transcrição) + yt-dlp (download de áudio)
try:
    import whisper  # type: ignore
    import yt_dlp  # type: ignore
    from tqdm import tqdm  # type: ignore
    WHISPER_DISPONIVEL = True
except ImportError:
    WHISPER_DISPONIVEL = False
    print("⚠️ Whisper não instalado. Para fallback de IA local, instale: pip install openai-whisper yt-dlp tqdm")

# ============================================
# CONFIGURAÇÃO
# ============================================

# API Key (carregada de variável de ambiente - NUNCA commitar no Git!)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "❌ API Key não encontrada!\n"
        "   Configure a variável GEMINI_API_KEY no arquivo .env\n"
        "   Copie .env.example para .env e adicione sua chave"
    )

BASE_PATH = r"c:\Users\Igor\Documents\Projetos\Geode\content"
DOSSIES_PATH = r"c:\Users\Igor\Documents\Projetos\Geode\data\dossies"
MODELO_GEMINI = "gemini-3-flash-preview"  # Modelo experimental mais avançado (Gemini 3.0)

# ============================================
# LIMITES DA API GEMINI (Free Tier - Valores CONFIRMADOS via AI Studio)
# ============================================
# Fonte: https://aistudio.google.com/usage
# Limites verificados em 28/12/2024:
GEMINI_RPD = 20          # Requests Per Day (confirmado via AI Studio)
GEMINI_RPM = 5           # Requests Per Minute (confirmado via AI Studio)
GEMINI_TPM = 250000      # Tokens Per Minute (confirmado via AI Studio)
GEMINI_DELAY_MIN = 12    # Delay mínimo entre requests (segundos) = 60/RPM

# Contadores globais (serão resetados a cada execução do script)
gemini_requests_hoje = 0
gemini_ultima_request = None
gemini_tokens_ultimo_minuto = []  # Lista de (timestamp, tokens) do último minuto

# Headers para fingir ser um navegador real
HEADERS_BROWSER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7'
}

# Padrões de URL para descoberta inteligente (ordem de prioridade)
VARIACOES_FEATURES = [
    "/features",
    "/product", 
    "/funcionalidades",
    "/recursos",
    "/tour",
    "/platform",
    "/capabilities",
    "/solutions",
    "/use-cases",
    "/customers",
    "/case-studies",
    "/why",
    "/how-it-works"
]

# Novas páginas para varredura extra (blog, reviews, etc)
VARIACOES_EXTRAS = [
    "/blog",
    "/resources",
    "/reviews",
    "/testimonials",
    "/demo",
    "/overview"
]

# Mapeamento de ferramentas
FERRAMENTAS_POR_CATEGORIA = {
    "atendimento": [
        "Intercom", "Octadesk", "Respond.io", "Take Blip", 
        "Tidio Chat", "Typebot", "Wati WhatsApp", "Zendesk Service"
    ],
    "marketing": [
        "ActiveCampaign", "Canva Pro", "Copy.ai", "Descript", "ElevenLabs",
        "Gamma App", "HeyGen AI", "InVideo AI", "Jasper AI", "Leadster",
        "Leonardo AI", "Midjourney", "mLabs", "Opus Clip", "Trakto Design"
    ],
    "produtividade": [
        "Asana", "Bitrix24", "ClickUp", "Conta Azul", "Fireflies AI",
        "Make.com", "Monday.com", "Notion", "Otter AI", "Pipefy",
        "Slack", "tldv.io", "Trello", "Zapier"
    ],
    "vendas": [
        "Apollo.io", "Clay AI", "Close CRM", "Freshsales CRM", "HubSpot CRM",
        "Kommo CRM", "Meetime", "Moskit CRM", "Pipedrive CRM", "Ploomes",
        "RD Station CRM", "Salesforce Starter", "Snov.io", "Zoho CRM"
    ]
}

PRIORIDADES = [
    "HubSpot CRM", "Pipedrive CRM", "RD Station CRM", 
    "ActiveCampaign", "Notion"  # TOP 5 (ajustado para segurança de rate limit)
]

# Ferramentas secundárias (processar depois)
SECUNDARIAS = [
    "ClickUp", "Zapier", "Monday.com", "Asana", "Trello"
]

# ============================================
# MAPEAMENTO DE URLS OFICIAIS
# ============================================

URLS_CONHECIDAS = {
    "hubspot crm": {"site": "https://www.hubspot.com/", "pricing": "https://www.hubspot.com/pricing/sales"},
    "pipedrive crm": {"site": "https://www.pipedrive.com/", "pricing": "https://www.pipedrive.com/pricing"},
    "rd station crm": {"site": "https://www.rdstation.com/", "pricing": "https://www.rdstation.com/pricing/"},
    "activecampaign": {"site": "https://www.activecampaign.com/", "pricing": "https://www.activecampaign.com/pricing"},
    "notion": {"site": "https://www.notion.so/", "pricing": "https://www.notion.so/pricing"},
    "clickup": {"site": "https://clickup.com/", "pricing": "https://clickup.com/pricing"},
    "zapier": {"site": "https://zapier.com/", "pricing": "https://zapier.com/pricing"},
    "monday.com": {"site": "https://monday.com/", "pricing": "https://monday.com/pricing"},
    "asana": {"site": "https://asana.com/", "pricing": "https://asana.com/pricing"},
    "trello": {"site": "https://trello.com/", "pricing": "https://trello.com/pricing"},
    "slack": {"site": "https://slack.com/", "pricing": "https://slack.com/pricing"},
    "agendor": {"site": "https://www.agendor.com.br/", "pricing": "https://www.agendor.com.br/planos/"},
    "meetime": {"site": "https://meetime.com.br/", "pricing": "https://meetime.com.br/planos/"},
    "chatwoot": {"site": "https://www.chatwoot.com/", "pricing": "https://www.chatwoot.com/pricing"},
    "manychat": {"site": "https://manychat.com/", "pricing": "https://manychat.com/pricing"}
}

# ============================================
# PROMPT OTIMIZADO V2 - SEM "SE ENTREGAR"
# ============================================

PROMPT_TEMPLATE = """Você é um analista sênior de ferramentas SaaS para PMEs brasileiras. Sua especialidade é criar análises profundas, honestas e humanizadas baseadas em pesquisa rigorosa de mercado.

⚠️ **ATENÇÃO CRÍTICA**: Alguns vídeos/transcrições fornecidos podem ser IRRELEVANTES (sobre outras ferramentas ou tópicos aleatórios). 
Você é responsável por FILTRAR e DESCARTAR qualquer conteúdo que não esteja relacionado à ferramenta sendo analisada.
USE APENAS conteúdo pertinente. Reporte vídeos descartados na seção VALIDAÇÃO.

**FERRAMENTA:** {nome_ferramenta}
**CATEGORIA:** {categoria}
**SITE OFICIAL:** {link_oficial}

---

## DADOS COLETADOS DA PESQUISA

### INFORMAÇÕES DO SITE OFICIAL (Preços, Features, Planos)
```
{texto_site}
```

### ANÁLISES DE MERCADO E REVIEWS DE USUÁRIOS
```
{transcricoes}
```

---

## INSTRUÇÕES DE ESCRITA

**TOM E ESTILO:**
- Escreva como um analista humano experiente que PESQUISOU a ferramenta
- NUNCA mencione "vídeos", "transcrições", "análise de conteúdo" ou similares
- Use frases como: "Na prática observa-se que...", "Usuários relatam...", "A experiência mostra..."
- Seja crítico quando necessário - não é publieditorial

**FILTRO DE RELEVÂNCIA (CRÍTICO):**
ANTES de iniciar a análise, você DEVE avaliar cada transcrição/análise de mercado fornecida:
- **DESCARTE IMEDIATAMENTE** qualquer vídeo/conteúdo que NÃO esteja relacionado à ferramenta {nome_ferramenta}
- Vídeos aleatórios, sobre outras ferramentas, ou genéricos demais DEVEM ser IGNORADOS
- Você é o FILTRO INTELIGENTE - se um vídeo não menciona a ferramenta ou fala de assunto diferente, NÃO USE
- **IMPORTANTE**: Mencione na seção VALIDAÇÃO quantos vídeos foram descartados por irrelevância (se houver)

**INSTRUÇÃO CRÍTICA DE USO DAS FONTES:**
Você DEVE integrar as informações das duas seções acima (Site Oficial + Análises de Mercado) em sua análise. 
**NÃO IGNORE AS ANÁLISES DE MERCADO** - elas contêm experiências reais de usuários que são essenciais para:
- Identificar problemas práticos que não aparecem no site oficial
- Entender a curva de aprendizado real
- Avaliar a qualidade do suporte
- Citar casos de uso autênticos
- Mencionar bugs ou limitações conhecidas

**HIERARQUIA DE FONTES (MUITO IMPORTANTE):**
1. **SITE OFICIAL = VERDADE ABSOLUTA** - Use para preços, recursos, especificações técnicas
   - O criador da ferramenta NÃO colocaria informação falsa no próprio site
   - Dados do site têm credibilidade institucional e responsabilidade legal
   - Se o site diz "integra com Salesforce", você pode afirmar isso com certeza
   - **VALIDAÇÃO OBRIGATÓRIA**: SEMPRE cross-check preços e recursos do site oficial
   - Se uma análise mencionar "US$ 50/mês" mas o site diz "US$ 75/mês", use o valor do SITE

2. **ANÁLISES DE MERCADO E REVIEWS = EXPERIÊNCIA REAL** - Use para prós/contras, casos de uso, críticas
   - OBRIGATÓRIO: Cite insights das análises em TODAS as seções do corpo (Como Funciona, Casos de Uso, etc)
   - Opiniões de usuários podem ser subjetivas mas são valiosas e DEVEM ser incluídas
   - Use para humanizar a análise: "Usuários relatam que...", "Na prática, observa-se...", "Segundo especialistas..."
   - Críticas negativas são importantes - inclua quando relevantes nos CONTRAS
   - **ATENÇÃO**: Se análise contradizer o site oficial em FATOS (preços/recursos), priorize o SITE
   - Use análises para EXPERIÊNCIAS SUBJETIVAS (facilidade de uso, suporte, bugs, satisfação), não para specs

**CONTEÚDO:**
- Use os dados do site oficial para PREÇOS EXATOS, RECURSOS, INTEGRAÇÕES, PLANOS (verdade absoluta)
- **OBRIGATÓRIO**: Use as análises de mercado para EXPERIÊNCIA DE USO, PRÓS/CONTRAS REAIS, CASOS PRÁTICOS
- Traduza todo conteúdo internacional automaticamente para PT-BR natural
- Preços em Reais quando disponível, caso contrário indique a moeda original
- **VALIDAÇÃO**: Cada seção do corpo DEVE conter pelo menos uma referência indireta às análises de usuários

**FORMATAÇÃO:**
- Output em Markdown puro, SEM HTML
- Estrutura: Hook → Description → Veredito → O que é → Para quem → Prós → Contras → Preços → Corpo → FAQ

---

## OUTPUT ESPERADO (MARKDOWN PURO)

### HOOK (50-80 caracteres)
[Frase impactante sobre o principal benefício]

### DESCRIPTION (150-250 caracteres)  
[Descrição completa para SEO]

### VEREDITO (80-120 palavras)
[Análise crítica: para quem é ideal, quando vale, quando evitar]

### O QUE É? (80-120 palavras)
[Explicação objetiva: problema que resolve, público-alvo]

### PARA QUEM É INDICADO? (100-150 palavras)
[Perfil ideal de usuário, quando NÃO é recomendado]

### PRÓS
- [Item 1 - sem emoji, 10-15 palavras]
- [Item 2]
- [Continue... mínimo 5, máximo 8]

### CONTRAS  
- [Item 1 - sem emoji, 10-15 palavras]
- [Item 2]
- [Continue... mínimo 4, máximo 7]

### PREÇOS (use EXATAMENTE os dados do site oficial)
**PLANO 1:**
- Nome: [Ex: Gratuito]
- Preço: [Ex: R$ 0/mês ou US$ 0/month]
- Descrição: [1 linha sobre o que inclui]

**PLANO 2:**
- Nome: [Ex: Starter]  
- Preço: [Ex: R$ 149/mês ou US$ 20/user/month]
- Descrição: [1 linha]

[Continue com TODOS os planos listados no site]

### CORPO DA ANÁLISE

## Como Funciona na Prática?
[300-400 palavras: experiência de uso, onboarding, interface, curva de aprendizado]

## Casos de Uso Reais  
[250-350 palavras: 3-4 cenários práticos de PMEs brasileiras]

## Recursos Principais
[300-400 palavras: principais funcionalidades e diferenciais]

## Integrações e Ecossistema
[150-200 palavras: integrações disponíveis, API, marketplace]

## Nossa Avaliação Final
[150-200 palavras: resumo crítico, custo-benefício, recomendação]

### FAQ (5-7 perguntas em formato YAML)
```yaml
faq:
  - question: "[Pergunta relevante sobre funcionalidade/preço/uso]"
    answer: "[Resposta direta, 80-150 palavras]"
  
  - question: "[Pergunta sobre integração/limitação]"
    answer: "[Resposta objetiva]"
  
  [Continue com mais 3-5 perguntas pertinentes]
```

### VALIDAÇÃO
- Data da Análise: {data_hoje}
- Link Oficial Validado: ✅ {link_oficial}
- Preços Confirmados: ✅ Extraídos diretamente do site oficial
- Páginas do Site Coletadas: {paginas_coletadas}
- Vídeos Analisados: {total_videos} vídeos{urls_videos}
- Vídeos Descartados por Irrelevância: [PREENCHA: número de vídeos que você identificou como não relacionados à ferramenta]
- Transcrições Lidas: {status_transcricoes}
- Idiomas das Fontes: {idiomas}
- Total de Caracteres Analisados: {total_caracteres}
- Dossiê Completo Salvo: ✅ data/dossies/{slug_ferramenta}/

---

**LEMBRETE CRÍTICO:** Você é um ANALISTA HUMANO escrevendo uma PESQUISA. Nunca revele suas fontes técnicas (vídeos/transcrições). Escreva naturalmente.
"""

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def gerar_nome_arquivo(numero, titulo, extensao="txt", max_chars=50):
    """Gera nome de arquivo padronizado: 01_titulo_video.txt
    
    Args:
        numero: Número sequencial do arquivo (1, 2, 3...)
        titulo: Título original do vídeo/conteúdo
        extensao: Extensão do arquivo (txt, mp3, etc) sem o ponto
        max_chars: Limite máximo de caracteres para o título
    
    Returns:
        String no formato: "01_titulo_truncado.txt"
    
    Exemplo:
        gerar_nome_arquivo(1, "Review Completo do Notion 2024", "txt")
        → "01_Review_Completo_do_Notion_2024.txt"
    """
    # Remove caracteres proibidos em nomes de arquivo
    titulo_limpo = re.sub(r'[<>:"/\\|?*]', '', titulo)
    
    # Substitui espaços por underscores
    titulo_limpo = re.sub(r'\s+', '_', titulo_limpo.strip())
    
    # Limita tamanho e remove underscore final se houver
    titulo_limpo = titulo_limpo[:max_chars].rstrip('_')
    
    # Retorna formato: "01_titulo.ext"
    return f"{numero:02d}_{titulo_limpo}.{extensao}"

# ============================================
# FUNÇÕES DE WEB SCRAPING
# ============================================

def obter_urls_ferramenta(nome_ferramenta):
    """Retorna URLs do site oficial e variações de pricing/features"""
    nome_lower = nome_ferramenta.lower()
    
    # Verifica se está no mapeamento manual (sempre prioritário)
    if nome_lower in URLS_CONHECIDAS:
        urls = URLS_CONHECIDAS[nome_lower]
        base_url = urls['site']
        return {
            "site": base_url,
            "pricing_urls": [urls['pricing']],
            "features_urls": [base_url.rstrip('/') + path for path in VARIACOES_FEATURES]
        }
    
    # Tenta inferir URLs baseado no nome
    slug = nome_lower.replace(" crm", "").replace(" ai", "").replace(" ", "")
    base_url = f"https://{slug}.com"
    
    # Múltiplas variações de URL de pricing
    pricing_variations = [
        f"{base_url}/pricing",
        f"{base_url}/plans",
        f"{base_url}/planos",
        f"{base_url}/precos",
        f"{base_url}/price",
        f"{base_url}/buy"
    ]
    
    # Múltiplas variações de URL de features
    features_variations = [base_url + path for path in VARIACOES_FEATURES]
    
    return {
        "site": base_url + "/",
        "pricing_urls": pricing_variations,
        "features_urls": features_variations
    }

def extrair_texto_limpo_site(url, limite_chars=None):
    """Entra na URL e extrai texto limpo (sem HTML). Retorna (texto, sucesso)
    
    limite_chars=None significa SEM LIMITE (vai com tudo!)
    """
    print(f"   🌍 Acessando: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS_BROWSER, timeout=30)
        if response.status_code != 200:
            print(f"   ❌ Status {response.status_code}")
            return None, False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove elementos não textuais
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript']):
            element.decompose()
        
        # Extrai texto
        texto = soup.get_text(separator='\n', strip=True)
        
        # Limpa linhas vazias excessivas
        linhas = [line.strip() for line in texto.splitlines() if line.strip()]
        texto_limpo = '\n'.join(linhas)
        
        # Aplica limite SOMENTE se especificado
        tamanho_original = len(texto_limpo)
        if limite_chars and len(texto_limpo) > limite_chars:
            texto_limpo = texto_limpo[:limite_chars] + "\n[...conteúdo truncado...]"
            print(f"   ✅ Extraídos {len(texto_limpo)} chars (truncado de {tamanho_original})")
        else:
            print(f"   ✅ Extraídos {len(texto_limpo)} caracteres (COMPLETO)")
        return texto_limpo, True
        
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️ Erro: {e}")
        return None, False

def coletar_dados_site_oficial(nome_ferramenta):
    """Coleta dados completos: Homepage + Pricing + Features + About
    Retorna: (conteudo_completo_string, dados_estruturados_dict)
    """
    urls = obter_urls_ferramenta(nome_ferramenta)
    base_url = urls['site']
    
    print(f"\n📄 Coletando dados do site oficial...")
    
    conteudo_completo = ""
    dados_estruturados = {
        "homepage": {"url": base_url, "texto": None, "sucesso": False},
        "pricing": {"url": None, "texto": None, "sucesso": False},
        "features": {"url": None, "texto": None, "sucesso": False},
        "about": {"url": None, "texto": None, "sucesso": False}
    }
    
    # 1. HOMEPAGE (visão geral e posicionamento)
    print(f"\n   🏠 HOMEPAGE:")
    texto_home, sucesso_home = extrair_texto_limpo_site(base_url, limite_chars=None)
    if sucesso_home:
        dados_estruturados["homepage"]["texto"] = texto_home
        dados_estruturados["homepage"]["sucesso"] = True
        conteudo_completo += f"\n{'='*70}\n"
        conteudo_completo += f"HOMEPAGE - {base_url}\n"
        conteudo_completo += f"{'='*70}\n"
        conteudo_completo += texto_home + "\n"
    else:
        print(f"   ⚠️ Homepage inacessível")
    
    # 2. PRICING PAGE (preços exatos - ESSENCIAL)
    print(f"\n   💰 PRICING:")
    
    for pricing_url in urls['pricing_urls']:
        texto_pricing, sucesso_pricing = extrair_texto_limpo_site(pricing_url, limite_chars=None)
        if sucesso_pricing:
            dados_estruturados["pricing"]["url"] = pricing_url
            dados_estruturados["pricing"]["texto"] = texto_pricing
            dados_estruturados["pricing"]["sucesso"] = True
            conteudo_completo += f"\n{'='*70}\n"
            conteudo_completo += f"PRICING PAGE - {pricing_url}\n"
            conteudo_completo += f"{'='*70}\n"
            conteudo_completo += texto_pricing + "\n"
            break  # Achou pricing, para de tentar
    
    if not dados_estruturados["pricing"]["sucesso"]:
        print(f"   ⚠️ Nenhuma página de pricing encontrada (tentou {len(urls['pricing_urls'])} URLs)")
    
    # 3. FEATURES PAGE (funcionalidades técnicas)
    print(f"\n   ⚙️ FEATURES:")
    
    for features_url in urls['features_urls']:
        texto_features, sucesso_features = extrair_texto_limpo_site(features_url, limite_chars=None)
        if sucesso_features:
            dados_estruturados["features"]["url"] = features_url
            dados_estruturados["features"]["texto"] = texto_features
            dados_estruturados["features"]["sucesso"] = True
            conteudo_completo += f"\n{'='*70}\n"
            conteudo_completo += f"FEATURES PAGE - {features_url}\n"
            conteudo_completo += f"{'='*70}\n"
            conteudo_completo += texto_features + "\n"
            break  # Achou features, para de tentar
    
    if not dados_estruturados["features"]["sucesso"]:
        print(f"   ⚠️ Nenhuma página de features encontrada (tentou {len(urls['features_urls'])} URLs)")
    
    # 4. ABOUT PAGE (informações da empresa)
    print(f"\n   ℹ️ ABOUT:")
    about_urls = [
        f"{base_url.rstrip('/')}/about",
        f"{base_url.rstrip('/')}/about-us",
        f"{base_url.rstrip('/')}/sobre",
        f"{base_url.rstrip('/')}/empresa"
    ]
    
    for about_url in about_urls:
        texto_about, sucesso_about = extrair_texto_limpo_site(about_url, limite_chars=None)
        if sucesso_about:
            dados_estruturados["about"]["url"] = about_url
            dados_estruturados["about"]["texto"] = texto_about
            dados_estruturados["about"]["sucesso"] = True
            conteudo_completo += f"\n{'='*70}\n"
            conteudo_completo += f"ABOUT PAGE - {about_url}\n"
            conteudo_completo += f"{'='*70}\n"
            conteudo_completo += texto_about + "\n"
            break  # Achou about, para de tentar
    
    # 5. PÁGINAS EXTRAS (blog, reviews, cases) - OPCIONAL MAS VALIOSO
    print(f"\n   📚 EXTRAS (blog, cases, reviews):")
    dados_estruturados["extras"] = []
    
    for path in VARIACOES_EXTRAS:
        extra_url = base_url.rstrip('/') + path
        texto_extra, sucesso_extra = extrair_texto_limpo_site(extra_url, limite_chars=100000)  # Limite maior para blogs
        
        if sucesso_extra:
            dados_estruturados["extras"].append({
                "tipo": path.replace('/', ''),
                "url": extra_url,
                "texto": texto_extra,
                "tamanho": len(texto_extra)
            })
            conteudo_completo += f"\n{'='*70}\n"
            conteudo_completo += f"EXTRA PAGE ({path}) - {extra_url}\n"
            conteudo_completo += f"{'='*70}\n"
            conteudo_completo += texto_extra + "\n"
            print(f"   ✅ {path}: {len(texto_extra)} chars")
            
            # Limita a 2 páginas extras para não sobrecarregar
            if len(dados_estruturados["extras"]) >= 2:
                print(f"   ℹ️ Limite de 2 páginas extras atingido")
                break
    
    if not dados_estruturados["extras"]:
        print(f"   ℹ️ Nenhuma página extra encontrada (não é crítico)")
    
    # Se não conseguiu NADA, retorna mensagem
    if not conteudo_completo:
        return f"⚠️ Não foi possível acessar nenhuma página de {base_url}. Use conhecimento interno.", dados_estruturados
    
    print(f"\n   📊 Coletados {len(conteudo_completo)} caracteres do site oficial")
    return conteudo_completo, dados_estruturados

# ============================================
# FUNÇÕES DE YOUTUBE MULTILÍNGUE
# ============================================

def verificar_duracao_video(video_id):
    """Verifica APENAS a duração do vídeo sem baixar.
    Retorna: (duracao_segundos, titulo) ou (0, None) se erro
    """
    try:
        with yt_dlp.YoutubeDL({
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'extract_flat': False,
        }) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
            return info.get('duration', 0), info.get('title', 'Sem título')
    except Exception:
        return 0, None


def transcrever_com_whisper(video_url, video_id, video_titulo, pasta_dossie=None, numero_video=None):
    """Baixa o áudio do YouTube e transcreve usando IA local (Whisper)
    FALLBACK quando youtube-transcript-api não achar legendas oficiais
    
    Args:
        video_url: URL do vídeo
        video_id: ID do vídeo (usado como fallback no nome)
        video_titulo: Título do vídeo para nome do arquivo
        pasta_dossie: Caminho do dossiê para salvar o áudio (opcional)
        numero_video: Número sequencial do vídeo para nomenclatura (opcional)
    """
    if not WHISPER_DISPONIVEL:
        return None
    
    print(f"      🎙️ Transcrevendo via IA local (Whisper)...")
    
    # Define onde salvar o áudio
    if pasta_dossie and os.path.exists(pasta_dossie):
        # Cria subpasta de áudios no dossiê
        pasta_audios = os.path.join(pasta_dossie, "audios")
        os.makedirs(pasta_audios, exist_ok=True)
        
        # Usa nomenclatura padronizada com numeração se disponível
        if numero_video is not None:
            nome_arquivo = gerar_nome_arquivo(numero_video, video_titulo, "mp3")
            temp_audio = os.path.join(pasta_audios, nome_arquivo)
        else:
            # Fallback: usa título limpo tradicional
            titulo_limpo = re.sub(r'[<>:"/\\|?*]', '', video_titulo)
            titulo_limpo = titulo_limpo[:100]
            temp_audio = os.path.join(pasta_audios, f"{titulo_limpo}.mp3")
    else:
        # Fallback: pasta temporária
        temp_audio = f"temp_audio_{video_id}.mp3"
    
    # Configurações para baixar apenas o áudio (economia de banda)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',  # Baixa qualidade é suficiente para voz
        }],
        'outtmpl': temp_audio.replace('.mp3', ''),  # Remove extensão, yt-dlp adiciona depois
        'quiet': True,  # Silencioso para terminal limpo
        'no_warnings': True,
        'ignoreerrors': True,
        'ignoreerrors': True,
        'keepvideo': False,
    }

    try:
        # Baixa o áudio do vídeo (duração já foi verificada antes)
        print(f"         📥 Baixando áudio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # 2. Verifica se o arquivo MP3 foi criado
        # yt-dlp cria: outtmpl + '.mp3' = temp_audio (sem extensão) + '.mp3'
        if not os.path.exists(temp_audio):
            print(f"         ❌ Arquivo MP3 não foi criado")
            print(f"         ℹ️ Esperado em: {temp_audio}")
            # Lista arquivos na pasta para debug
            pasta = os.path.dirname(temp_audio)
            if os.path.exists(pasta):
                arquivos = os.listdir(pasta)
                print(f"         ℹ️ Arquivos na pasta: {arquivos[:5]}")
            return None
        
        # 3. Valida tamanho do arquivo
        tamanho = os.path.getsize(temp_audio)
        if tamanho < 1000:
            print(f"         ❌ Arquivo MP3 muito pequeno: {tamanho} bytes")
            return None
        
        # 4. Carrega o modelo Whisper (usa GPU NVIDIA se disponível)
        # Modelos: tiny (rápido, 75MB), base (bom, 150MB), small (melhor, 500MB)
        print(f"         🧠 Carregando modelo de IA...")
        model = whisper.load_model("base")  # Compromise entre velocidade e qualidade
        
        # 5. Transcreve o arquivo (pode levar 1-3 minutos para vídeos de 10 min)
        print(f"         ⏳ Transcrevendo (isso pode demorar alguns minutos)...")
        
        try:
            result = model.transcribe(temp_audio, fp16=False)  # AUTO-DETECT LANGUAGE!
        except Exception as transcribe_error:
            print(f"         ❌ Erro ao transcrever: {str(transcribe_error)[:100]}")
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            return None
        
        # Exibe idioma detectado
        idioma_detectado = result.get('language', 'desconhecido')
        texto_transcrito = result['text'].strip()
        print(f"         🌍 Idioma detectado: {idioma_detectado}")
        print(f"         ✅ Whisper: {len(texto_transcrito):,} caracteres transcritos!")
        
        # 4. Valida tamanho mínimo (3000 chars) e DELETA áudio se muito curto
        TAMANHO_MINIMO = 3000
        if len(texto_transcrito) < TAMANHO_MINIMO:
            print(f"         ⚠️ Transcrição muito curta ({len(texto_transcrito)} chars < {TAMANHO_MINIMO}). Descartando áudio...")
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            return None  # Retorna None para indicar descarte
        
        # 5. Se chegou aqui, transcrição é válida - mantém ou deleta conforme contexto
        if not pasta_dossie:
            # Se for temp (não está no dossiê), aí sim deleta
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
        else:
            print(f"         💾 Áudio salvo: {os.path.basename(temp_audio)}")
        
        return texto_transcrito

    except Exception as e:
        erro_msg = str(e)
        print(f"         ❌ Whisper falhou: {erro_msg[:150]}")
        
        # Log completo do erro para debug
        if 'ffmpeg' in erro_msg.lower():
            print(f"         ℹ️ Problema de ffmpeg detectado. Arquivo: {temp_audio}")
            print(f"         ℹ️ Arquivo existe: {os.path.exists(temp_audio) if os.path.exists(temp_audio) else 'NÃO'}")
            if os.path.exists(temp_audio):
                print(f"         ℹ️ Tamanho: {os.path.getsize(temp_audio)} bytes")
        
        # Remove arquivo temporário em caso de erro (somente se não estiver no dossiê)
        if not pasta_dossie and os.path.exists(temp_audio):
            os.remove(temp_audio)
        return None

def buscar_videos_multilingue(nome_ferramenta, limite_por_idioma=10, max_videos=50):
    """Busca vídeos em PT, EN e ES ordenados por relevância (visualizações)
    
    Args:
        limite_por_idioma: Máximo de vídeos por query
        max_videos: Limite total de vídeos retornados (ordenados por views)
    """
    print(f"\n🎥 Buscando reviews multilíngues (até {max_videos} vídeos, ordenados por relevância)...")
    
    videos_encontrados = []
    video_ids_vistos = set()  # Rastreia IDs já processados (evita duplicatas)
    
    # Queries expandidas para garantir variedade
    queries = [
        (f"{nome_ferramenta} review vale a pena português", "PT-BR"),
        (f"{nome_ferramenta} tutorial completo brasil", "PT-BR"),
        (f"{nome_ferramenta} como usar tutorial", "PT-BR"),
        (f"{nome_ferramenta} review pros and cons", "EN"),
        (f"{nome_ferramenta} vs alternatives comparison", "EN"),
        (f"{nome_ferramenta} tutorial complete guide", "EN"),
        (f"{nome_ferramenta} opinión español", "ES"),
        (f"{nome_ferramenta} tutorial español", "ES")
    ]
    
    for query, idioma in queries:
        # Para de buscar se já atingiu o limite
        if len(videos_encontrados) >= max_videos:
            break
            
        try:
            url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
            response = requests.get(url, headers=HEADERS_BROWSER, timeout=10)
            
            # Extrai IDs, títulos e view counts
            video_ids = re.findall(r'"videoId":"([^"]{11})"', response.text)
            titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', response.text)
            view_counts = re.findall(r'"viewCountText":\{"simpleText":"([^"]+)"\}', response.text)
            
            # Cria lista com metadados para ordenação
            videos_temp = []
            for i, vid in enumerate(video_ids[:limite_por_idioma]):
                if len(videos_encontrados) >= max_videos:
                    break
                
                # ✅ DEDUPLICAÇÃO: Pula se vídeo já foi processado
                if vid in video_ids_vistos:
                    continue
                
                if i < len(titles):
                    # Extrai número de views (ex: "1.2M" -> 1200000)
                    views = 0
                    if i < len(view_counts):
                        view_str = view_counts[i].replace(',', '').replace('.', '')
                        if 'K' in view_str:
                            views = int(float(view_str.replace('K', '')) * 1000)
                        elif 'M' in view_str:
                            views = int(float(view_str.replace('M', '')) * 1000000)
                        elif 'mi' in view_str:  # "mi" = milhão em PT
                            views = int(float(view_str.split()[0].replace(',', '.')) * 1000000)
                        elif 'mil' in view_str:  # "mil" em PT
                            views = int(float(view_str.split()[0].replace(',', '.')) * 1000)
                        else:
                            try:
                                views = int(view_str.split()[0])
                            except:
                                views = 0
                    videos_temp.append((vid, titles[i], idioma, views))
                    video_ids_vistos.add(vid)  # ✅ Marca como visto
            
            # Ordena por visualizações (mais relevantes primeiro)
            videos_temp.sort(key=lambda x: x[3], reverse=True)
            
            # Adiciona à lista final (já deduplicados)
            for vid, title, lang, views in videos_temp:
                if len(videos_encontrados) < max_videos:
                    videos_encontrados.append((vid, title, lang))
                    
        except Exception as e:
            print(f"   ⚠️ Erro na busca {idioma}: {e}")
            continue
    
    print(f"   ✅ Encontrados {len(videos_encontrados)} vídeos candidatos")
    return videos_encontrados

def extrair_transcricoes_multilingue(nome_ferramenta, pasta_dossie=None):
    """Extrai transcrições multilíngues de vídeos do YouTube com filtro de qualidade.
    
    NOVO EM V2.7:
    - Filtra duração (>5min) ANTES de processar
    - Contador de falhas corrigido (não conta vídeos curtos como falha)
    - Prompt interativo para buscar mais vídeos se necessário
    
    Returns: (transcricoes_str, idiomas_list, videos_dados_list)
    """
    # PASSO 1: Buscar 50 vídeos candidatos
    videos_candidatos = buscar_videos_multilingue(nome_ferramenta, max_videos=50)
    
    if not videos_candidatos:
        return "Sem vídeos encontrados no YouTube.", [], []
    
    # PASSO 2: Filtrar por duração (>5min) ANTES de processar
    print(f"\n🔍 Filtrando {len(videos_candidatos)} vídeos por duração (mínimo 5 min)...")
    videos_validos = []
    video_ids_processados = set()  # ✅ Evita duplicatas na filtragem
    
    for video_id, titulo, idioma in videos_candidatos:
        # ✅ DEDUPLICAÇÃO: Pula se vídeo já foi processado
        if video_id in video_ids_processados:
            print(f"   🔁 Duplicata ignorada: {titulo[:60]}...")
            continue
        
        video_ids_processados.add(video_id)
        
        duracao, titulo_real = verificar_duracao_video(video_id)
        if titulo_real:
            titulo = titulo_real  # Atualiza com título real
        
        if duracao >= 300 and duracao <= 3600:  # 5-60 minutos
            videos_validos.append((video_id, titulo, idioma, duracao))
            print(f"   ✅ {titulo[:60]}... ({duracao//60}min{duracao%60}s)")
        elif duracao < 300:
            print(f"   ⏭️ {titulo[:60]}... ({duracao}s - muito curto)")
        else:
            print(f"   ⏭️ {titulo[:60]}... ({duracao//60}min{duracao%60}s - muito longo, máx 60min)")
    
    print(f"\n📊 Resultado: {len(videos_validos)} vídeos válidos (>5min) de {len(videos_candidatos)} candidatos")
    
    # PASSO 3: Se <5 vídeos, buscar automaticamente mais 25 (1ª expansão)
    if len(videos_validos) < 5:
        print(f"\n⚠️ Encontrados apenas {len(videos_validos)} vídeos acima de 5 minutos")
        print("🔄 Buscando automaticamente mais 25 vídeos (1ª expansão)...")
        
        videos_extras = buscar_videos_multilingue(nome_ferramenta, max_videos=25)
        
        print(f"🔍 Filtrando {len(videos_extras)} vídeos extras por duração...")
        for video_id, titulo, idioma in videos_extras:
            # Evita duplicatas
            if video_id not in [v[0] for v in videos_validos]:
                duracao, titulo_real = verificar_duracao_video(video_id)
                if titulo_real:
                    titulo = titulo_real
                
                if duracao >= 300 and duracao <= 3600:
                    videos_validos.append((video_id, titulo, idioma, duracao))
                    print(f"   ✅ {titulo[:60]}... ({duracao//60}min{duracao%60}s)")
                elif duracao < 300:
                    print(f"   ⏭️ {titulo[:60]}... ({duracao}s - muito curto)")
                else:
                    print(f"   ⏭️ {titulo[:60]}... ({duracao//60}min{duracao%60}s - muito longo, máx 60min)")
        
        print(f"\n📊 Após 1ª expansão: {len(videos_validos)} vídeos válidos")
    
    # PASSO 4: Se ainda <5 vídeos, buscar automaticamente mais 25 (2ª expansão)
    if len(videos_validos) < 5:
        print(f"\n⚠️ Ainda insuficiente: {len(videos_validos)} vídeos válidos")
        print("🔄 Buscando automaticamente mais 25 vídeos (2ª expansão)...")
        
        videos_extras2 = buscar_videos_multilingue(nome_ferramenta, max_videos=25)
        
        print(f"🔍 Filtrando {len(videos_extras2)} vídeos extras por duração...")
        for video_id, titulo, idioma in videos_extras2:
            # Evita duplicatas
            if video_id not in [v[0] for v in videos_validos]:
                duracao, titulo_real = verificar_duracao_video(video_id)
                if titulo_real:
                    titulo = titulo_real
                
                if duracao >= 300 and duracao <= 3600:
                    videos_validos.append((video_id, titulo, idioma, duracao))
                    print(f"   ✅ {titulo[:60]}... ({duracao//60}min{duracao%60}s)")
                elif duracao < 300:
                    print(f"   ⏭️ {titulo[:60]}... ({duracao}s - muito curto)")
                else:
                    print(f"   ⏭️ {titulo[:60]}... ({duracao//60}min{duracao%60}s - muito longo, máx 60min)")
        
        print(f"\n📊 Após 2ª expansão: {len(videos_validos)} vídeos válidos")
    
    # PASSO 5: Verifica se encontrou PELO MENOS 1 vídeo (senão aborta)
    if len(videos_validos) == 0:
        print(f"\n❌ ERRO: Nenhum vídeo válido encontrado após 2 expansões (50+25+25 vídeos buscados)")
        return "Nenhum vídeo válido encontrado no YouTube.", [], []
    
    # PASSO 6: Processar os vídeos encontrados (até 5, ou menos se não houver 5)
    videos = videos_validos[:5]
    print(f"\n🎯 Processando {len(videos)} vídeo(s) encontrado(s):")
    for i, (video_id, titulo, idioma, duracao) in enumerate(videos, 1):
        print(f"   {i}. {titulo[:70]}... ({duracao//60}min{duracao%60}s, {idioma})")
    
    print(f"\n📥 Extraindo transcrições dos {len(videos)} vídeos (WHISPER PRIORITÁRIO)...")
    
    # PASSO 7: Processar os vídeos selecionados
    ytt_api = YouTubeTranscriptApi()
    transcricoes_completas = ""
    idiomas_usados = set()
    videos_dados = []
    videos_descartados = []
    count_sucesso = 0
    falhas_whisper_reais = 0
    MAX_FALHAS_WHISPER = 3
    TAMANHO_MINIMO = 3000
    
    for idx, (video_id, titulo, idioma_busca, duracao) in enumerate(videos, 1):
        print(f"\n   🎬 Vídeo {idx}/{len(videos)}: {titulo[:70]}... ({duracao//60}min{duracao%60}s)")
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        texto_final = None
        tipo_legenda = "desconhecida"
        idioma_final = idioma_busca
        
        # ═════════════════════════════════════════════════════════
        # PRIORIDADE 1: WHISPER AI (vídeo já validado por duração!)
        # ═════════════════════════════════════════════════════════
        if WHISPER_DISPONIVEL and falhas_whisper_reais < MAX_FALHAS_WHISPER:
            print(f"   🎙️ Tentando Whisper IA primeiro...")
            texto_whisper = transcrever_com_whisper(video_url, video_id, titulo, pasta_dossie, idx)
            
            if texto_whisper and len(texto_whisper) >= TAMANHO_MINIMO:
                # ✅ Sucesso total
                texto_final = texto_whisper
                tipo_legenda = "whisper-ai"
                idioma_final = "pt (Whisper IA)"
                print(f"   ✅ Whisper: {len(texto_final):,} chars")
            elif texto_whisper:
                # ⚠️ Whisper OK, mas transcrição curta (vídeo tem pouco áudio falado)
                print(f"   ⚠️ Whisper OK, mas transcrição curta ({len(texto_whisper):,} chars < {TAMANHO_MINIMO:,}). Tentando legendas...")
                # NÃO incrementa falhas (Whisper funcionou!)
            else:
                # ❌ Whisper falhou (retornou None)
                falhas_whisper_reais += 1
                print(f"   ❌ Whisper falhou ({falhas_whisper_reais}/{MAX_FALHAS_WHISPER}). Tentando legendas...")
                if falhas_whisper_reais >= MAX_FALHAS_WHISPER:
                    print(f"   ⚠️ Whisper falhou {MAX_FALHAS_WHISPER}x. Usando apenas legendas daqui pra frente...")
        elif WHISPER_DISPONIVEL and falhas_whisper_reais >= MAX_FALHAS_WHISPER:
            print(f"   ℹ️ Pulando Whisper (muitas falhas). Tentando legendas YouTube...")
        
        # ═════════════════════════════════════════════════════════
        # PRIORIDADE 2: LEGENDAS OFICIAIS (fallback)
        # ═════════════════════════════════════════════════════════
        if not texto_final:
            print(f"   📜 Whisper falhou/indisponível, tentando legendas oficiais...")
            
            try:
                # Tenta acessar lista de legendas (pode lançar exceção)
                transcript_list = ytt_api.list(video_id)
                transcript = None
                
                # Tentativa 1: Legenda MANUAL nos idiomas preferidos
                try:
                    transcript = transcript_list.find_manually_created_transcript(['pt', 'pt-BR', 'en', 'en-US', 'es'])
                    tipo_legenda = "manual"
                except:
                    pass
                
                # Tentativa 2: Legenda AUTO-GERADA
                if not transcript:
                    try:
                        transcript = transcript_list.find_generated_transcript(['pt', 'pt-BR', 'en', 'en-US', 'es'])
                        tipo_legenda = "auto-gerada"
                    except:
                        pass
                
                # Tentativa 3: QUALQUER legenda disponível
                if not transcript:
                    try:
                        for t in transcript_list:
                            transcript = t
                            tipo_legenda = "disponível"
                            break
                    except:
                        pass
                
                # Se conseguiu alguma transcrição
                if transcript:
                    idioma_original = transcript.language_code
                    
                    # Traduz se necessário
                    if idioma_original not in ['pt', 'pt-BR', 'en', 'en-US', 'es']:
                        try:
                            transcript = transcript.translate('pt')
                            idioma_final = 'pt (traduzido)'
                        except:
                            idioma_final = idioma_original
                    else:
                        idioma_final = idioma_original
                    
                    # Baixa e formata
                    legendas_data = transcript.fetch()
                    formatter = TextFormatter()
                    texto_final = formatter.format_transcript(legendas_data)
                    
                    # Valida tamanho
                    if len(texto_final) < TAMANHO_MINIMO:
                        videos_descartados.append({
                            "video_id": video_id,
                            "titulo": titulo,
                            "idioma": idioma_final,
                            "url": video_url,
                            "tamanho": len(texto_final),
                            "status": "descartado",
                            "motivo": f"Vídeo muito curto ({len(texto_final)} chars < {TAMANHO_MINIMO} mínimo)"
                        })
                        print(f"   ⚠️ Legendas DESCARTADAS ({len(texto_final):,} chars < {TAMANHO_MINIMO:,} mínimo): {titulo[:50]}...")
                        continue
                    
                    print(f"   ✅ Legenda {tipo_legenda} ({idioma_final}, {len(texto_final):,} chars): {titulo[:50]}...")
                    
            except Exception as e:
                # Nenhuma legenda disponível
                videos_dados.append({
                    "video_id": video_id,
                    "titulo": titulo,
                    "idioma": idioma_busca,
                    "url": video_url,
                    "texto": None,
                    "tamanho": 0,
                    "status": "falha",
                    "erro": f"Sem legendas e Whisper falhou: {str(e)[:80]}"
                })
                print(f"   ❌ SEM LEGENDAS e Whisper falhou: {titulo[:50]}...")
                continue
        
        # ═══════════════════════════════════════════════════════════
        # SALVA VÍDEO DE QUALIDADE
        # ═══════════════════════════════════════════════════════════
        if texto_final:
            idiomas_usados.add(idioma_final)
            
            videos_dados.append({
                "video_id": video_id,
                "titulo": titulo,
                "idioma": idioma_final,
                "url": video_url,
                "texto": texto_final,
                "tamanho": len(texto_final),
                "status": "sucesso",
                "tipo_legenda": tipo_legenda
            })
            
            # Adiciona ao texto completo
            transcricoes_completas += f"\n{'='*60}\n"
            transcricoes_completas += f"REVIEW: {titulo}\n"
            transcricoes_completas += f"URL: {video_url}\n"
            transcricoes_completas += f"IDIOMA: {idioma_final} ({tipo_legenda})\n"
            transcricoes_completas += f"{'='*60}\n"
            transcricoes_completas += texto_final + "\n"
            
            count_sucesso += 1
            
            # ═══════════════════════════════════════════════════════════
            # 💾 SALVAR TRANSCRIÇÃO IMEDIATAMENTE (para validação incremental)
            # ═══════════════════════════════════════════════════════════
            if pasta_dossie:
                try:
                    # Cria pasta do dossiê se não existir
                    os.makedirs(pasta_dossie, exist_ok=True)
                    
                    # Salva arquivo individual com nomenclatura padronizada
                    nome_arquivo = gerar_nome_arquivo(count_sucesso, titulo, "txt")
                    arquivo_saida = os.path.join(pasta_dossie, nome_arquivo)
                    with open(arquivo_saida, 'w', encoding='utf-8') as f:
                        f.write(f"VÍDEO #{count_sucesso}\n")
                        f.write(f"{'='*70}\n")
                        f.write(f"Título: {titulo}\n")
                        f.write(f"URL: {video_url}\n")
                        f.write(f"Idioma: {idioma_final} ({tipo_legenda})\n")
                        f.write(f"Tamanho: {len(texto_final)} caracteres\n")
                        f.write(f"Data Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                        f.write(f"{'='*70}\n\n")
                        f.write(f" {texto_final}")
                    
                    print(f"   💾 Salvo: {nome_arquivo} ({len(texto_final):,} chars)")
                except Exception as e:
                    print(f"   ⚠️ Erro ao salvar transcrição: {e}")
            
            # OTIMIZAÇÃO: Para de processar após 5 vídeos de qualidade
            if count_sucesso >= 5:
                print(f"   ℹ️ Limite de 5 vídeos de qualidade atingido")
                break
    
    # ═══════════════════════════════════════════════════════════
    # VALIDAÇÃO FINAL
    # ═══════════════════════════════════════════════════════════
    if count_sucesso == 0:
        print(f"   ❌ NENHUMA transcrição de qualidade extraída de {len(videos)} vídeos")
        print(f"   💡 POSSÍVEL BLOQUEIO DO YOUTUBE - Rate limit ou detecção de bot")
        print(f"   ⏸️ SOLUÇÃO: Aguarde 15-30 minutos e tente novamente")
        return "Nenhuma transcrição disponível (vídeos sem legendas ou muito curtos).", [], videos_dados + videos_descartados
    
    # VALIDAÇÃO CRÍTICA: Mínimo de 5 vídeos de qualidade (atualizado)
    if count_sucesso < 5:
        print(f"   ⚠️ ATENÇÃO: Apenas {count_sucesso} vídeo(s) de qualidade encontrado(s) (mínimo: 5)")
        if not WHISPER_DISPONIVEL:
            print(f"   💡 Recomendação: Whisper não está disponível, poderia ajudar")
    
    # Relatório final
    total_falhas = len([v for v in videos_dados if v.get('status') == 'falha'])
    print(f"   📊 Total: {count_sucesso} vídeos de qualidade ✅ + {len(videos_descartados)} descartados ⚠️ + {total_falhas} falharam ❌")
    
    if videos_descartados:
        print(f"   ℹ️ Vídeos descartados por serem muito curtos: {len(videos_descartados)}")
    
    return transcricoes_completas, list(idiomas_usados), videos_dados + videos_descartados
    """Extrai transcrições de forma AGRESSIVA (manual + auto-gerada + traduzida)
    COM FILTRO DE QUALIDADE: Descarta vídeos muito curtos (< 3.000 chars)
    Retorna: (transcricoes_completas_string, idiomas_usados_list, videos_dados_list)
    """
    # PASSO 1: Busca 50 vídeos ordenados por visualizações (mais relevantes primeiro)
    videos_candidatos = buscar_videos_multilingue(nome_ferramenta, max_videos=50)
    
    if not videos_candidatos:
        return "Sem vídeos encontrados no YouTube.", [], []
    
    # PASSO 2: Filtra por duração (>5min) ANTES de processar
    print(f"\n🔍 Filtrando {len(videos_candidatos)} vídeos por duração (mínimo 5 min)...")
    videos_validos = []
    for video_id, titulo, idioma in videos_candidatos:
        duracao, _ = verificar_duracao_video(video_id)
        if duracao >= 300:  # 5 minutos
            videos_validos.append((video_id, titulo, idioma, duracao))
            print(f"   ✅ {titulo[:60]}... ({duracao//60}min{duracao%60}s)")
        else:
            print(f"   ⏭️ {titulo[:60]}... ({duracao}s - muito curto)")
    
    print(f"\n📊 Resultado: {len(videos_validos)} vídeos válidos de {len(videos_candidatos)} candidatos")
    
    # PASSO 3: Se <5 vídeos, perguntar se quer buscar mais
    if len(videos_validos) < 5:
        print(f"\n⚠️ Encontrados apenas {len(videos_validos)} vídeos acima de 5 minutos (mínimo: 5)")
        resposta = input("\n❓ Deseja buscar mais 25 vídeos? (s/n): ").strip().lower()
        
        if resposta == 's':
            print("\n🔄 Buscando mais 25 vídeos...")
            videos_extras = buscar_videos_multilingue(nome_ferramenta, max_videos=25)
            
            print(f"🔍 Filtrando {len(videos_extras)} vídeos extras por duração...")
            for video_id, titulo, idioma in videos_extras:
                if (video_id, titulo, idioma, 0) not in [(v[0], v[1], v[2], 0) for v in videos_validos]:
                    duracao, _ = verificar_duracao_video(video_id)
                    if duracao >= 300:
                        videos_validos.append((video_id, titulo, idioma, duracao))
                        print(f"   ✅ {titulo[:60]}... ({duracao//60}min{duracao%60}s)")
            
            print(f"\n📊 Novo total: {len(videos_validos)} vídeos válidos")
        else:
            print("\n🛑 Processamento cancelado pelo usuário.")
            return "Processamento cancelado: vídeos insuficientes.", [], []
    
    # PASSO 4: Se ainda <5 vídeos, abortar
    if len(videos_validos) < 5:
        print(f"\n❌ Insuficiente: apenas {len(videos_validos)} vídeos >5min encontrados (mínimo: 5)")
        return "Vídeos insuficientes para análise de qualidade.", [], []
    
    # PASSO 5: Já ordenados por relevância, pegar top 5
    videos = videos_validos[:5]
    print(f"\n🎯 Selecionados TOP 5 vídeos mais relevantes (já ordenados por views)")
    for i, (video_id, titulo, idioma, duracao) in enumerate(videos, 1):
        print(f"   {i}. {titulo[:70]}... ({duracao//60}min{duracao%60}s, {idioma})")
    
    print(f"\n📥 Extraindo transcrições dos 5 vídeos selecionados (WHISPER PRIORITÁRIO)...")
    
    # Cria instância da API (necessário para usar .list())
    ytt_api = YouTubeTranscriptApi()
    
    transcricoes_completas = ""
    idiomas_usados = set()
    videos_dados = []
    videos_descartados = []
    count_sucesso = 0
    TAMANHO_MINIMO = 3000  # Caracteres mínimos para considerar vídeo de qualidade
    whisper_falhas_seguidas = 0
    MAX_WHISPER_FALHAS = 3
    
    for idx, (video_id, titulo, idioma_busca, duracao) in enumerate(videos, 1):
        print(f"\n   🎬 Vídeo {idx}/{len(videos)}: {titulo[:70]}... ({duracao//60}min{duracao%60}s)")
        video_url = f"https://youtube.com/watch?v={video_id}"
        
        transcript = None
        tipo_legenda = "desconhecida"
        
        # TENTATIVA 1: WHISPER IA (prioritário, vídeo já foi validado por duração)
        if WHISPER_DISPONIVEL and whisper_falhas_seguidas < MAX_WHISPER_FALHAS:
            print(f"   🎙️ Tentando Whisper IA primeiro...")
            transcript = transcrever_com_whisper(
                video_id, titulo, video_url, 
                pasta_dossie=pasta_dossie, 
                numero_video=idx
            )
            if transcript:
                tipo_legenda = "whisper"
                idiomas_usados.add("multilíngue (IA)")
                whisper_falhas_seguidas = 0  # Reset contador
            else:
                whisper_falhas_seguidas += 1
                if whisper_falhas_seguidas >= MAX_WHISPER_FALHAS:
                    print(f"   ⚠️ Whisper falhou {MAX_WHISPER_FALHAS}x seguidas. Usando apenas legendas YouTube daqui pra frente...")
        elif whisper_falhas_seguidas >= MAX_WHISPER_FALHAS:
            print(f"   ℹ️ Pulando Whisper (muitas falhas). Tentando legendas YouTube...")
        
        # TENTATIVA 2: Buscar legendas oficiais (manual, auto-gerada ou qualquer uma)
        if not transcript:
            print(f"   📜 Whisper falhou/indisponível, tentando legendas oficiais...")
            try:
                transcript_list = ytt_api.list(video_id)
                
                # Tentativa 2A: Legenda MANUAL nos idiomas preferidos
                try:
                    transcript = transcript_list.find_manually_created_transcript(['pt', 'pt-BR', 'en', 'en-US', 'es'])
                    tipo_legenda = "manual"
                except:
                    pass
                
                # Tentativa 2B: Legenda AUTO-GERADA (aceita qualquer idioma)
                if not transcript:
                    try:
                        transcript = transcript_list.find_generated_transcript(['pt', 'pt-BR', 'en', 'en-US', 'es'])
                        tipo_legenda = "auto-gerada"
                    except:
                        pass
                
                # Tentativa 2C: QUALQUER legenda disponível (última tentativa)
                if not transcript:
                    try:
                        # Pega a primeira que aparecer
                        for t in transcript_list:
                            transcript = t
                            tipo_legenda = "disponível"
                            break
                    except:
                        pass
            except Exception as e:
                # Vídeo não tem legendas OU erro ao listar → transcript continua None
                print(f"   ⚠️ Sem legendas oficiais: {str(e)[:50]}...")
                pass
        
        # BRANCH 1: Se conseguiu legenda oficial do YouTube
        if transcript:
            try:
                # Tenta traduzir para PT se não for PT/EN/ES
                idioma_original = transcript.language_code
                
                if idioma_original not in ['pt', 'pt-BR', 'en', 'en-US', 'es']:
                    try:
                        transcript = transcript.translate('pt')
                        idioma_final = 'pt (traduzido)'
                    except:
                        idioma_final = idioma_original
                else:
                    idioma_final = idioma_original
                
                # Baixa e formata
                legendas_data = transcript.fetch()
                formatter = TextFormatter()
                texto = formatter.format_transcript(legendas_data)
                
                idiomas_usados.add(idioma_final)
                
                # VALIDAÇÃO DE QUALIDADE: Descarta se muito curto
                if len(texto) < TAMANHO_MINIMO:
                    videos_descartados.append({
                        "video_id": video_id,
                        "titulo": titulo,
                        "idioma": idioma_final,
                        "url": video_url,
                        "tamanho": len(texto),
                        "status": "descartado",
                        "motivo": f"Vídeo muito curto ({len(texto)} chars < {TAMANHO_MINIMO} mínimo)"
                    })
                    print(f"   ⚠️ DESCARTADO ({len(texto):,} chars < {TAMANHO_MINIMO:,} mínimo): {titulo[:50]}...")
                    continue  # Pula para próximo vídeo
                
                # Salva dados estruturados (apenas vídeos de qualidade)
                videos_dados.append({
                    "video_id": video_id,
                    "titulo": titulo,
                    "idioma": idioma_final,
                    "url": video_url,
                    "texto": texto,
                    "tamanho": len(texto),
                    "status": "sucesso",
                    "tipo_legenda": tipo_legenda
                })
                
                # Adiciona ao texto completo
                transcricoes_completas += f"\n{'='*60}\n"
                transcricoes_completas += f"REVIEW: {titulo}\n"
                transcricoes_completas += f"URL: {video_url}\n"
                transcricoes_completas += f"IDIOMA: {idioma_final} (legenda {tipo_legenda})\n"
                transcricoes_completas += f"{'='*60}\n"
                transcricoes_completas += texto + "\n"
                
                count_sucesso += 1
                print(f"   ✅ Legenda {tipo_legenda} ({idioma_final}, {len(texto):,} chars): {titulo[:50]}...")
                
                # 💾 SALVAR TRANSCRIÇÃO IMEDIATAMENTE (validação incremental)
                if pasta_dossie:
                    try:
                        os.makedirs(pasta_dossie, exist_ok=True)
                        nome_arquivo = gerar_nome_arquivo(count_sucesso, titulo, "txt")
                        arquivo_saida = os.path.join(pasta_dossie, nome_arquivo)
                        with open(arquivo_saida, 'w', encoding='utf-8') as f:
                            f.write(f"VÍDEO #{count_sucesso}\n")
                            f.write(f"{'='*70}\n")
                            f.write(f"Título: {titulo}\n")
                            f.write(f"URL: {video_url}\n")
                            f.write(f"Idioma: {idioma_final} (legenda {tipo_legenda})\n")
                            f.write(f"Tamanho: {len(texto)} caracteres\n")
                            f.write(f"Data Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                            f.write(f"{'='*70}\n\n")
                            f.write(f" {texto}")
                        print(f"   💾 Salvo: {nome_arquivo} ({len(texto):,} chars)")
                    except Exception as e:
                        print(f"   ⚠️ Erro ao salvar: {e}")
                
                # OTIMIZAÇÃO: Para de processar após 5 vídeos de qualidade
                if count_sucesso >= 5:
                    print(f"   ℹ️ Limite de 5 vídeos de qualidade atingido")
                    break
            except Exception as e:
                print(f"   ⚠️ Erro ao processar legenda oficial: {str(e)[:50]}...")
                # Mesmo com legenda encontrada, se houver erro no processamento, continua
                transcript = None
        
        # BRANCH 2: Se NENHUMA tentativa funcionou (nem Whisper, nem legendas)
        if not transcript:
            print(f"   ❌ Falhou TODAS tentativas (Whisper + Legendas): {titulo[:50]}...")
            videos_descartados.append({
                "video_id": video_id,
                "titulo": titulo,
                "idioma": idioma_busca,
                "url": video_url,
                "tamanho": 0,
                "status": "falha",
                "motivo": "Sem Whisper nem legendas disponíveis"
            })
            continue
        
        # ✅ SUCESSO: Contador final
        count_sucesso += 1
        
        if count_sucesso >= 5:
            print(f"   ℹ️ Limite de 5 vídeos de qualidade atingido")
            break
    
    print(f"   📊 Total: {count_sucesso} vídeos de qualidade ✅ + {len(videos_descartados)} descartados/falhados ⚠️")
    
    return transcricoes_completas, list(idiomas_usados), videos_dados + videos_descartados

# ============================================
# SISTEMA DE DOSSIÊ (AUDITORIA)
# ============================================

def salvar_dossie(nome_ferramenta, categoria, dados_site, videos_dados, idiomas):
    """Salva dados brutos coletados para auditoria e reutilização futura
    
    Estrutura criada:
    data/dossies/[ferramenta]/
      ├── metadata.json (resumo: data, URLs, idiomas, stats)
      ├── site_homepage.txt
      ├── site_pricing.txt
      ├── site_features.txt
      ├── site_about.txt
      └── youtube_transcripts.txt (todas concatenadas)
    """
    nome_slug = nome_ferramenta.lower()
    nome_slug = re.sub(r'[^a-z0-9-]', '', nome_slug.replace(' ', '-'))
    
    pasta_dossie = os.path.join(DOSSIES_PATH, nome_slug)
    os.makedirs(pasta_dossie, exist_ok=True)
    
    print(f"\n📂 Salvando dossiê em: {pasta_dossie}")
    
    # 1. Salvar páginas do site (arquivos separados)
    for tipo in ['homepage', 'pricing', 'features', 'about']:
        if dados_site[tipo]['sucesso'] and dados_site[tipo]['texto']:
            caminho = os.path.join(pasta_dossie, f"site_{tipo}.txt")
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"URL: {dados_site[tipo]['url']}\n")
                f.write(f"Data Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Tamanho: {len(dados_site[tipo]['texto'])} caracteres\n")
                f.write(f"{'='*70}\n\n")
                f.write(dados_site[tipo]['texto'])
            print(f"   💾 {tipo}: {len(dados_site[tipo]['texto'])} chars")
    
    # 2. Salvar transcrições do YouTube (CADA VÍDEO EM ARQUIVO SEPARADO + índice)
    videos_com_sucesso = [v for v in videos_dados if v.get('status') == 'sucesso']
    videos_sem_legenda = [v for v in videos_dados if v.get('status') == 'falha']
    
    if videos_dados:
        # 2.1. Índice geral de vídeos
        caminho_indice = os.path.join(pasta_dossie, "youtube_videos_indice.txt")
        with open(caminho_indice, 'w', encoding='utf-8') as f:
            f.write(f"📹 ÍNDICE DE VÍDEOS ANALISADOS\n")
            f.write(f"{'='*70}\n")
            f.write(f"Data Coleta: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write(f"Total de Vídeos Encontrados: {len(videos_dados)}\n")
            f.write(f"Vídeos COM Transcrição: {len(videos_com_sucesso)}\n")
            f.write(f"Vídeos SEM Transcrição: {len(videos_sem_legenda)}\n")
            f.write(f"{'='*70}\n\n")
            
            for i, video in enumerate(videos_dados, 1):
                status_emoji = "✅" if video['status'] == 'sucesso' else "❌"
                f.write(f"{i}. {status_emoji} [{video['idioma']}] {video['titulo']}\n")
                f.write(f"   URL: {video['url']}\n")
                f.write(f"   Status: {video['status']}\n")
                if video['status'] == 'sucesso':
                    f.write(f"   Tamanho: {video['tamanho']} caracteres\n")
                    # Gera nome padronizado para referência
                    nome_arquivo_ref = gerar_nome_arquivo(i, video['titulo'], "txt")
                    f.write(f"   Arquivo: {nome_arquivo_ref}\n")
                else:
                    f.write(f"   Erro: {video.get('erro', 'Sem legendas disponíveis')}\n")
                f.write(f"\n")
        
        print(f"   💾 YouTube Índice: {len(videos_dados)} vídeos catalogados")
        
        # 2.2. Arquivos já foram salvos incrementalmente durante o processamento
        # (Não precisa reescrever aqui - já salvamos com gerar_nome_arquivo)
        
        if videos_com_sucesso:
            total_chars_yt = sum(v['tamanho'] for v in videos_com_sucesso)
            print(f"   💾 YouTube Transcrições: {len(videos_com_sucesso)} arquivos, {total_chars_yt:,} chars total")
    
    # 3. Salvar metadata (JSON para fácil parsing futuro)
    metadata = {
        "ferramenta": nome_ferramenta,
        "categoria": categoria,
        "data_coleta": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "site": {
            "homepage": {
                "url": dados_site['homepage']['url'],
                "coletado": dados_site['homepage']['sucesso'],
                "tamanho": len(dados_site['homepage']['texto']) if dados_site['homepage']['texto'] else 0
            },
            "pricing": {
                "url": dados_site['pricing']['url'],
                "coletado": dados_site['pricing']['sucesso'],
                "tamanho": len(dados_site['pricing']['texto']) if dados_site['pricing']['texto'] else 0
            },
            "features": {
                "url": dados_site['features']['url'],
                "coletado": dados_site['features']['sucesso'],
                "tamanho": len(dados_site['features']['texto']) if dados_site['features']['texto'] else 0
            },
            "about": {
                "url": dados_site['about']['url'],
                "coletado": dados_site['about']['sucesso'],
                "tamanho": len(dados_site['about']['texto']) if dados_site['about']['texto'] else 0
            }
        },
        "youtube": {
            "total_videos_encontrados": len(videos_dados),
            "videos_com_transcricao": len([v for v in videos_dados if v.get('status') == 'sucesso']),
            "videos_sem_transcricao": len([v for v in videos_dados if v.get('status') == 'falha']),
            "idiomas": idiomas,
            "videos": [
                {
                    "titulo": v['titulo'],
                    "url": v['url'],
                    "idioma": v['idioma'],
                    "status": v.get('status', 'desconhecido'),
                    "tamanho": v.get('tamanho', 0),
                    "erro": v.get('erro', None) if v.get('status') == 'falha' else None
                }
                for v in videos_dados
            ]
        },
        "estatisticas": {
            "total_chars_site": sum(
                len(dados_site[t]['texto']) if dados_site[t]['texto'] else 0 
                for t in ['homepage', 'pricing', 'features', 'about']
            ),
            "total_chars_youtube": sum(v.get('tamanho', 0) for v in videos_dados if v.get('status') == 'sucesso'),
            "paginas_coletadas": sum(1 for t in ['homepage', 'pricing', 'features', 'about'] if dados_site[t]['sucesso']),
            "videos_encontrados": len(videos_dados),
            "videos_com_transcricao": len([v for v in videos_dados if v.get('status') == 'sucesso']),
            "videos_sem_transcricao": len([v for v in videos_dados if v.get('status') == 'falha'])
        }
    }
    
    caminho_metadata = os.path.join(pasta_dossie, "metadata.json")
    with open(caminho_metadata, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    videos_msg = f"{len(videos_dados)} vídeos ({len([v for v in videos_dados if v.get('status') == 'sucesso'])} com transcrição)"
    print(f"   💾 Metadata: {metadata['estatisticas']['paginas_coletadas']} páginas + {videos_msg}")
    print(f"   ✅ Dossiê completo salvo!\n")

# ============================================
# CONTROLE DE RATE LIMITING GEMINI
# ============================================

def estimar_tokens(texto):
    """Estimativa grosseira: 1 token ≈ 4 caracteres para PT-BR"""
    return len(texto) // 4

def aguardar_rate_limit():
    """Aguarda o tempo necessário para respeitar RPM (5 requests/min)
    
    Retorna: True se pode prosseguir, False se atingiu limite diário
    """
    global gemini_requests_hoje, gemini_ultima_request, gemini_tokens_ultimo_minuto
    
    # Verifica limite diário
    if gemini_requests_hoje >= GEMINI_RPD:
        print(f"\n❌ LIMITE DIÁRIO ATINGIDO ({GEMINI_RPD} requests)")
        print(f"   ⏸️ Processamento pausado. Continue amanhã!")
        return False
    
    agora = time.time()
    
    # Remove tokens de mais de 1 minuto atrás
    gemini_tokens_ultimo_minuto = [
        (ts, tokens) for ts, tokens in gemini_tokens_ultimo_minuto 
        if agora - ts < 60
    ]
    
    # Calcula delay necessário
    if gemini_ultima_request:
        tempo_desde_ultima = agora - gemini_ultima_request
        if tempo_desde_ultima < GEMINI_DELAY_MIN:
            delay = GEMINI_DELAY_MIN - tempo_desde_ultima
            print(f"   ⏸️ Rate limiting: aguardando {delay:.1f}s...")
            time.sleep(delay)
    
    return True

def registrar_request_gemini(tokens_estimados):
    """Registra uma request ao Gemini para controle de limites"""
    global gemini_requests_hoje, gemini_ultima_request, gemini_tokens_ultimo_minuto
    
    gemini_requests_hoje += 1
    gemini_ultima_request = time.time()
    gemini_tokens_ultimo_minuto.append((time.time(), tokens_estimados))
    
    # Calcula TPM atual
    tokens_ultimo_min = sum(t for _, t in gemini_tokens_ultimo_minuto)
    
    print(f"   📊 Gemini: Request {gemini_requests_hoje}/{GEMINI_RPD} | Tokens/min: {tokens_ultimo_min:,}/{GEMINI_TPM:,}")

# ============================================
# PROCESSAMENTO PRINCIPAL
# ============================================

def processar_ferramenta(nome_ferramenta, categoria, model, modo_dossie=False):
    """Processa uma ferramenta: Site + YouTube + Gemini
    
    Args:
        modo_dossie: Se True, apenas cria dossiê sem enviar ao Gemini
    """
    
    modo_texto = "DOSSIÊ" if modo_dossie else "PROCESSANDO"
    print(f"\n{'='*70}")
    print(f"🚀 {modo_texto}: {nome_ferramenta} ({categoria})")
    print(f"{'='*70}")
    
    # 0. VERIFICAÇÃO: Pula se já foi processado
    nome_arquivo = nome_ferramenta.lower()
    nome_arquivo = re.sub(r'[^a-z0-9-]', '', nome_arquivo.replace(' ', '-'))
    pasta_categoria = os.path.join(BASE_PATH, categoria)
    caminho = os.path.join(pasta_categoria, f"{nome_arquivo}_raw.md")
    
    if os.path.exists(caminho):
        print(f"   ⏭️ JÁ PROCESSADO anteriormente - pulando...")
        print(f"   📄 Arquivo existente: {caminho}")
        return caminho
    
    # 0.1. Prepara pasta do dossiê ANTES de coletar (para Whisper salvar áudios)
    pasta_dossie = os.path.join(DOSSIES_PATH, nome_arquivo)
    os.makedirs(pasta_dossie, exist_ok=True)
    
    # 1. COLETA: Site Oficial
    urls = obter_urls_ferramenta(nome_ferramenta)
    link_oficial = urls['site']
    texto_site, dados_site = coletar_dados_site_oficial(nome_ferramenta)
    
    # 2. COLETA: Reviews Multilíngues (PASSA pasta_dossie para Whisper)
    transcricoes, idiomas, videos_dados = extrair_transcricoes_multilingue(nome_ferramenta, pasta_dossie)
    
    # 2.1. VALIDAÇÃO CRÍTICA: Se nenhum vídeo foi extraído, PULA ferramenta
    videos_com_sucesso = [v for v in videos_dados if v.get('status') == 'sucesso']
    
    if len(videos_com_sucesso) == 0:
        print(f"\n   ⚠️ FALHA CRÍTICA: Nenhum vídeo extraído com sucesso")
        print(f"   💡 Possível bloqueio do YouTube (rate limit/detecção de bot)")
        print(f"   ⏭️ PULANDO {nome_ferramenta} - reprocessar depois")
        print(f"   ℹ️ NÃO salvando dossiê nem _raw.md (permite reprocessamento)\n")
        return None
    
    print(f"\n   ✅ Total de vídeos processados com sucesso: {len(videos_com_sucesso)}")
    
    # 3. SALVAR DOSSIÊ (Auditoria e Reutilização)
    salvar_dossie(nome_ferramenta, categoria, dados_site, videos_dados, idiomas)
    
    # SE MODO DOSSIÊ: Para aqui (não chama Gemini)
    if modo_dossie:
        print(f"\n✅ DOSSIÊ CRIADO: {nome_ferramenta}")
        print(f"   📁 Pasta: dossies/{nome_arquivo}/")
        print(f"   ℹ️ Dados coletados mas NÃO enviados ao Gemini (modo dossiê)")
        return "DOSSIE_OK"  # Retorna string especial para marcar na fila
    
    # 4. CONTROLE DE RATE LIMITING (ANTES de chamar Gemini)
    if not aguardar_rate_limit():
        print(f"   ⚠️ {nome_ferramenta} coletado mas NÃO analisado (limite diário)")
        print(f"   💾 Dossiê salvo - reprocessar amanhã com Gemini")
        return None
    
    # 5. GEMINI: Gera análise
    total_chars = len(texto_site) + len(transcricoes)
    tokens_estimados = estimar_tokens(texto_site + transcricoes + PROMPT_TEMPLATE)
    
    print(f"\n🤖 Gemini processando {total_chars:,} caracteres (~{tokens_estimados:,} tokens)...")
    print(f"   📊 Site: {len(texto_site):,} chars | YouTube: {len(transcricoes):,} chars ({len(videos_com_sucesso)} vídeos)")
    
    # Calcula estatísticas para validação
    paginas_site = sum(1 for t in ['homepage', 'pricing', 'features', 'about'] if dados_site[t]['sucesso'])
    if 'extras' in dados_site and dados_site['extras']:
        paginas_site += len(dados_site['extras'])
    
    urls_videos_str = ""
    if videos_dados:
        urls_list = [f"\n  - {v['url']} ({v['idioma']})" for v in videos_dados[:5]]  # Primeiros 5
        urls_videos_str = "".join(urls_list)
    
    status_transcricoes = "✅ Analisadas e integradas" if videos_dados else "⚠️ Nenhuma transcrição disponível"
    
    prompt = PROMPT_TEMPLATE.format(
        nome_ferramenta=nome_ferramenta,
        categoria=categoria,
        link_oficial=link_oficial,
        texto_site=texto_site,
        transcricoes=transcricoes,
        data_hoje=datetime.now().strftime('%d/%m/%Y'),
        idiomas=", ".join(idiomas) if idiomas else "PT-BR (conhecimento interno)",
        paginas_coletadas=f"{paginas_site} páginas",
        total_videos=len(videos_dados),
        urls_videos=urls_videos_str,
        status_transcricoes=status_transcricoes,
        total_caracteres=f"{total_chars:,} caracteres",
        slug_ferramenta=nome_arquivo
    )
    
    try:
        # Registra request ANTES de chamar (para controle preciso)
        registrar_request_gemini(tokens_estimados)
        
        response = model.generate_content(prompt)
        conteudo = response.text
        print(f"   ✅ Análise gerada! ({len(conteudo)} caracteres)")
        
    except Exception as e:
        print(f"   ❌ Erro no Gemini: {e}")
        # Decrementa contador se falhou (não contabiliza como request bem-sucedida)
        global gemini_requests_hoje
        gemini_requests_hoje -= 1
        return None
    
    # 5. SALVAR ANÁLISE FINAL (Markdown puro - formatação manual depois)
    # Nome do arquivo já calculado no início da função
    conteudo_final = f"""---
ANÁLISE GERADA AUTOMATICAMENTE - REQUER FORMATAÇÃO
Ferramenta: {nome_ferramenta}
Categoria: {categoria}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Site: {link_oficial}
Idiomas Fonte: {', '.join(idiomas) if idiomas else 'PT-BR'}
---

{conteudo}
"""
    
    os.makedirs(pasta_categoria, exist_ok=True)
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo_final)
    
    print(f"   💾 Salvo em: {caminho}")
    return caminho

# ============================================
# MAIN
# ============================================

def ler_fila():
    """Lê fila de processamento e retorna lista de (nome, categoria)
    
    Formato esperado no arquivo:
    Nome da Ferramenta | Categoria
    
    Ignora linhas vazias e comentários (#)
    """
    arquivo_fila = os.path.join(os.path.dirname(BASE_PATH), "fila_processamento.txt")
    
    if not os.path.exists(arquivo_fila):
        print(f"\n❌ Arquivo de fila não encontrado: {arquivo_fila}")
        print("💡 Crie o arquivo com o formato: 'Nome da Ferramenta | Categoria'")
        return []
    
    ferramentas_fila = []
    
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            
            # Ignora comentários e linhas vazias
            if not linha or linha.startswith('#'):
                continue
            
            # Parse: "Nome | Categoria"
            if '|' in linha:
                partes = linha.split('|')
                nome = partes[0].strip()
                categoria = partes[1].strip()
                ferramentas_fila.append((nome, categoria))
            else:
                # Formato antigo (só nome, sem categoria) - tenta inferir
                nome = linha
                # Busca categoria no dicionário hardcoded (fallback)
                categoria = None
                for cat, tools in FERRAMENTAS_POR_CATEGORIA.items():
                    if nome in tools:
                        categoria = cat
                        break
                
                if categoria:
                    ferramentas_fila.append((nome, categoria))
                else:
                    print(f"   ⚠️ Ferramenta '{nome}' sem categoria definida - pulando")
    
    return ferramentas_fila


def marcar_dossie_na_fila(ferramentas_com_dossie):
    """Marca ferramentas com dossiê na fila (ADICIONA tag [DOSSIÊ OK])
    
    Args:
        ferramentas_com_dossie: Lista de nomes de ferramentas que tiveram dossiê gerado
    """
    if not ferramentas_com_dossie:
        return
    
    arquivo_fila = os.path.join(os.path.dirname(BASE_PATH), "fila_processamento.txt")
    
    if not os.path.exists(arquivo_fila):
        return
    
    # Lê todas as linhas
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    linhas_atualizadas = []
    marcadas = 0
    
    for linha in linhas:
        linha_original = linha
        linha_limpa = linha.strip()
        
        # Ignora linhas vazias e comentários
        if not linha_limpa or linha_limpa.startswith('#'):
            linhas_atualizadas.append(linha_original)
            continue
        
        # Verifica se é uma das ferramentas com dossiê
        nome_na_linha = linha_limpa.split('|')[0].strip()
        
        if nome_na_linha in ferramentas_com_dossie:
            # Verifica se já tem a tag
            if '[DOSSIÊ OK]' not in linha_limpa:
                # Adiciona tag no final (mantém \n original)
                linha_atualizada = linha_original.rstrip('\n') + ' [DOSSIÊ OK]\n'
                linhas_atualizadas.append(linha_atualizada)
                marcadas += 1
            else:
                # Já marcada, mantém como está
                linhas_atualizadas.append(linha_original)
        else:
            # Não é ferramenta processada, mantém como está
            linhas_atualizadas.append(linha_original)
    
    # Reescreve arquivo
    with open(arquivo_fila, 'w', encoding='utf-8') as f:
        f.writelines(linhas_atualizadas)
    
    print(f"\n📋 Fila atualizada:")
    print(f"   ✅ {marcadas} ferramenta(s) MARCADA(S) com [DOSSIÊ OK]")


def remover_da_fila(ferramentas_processadas):
    """Remove ferramentas processadas da fila (DELETA as linhas)
    
    Args:
        ferramentas_processadas: Lista de nomes de ferramentas que foram processadas
    """
    if not ferramentas_processadas:
        return
    
    arquivo_fila = os.path.join(os.path.dirname(BASE_PATH), "fila_processamento.txt")
    
    if not os.path.exists(arquivo_fila):
        return
    
    # Lê arquivo
    with open(arquivo_fila, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Filtra linhas (remove as processadas)
    ferramentas_lower = [f.lower() for f in ferramentas_processadas]
    linhas_filtradas = []
    
    for linha in linhas:
        linha_stripped = linha.strip()
        
        # Mantém comentários e linhas vazias
        if not linha_stripped or linha_stripped.startswith('#'):
            linhas_filtradas.append(linha)
            continue
        
        # Extrai nome da ferramenta (antes do |)
        if '|' in linha_stripped:
            nome_ferramenta = linha_stripped.split('|')[0].strip()
        else:
            nome_ferramenta = linha_stripped
        
        # Remove se foi processada
        if nome_ferramenta.lower() not in ferramentas_lower:
            linhas_filtradas.append(linha)
        # Senão, deleta a linha (não adiciona em linhas_filtradas)
    
    # Reescreve arquivo
    with open(arquivo_fila, 'w', encoding='utf-8') as f:
        f.writelines(linhas_filtradas)
    
    print(f"\n🧹 Fila atualizada:")
    print(f"   ✅ {len(ferramentas_processadas)} ferramenta(s) REMOVIDA(S) da fila")


def main():
    import sys
    
    print("\n" + "="*70)
    print("  🚀 GEODE SUPER CRAWLER V2.6 - BUSCA INTELIGENTE")
    print("="*70)
    print(f"  📊 Limites API Gemini: {GEMINI_RPD} req/dia | {GEMINI_RPM} req/min | {GEMINI_TPM:,} tok/min")
    print(f"  ⏱️ Delay entre requests: {GEMINI_DELAY_MIN}s")
    print(f"  ✅ Whisper IA: {'ATIVO' if WHISPER_DISPONIVEL else 'INATIVO'}")
    print("="*70 + "\n")
    
    # Configura Gemini
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODELO_GEMINI)
    
    # Lê fila de processamento
    fila = ler_fila()
    
    if not fila:
        print("❌ Fila de processamento vazia ou arquivo não encontrado!")
        print(f"📝 Edite: {os.path.join(os.path.dirname(BASE_PATH), 'fila_processamento.txt')}")
        return
    
    print(f"📋 Fila carregada: {len(fila)} ferramenta(s) pendente(s)\n")
    
    # ═══════════════════════════════════════════════════════════
    # MENU SIMPLIFICADO (TODAS AS OPÇÕES USAM A FILA)
    # ═══════════════════════════════════════════════════════════
    
    print("📋 ESCOLHA UMA OPÇÃO:\n")
    print("1️⃣  Processar 5 FERRAMENTAS da fila (batch rápido - ~15 min)")
    print("2️⃣  Processar 1 FERRAMENTA da fila (primeira)")
    print("3️⃣  Processar ferramenta ESPECÍFICA da fila (buscar por nome)")
    print("4️⃣  Ver FILA completa (ferramentas pendentes)")
    print("5️⃣  Sair")
    print("6️⃣  MODO DOSSIÊ: Criar dossiês SEM enviar ao Gemini (não remove da fila)")
    print("7️⃣  Processar 20 FERRAMENTAS da fila (batch COMPLETO - ~1h)\n")
    
    escolha = input("👉 Sua opção (1-7): ").strip()
    
    if escolha == "5":
        print("\n👋 Até logo!\n")
        return
    
    # ═══════════════════════════════════════════════════════════
    # OPÇÃO 1: Processar 5 ferramentas DA FILA em batch
    # ═══════════════════════════════════════════════════════════
    if escolha == "1":
        print("\n" + "="*70)
        print("🚀 MODO BATCH: Processando 5 ferramentas da fila")
        print("="*70)
        
        # Pega as 5 primeiras da fila (ou menos se não houver 5)
        ferramentas_processar = fila[:5]
        
        print(f"\n📊 Fila total: {len(fila)} ferramenta(s)")
        print(f"🎯 Processando as {len(ferramentas_processar)} primeiras:\n")
        
        for i, (ferramenta, categoria) in enumerate(ferramentas_processar, 1):
            print(f"   {i}. {ferramenta} ({categoria})")
        
        print(f"\n⏱️ Tempo estimado: ~{len(ferramentas_processar) * 3} minutos")
        print(f"📊 Requests Gemini: {len(ferramentas_processar)}/{GEMINI_RPD}")
        
        confirma = input("\n✅ Confirma processamento? (s/n): ").strip().lower()
        if confirma != 's':
            print("\n❌ Cancelado")
            return
        
        # Pergunta sobre desligamento ANTES de iniciar
        desligar_ao_final = input("\n🔌 Desligar PC automaticamente quando terminar? (s/n): ").strip().lower() == 's'
        if desligar_ao_final:
            print("✅ PC desligará automaticamente após conclusão")
        
        # Processa
        sucesso = 0
        falhas = 0
        processadas = []
        
        for i, (ferramenta, categoria) in enumerate(ferramentas_processar, 1):
            print(f"\n{'='*70}")
            print(f"📦 Batch: {i}/{len(ferramentas_processar)}")
            print(f"{'='*70}")
            
            try:
                resultado = processar_ferramenta(ferramenta, categoria, model)
                if resultado:
                    sucesso += 1
                    processadas.append(ferramenta)
                else:
                    falhas += 1
            except Exception as e:
                print(f"\n❌ ERRO: {e}")
                falhas += 1
        
        # Remove da fila
        remover_da_fila(processadas)
        
        # Relatório
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DO BATCH")
        print("="*70)
        print(f"✅ Sucesso: {sucesso}")
        print(f"❌ Falhas: {falhas}")
        print(f"📈 Taxa: {(sucesso/len(ferramentas_processar)*100):.1f}%")
        print(f"🔥 Requests: {gemini_requests_hoje}/{GEMINI_RPD}")
        print(f"📋 Restam na fila: {len(fila) - len(processadas)} ferramenta(s)")
        print("="*70 + "\n")
        
        # Desliga PC se confirmado no início
        if desligar_ao_final:
            print("\n" + "="*70)
            print("⚡ DESLIGAMENTO AUTOMÁTICO PROGRAMADO")
            print("="*70)
            print("\n⏳ Desligando o computador em 10 segundos...")
            print("💡 Pressione Ctrl+C para CANCELAR\n")
            try:
                time.sleep(10)
                import subprocess
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            except KeyboardInterrupt:
                print("\n❌ Desligamento cancelado pelo usuário")
            except Exception as e:
                print(f"\n⚠️ Erro ao desligar: {e}")
                print("💡 Execute manualmente: shutdown /s /f /t 0")
    
    # ═══════════════════════════════════════════════════════════
    # OPÇÃO 2: Processar 1 ferramenta DA FILA (primeira)
    # ═══════════════════════════════════════════════════════════
    elif escolha == "6":
        print("\n" + "="*70)
        print("📂 MODO DOSSIÊ: Criar dossiês SEM enviar ao Gemini")
        print("="*70)
        print("\n⚠️ Este modo coleta dados (site + YouTube) mas NÃO gera artigo.")
        print("💡 Útil para preparar material ou evitar uso da API Gemini.")
        print("📝 Ferramentas continuam na fila, mas marcadas com [DOSSIÊ OK]\n")
        
        print("📋 SUBMODO:\n")
        print("1️⃣  Criar dossiês para TODAS da fila")
        print("2️⃣  Criar dossiê para 1 ferramenta (primeira)")
        print("3️⃣  Criar dossiê para ferramenta ESPECÍFICA")
        print("4️⃣  Voltar\n")
        
        submodo = input("👉 Sua opção (1-4): ").strip()
        
        if submodo == "4":
            print("\n🔙 Voltando ao menu principal...\n")
            return main()
        
        # SUBMODO 1: Todas da fila
        if submodo == "1":
            print(f"\n📊 Total de {len(fila)} ferramenta(s) na fila")
            print(f"⏱️ Tempo estimado: ~{len(fila) * 2} minutos (sem Gemini)\n")
            
            confirma = input("✅ Criar dossiês para TODAS? (s/n): ").strip().lower()
            if confirma != 's':
                print("\n❌ Cancelado")
                return
            
            # Pergunta sobre desligamento ANTES (só se 10+)
            desligar_ao_final = False
            if len(fila) >= 10:
                desligar_ao_final = input("\n🔌 Desligar PC automaticamente quando terminar? (s/n): ").strip().lower() == 's'
                if desligar_ao_final:
                    print(f"✅ PC desligará automaticamente após criar {len(fila)} dossiês")
            
            sucesso = 0
            falhas = 0
            processadas = []
            
            for i, (ferramenta, categoria) in enumerate(fila, 1):
                print(f"\n{'='*70}")
                print(f"📦 Dossiê {i}/{len(fila)}: {ferramenta}")
                print(f"{'='*70}")
                
                try:
                    resultado = processar_ferramenta(ferramenta, categoria, model, modo_dossie=True)
                    if resultado:
                        sucesso += 1
                        processadas.append(ferramenta)
                    else:
                        falhas += 1
                except Exception as e:
                    print(f"\n❌ ERRO: {e}")
                    falhas += 1
            
            # Marca na fila (NÃO remove)
            marcar_dossie_na_fila(processadas)
            
            print("\n" + "="*70)
            print("📊 RELATÓRIO - MODO DOSSIÊ")
            print("="*70)
            print(f"✅ Dossiês criados: {sucesso}")
            print(f"❌ Falhas: {falhas}")
            print(f"📝 Ferramentas marcadas na fila: {len(processadas)}")
            print(f"💡 Para gerar artigos, use opções 1-3 do menu principal")
            print("="*70 + "\n")
            
            # Desliga PC se confirmado no início
            if desligar_ao_final:
                print("\n" + "="*70)
                print("⚡ DESLIGAMENTO AUTOMÁTICO PROGRAMADO")
                print("="*70)
                print("\n⏳ Desligando o computador em 10 segundos...")
                print("💡 Pressione Ctrl+C para CANCELAR\n")
                try:
                    time.sleep(10)
                    import subprocess
                    subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
                except KeyboardInterrupt:
                    print("\n❌ Desligamento cancelado pelo usuário")
                except Exception as e:
                    print(f"\n⚠️ Erro ao desligar: {e}")
                    print("💡 Execute manualmente: shutdown /s /f /t 0")
        
        # SUBMODO 2: Primeira da fila
        elif submodo == "2":
            if not fila:
                print("\n🎉 Fila vazia!")
                return
            
            ferramenta, categoria = fila[0]
            print(f"\n🎯 Criar dossiê: {ferramenta} ({categoria})")
            
            confirma = input("\n✅ Confirma? (s/n): ").strip().lower()
            if confirma != 's':
                print("\n❌ Cancelado")
                return
            
            resultado = processar_ferramenta(ferramenta, categoria, model, modo_dossie=True)
            
            if resultado:
                marcar_dossie_na_fila([ferramenta])
                print(f"\n✅ Dossiê de {ferramenta} criado e marcado na fila!")
            else:
                print(f"\n❌ Falha ao criar dossiê de {ferramenta}")
        
        # SUBMODO 3: Específica
        elif submodo == "3":
            print(f"\n📋 Ferramentas disponíveis na fila:\n")
            for i, (f, c) in enumerate(fila, 1):
                print(f"   {i}. {f} ({c})")
            
            busca = input("\n🔍 Digite o nome (ou parte): ").strip().lower()
            
            encontradas = [(f, c) for f, c in fila if busca in f.lower()]
            
            if not encontradas:
                print(f"\n❌ Nenhuma ferramenta encontrada com '{busca}'")
                return
            
            if len(encontradas) > 1:
                print(f"\n📋 Encontradas {len(encontradas)} ferramentas:\n")
                for i, (f, c) in enumerate(encontradas, 1):
                    print(f"   {i}. {f} ({c})")
                
                idx = input("\n👉 Escolha o número: ").strip()
                try:
                    ferramenta, categoria = encontradas[int(idx) - 1]
                except:
                    print("\n❌ Opção inválida")
                    return
            else:
                ferramenta, categoria = encontradas[0]
            
            print(f"\n🎯 Criar dossiê: {ferramenta} ({categoria})")
            
            confirma = input("\n✅ Confirma? (s/n): ").strip().lower()
            if confirma != 's':
                print("\n❌ Cancelado")
                return
            
            resultado = processar_ferramenta(ferramenta, categoria, model, modo_dossie=True)
            
            if resultado:
                marcar_dossie_na_fila([ferramenta])
                print(f"\n✅ Dossiê de {ferramenta} criado e marcado na fila!")
            else:
                print(f"\n❌ Falha ao criar dossiê de {ferramenta}")
        else:
            print("\n❌ Opção inválida")
    
    elif escolha == "2":
        if not fila:
            print("\n🎉 Fila vazia - todas processadas!")
            return
        
        ferramenta, categoria = fila[0]
        print(f"\n🎯 Processando primeira da fila: {ferramenta} ({categoria})")
        print(f"📋 Ainda restam: {len(fila) - 1} ferramenta(s) após esta")
        
        confirma = input("\n✅ Confirma? (s/n): ").strip().lower()
        if confirma != 's':
            print("\n❌ Cancelado")
            return
        
        resultado = processar_ferramenta(ferramenta, categoria, model)
        
        if resultado:
            remover_da_fila([ferramenta])
            print(f"\n✅ {ferramenta} processada e removida da fila!")
        else:
            print(f"\n❌ Falha ao processar {ferramenta}")
    
    # ═══════════════════════════════════════════════════════════
    # OPÇÃO 3: Processar ferramenta ESPECÍFICA DA FILA
    # ═══════════════════════════════════════════════════════════
    elif escolha == "3":
        print("\n✏️ Digite o nome da ferramenta (deve estar na fila)")
        print(f"💡 Ferramentas disponíveis na fila: {len(fila)}\n")
        
        # Mostra preview das primeiras 10
        print("📋 Primeiras 10 da fila:")
        for i, (nome, cat) in enumerate(fila[:10], 1):
            print(f"   {i}. {nome} ({cat})")
        
        if len(fila) > 10:
            print(f"   ... e mais {len(fila) - 10} ferramenta(s)")
        
        nome_input = input("\n👉 Nome da ferramenta: ").strip()
        
        if not nome_input:
            print("\n❌ Nome vazio")
            return
        
        # Busca na fila (case-insensitive)
        ferramenta_encontrada = None
        categoria_encontrada = None
        
        for nome, cat in fila:
            if nome.lower() == nome_input.lower():
                ferramenta_encontrada = nome
                categoria_encontrada = cat
                break
        
        if not ferramenta_encontrada:
            print(f"\n❌ '{nome_input}' não encontrada na fila")
            print("💡 Use opção 4 para ver a fila completa")
            return
        
        print(f"\n✅ Encontrado na fila: {ferramenta_encontrada} ({categoria_encontrada})")
        
        confirma = input("\n✅ Processar agora? (s/n): ").strip().lower()
        if confirma != 's':
            print("\n❌ Cancelado")
            return
        
        resultado = processar_ferramenta(ferramenta_encontrada, categoria_encontrada, model)
        
        if resultado:
            remover_da_fila([ferramenta_encontrada])
            print(f"\n✅ {ferramenta_encontrada} processada e removida da fila!")
        else:
            print(f"\n❌ Falha ao processar {ferramenta_encontrada}")
    
    # ═══════════════════════════════════════════════════════════
    # OPÇÃO 4: Ver FILA completa
    # ═══════════════════════════════════════════════════════════
    elif escolha == "4":
        print("\n" + "="*70)
        print("📋 FILA DE PROCESSAMENTO COMPLETA")
        print("="*70 + "\n")
        
        if not fila:
            print("🎉 Fila vazia - todas as ferramentas foram processadas!\n")
            return
        
        # Agrupa por categoria
        por_categoria = {}
        for nome, cat in fila:
            if cat not in por_categoria:
                por_categoria[cat] = []
            por_categoria[cat].append(nome)
        
        total = 0
        for cat in sorted(por_categoria.keys()):
            ferramentas = por_categoria[cat]
            print(f"\n📂 {cat.upper()} ({len(ferramentas)} ferramenta(s))")
            print("-" * 50)
            
            for ferramenta in ferramentas:
                total += 1
                print(f"   {total:2d}. {ferramenta}")
        
        print("\n" + "="*70)
        print(f"📊 Total na fila: {total} ferramenta(s)")
        print(f"⏱️ Tempo estimado (5 por batch): ~{(total // 5 + 1) * 15} minutos")
        print("="*70 + "\n")
    
    # ═══════════════════════════════════════════════════════════
    # OPÇÃO 7: Processar 20 ferramentas DA FILA (batch COMPLETO)
    # ═══════════════════════════════════════════════════════════
    elif escolha == "7":
        print("\n" + "="*70)
        print("🚀 MODO BATCH COMPLETO: Processando 20 ferramentas da fila")
        print("="*70)
        print("\n⚠️ ATENÇÃO: Este processo pode levar ~1 hora!")
        print(f"⚠️ Limite diário Gemini: {GEMINI_RPD} requests/dia")
        
        if gemini_requests_hoje >= GEMINI_RPD:
            print(f"\n❌ LIMITE DIÁRIO ATINGIDO ({gemini_requests_hoje}/{GEMINI_RPD})")
            print("💡 Tente novamente amanhã ou use MODO DOSSIÊ (opção 6)")
            return
        
        # Pega as 20 primeiras da fila (ou menos se não houver 20)
        ferramentas_processar = fila[:20]
        
        print(f"\n📊 Fila total: {len(fila)} ferramenta(s)")
        print(f"🎯 Processando as {len(ferramentas_processar)} primeiras:\n")
        
        for i, (ferramenta, categoria) in enumerate(ferramentas_processar, 1):
            print(f"   {i:2d}. {ferramenta} ({categoria})")
        
        print(f"\n⏱️ Tempo estimado: ~{len(ferramentas_processar) * 3} minutos")
        print(f"📊 Requests Gemini: {len(ferramentas_processar)}/{GEMINI_RPD}")
        
        # Verifica se vai estourar o limite
        if gemini_requests_hoje + len(ferramentas_processar) > GEMINI_RPD:
            print(f"\n⚠️ ATENÇÃO: Processamento pode estourar limite diário!")
            print(f"   Requests hoje: {gemini_requests_hoje}")
            print(f"   Processando: {len(ferramentas_processar)}")
            print(f"   Total: {gemini_requests_hoje + len(ferramentas_processar)}/{GEMINI_RPD}")
            print(f"\n💡 Algumas ferramentas podem falhar por limite de API")
        
        confirma = input("\n✅ Confirma processamento? (s/n): ").strip().lower()
        if confirma != 's':
            print("\n❌ Cancelado")
            return
        
        # Pergunta sobre desligamento ANTES de iniciar
        desligar_ao_final = input("\n🔌 Desligar PC automaticamente quando terminar? (s/n): ").strip().lower() == 's'
        if desligar_ao_final:
            print("✅ PC desligará automaticamente após conclusão (~1 hora)")
        
        # Processa
        sucesso = 0
        falhas = 0
        processadas = []
        
        print("\n🔥 INICIANDO PROCESSAMENTO EM LOTE...\n")
        
        for i, (ferramenta, categoria) in enumerate(ferramentas_processar, 1):
            print(f"\n{'='*70}")
            print(f"📦 Batch: {i}/{len(ferramentas_processar)} | Progresso: {(i/len(ferramentas_processar)*100):.1f}%")
            print(f"✅ Sucesso até agora: {sucesso} | ❌ Falhas: {falhas}")
            print(f"{'='*70}")
            
            try:
                resultado = processar_ferramenta(ferramenta, categoria, model)
                if resultado:
                    sucesso += 1
                    processadas.append(ferramenta)
                else:
                    falhas += 1
            except Exception as e:
                print(f"\n❌ ERRO: {e}")
                falhas += 1
            
            # Atualiza contador de requests
            if i % 5 == 0 and i < len(ferramentas_processar):
                print(f"\n⏸️ Checkpoint: {i} de {len(ferramentas_processar)} processadas")
                print(f"⏱️ Tempo restante estimado: ~{(len(ferramentas_processar) - i) * 3} minutos")
        
        # Remove da fila
        remover_da_fila(processadas)
        
        # Relatório Final
        print("\n" + "="*70)
        print("🏁 RELATÓRIO FINAL - BATCH COMPLETO (20 FERRAMENTAS)")
        print("="*70)
        print(f"✅ Sucesso: {sucesso}")
        print(f"❌ Falhas: {falhas}")
        print(f"📊 Total processado: {len(ferramentas_processar)}")
        print(f"📈 Taxa de sucesso: {(sucesso/len(ferramentas_processar)*100):.1f}%")
        print(f"🔥 Requests Gemini hoje: {gemini_requests_hoje}/{GEMINI_RPD}")
        print(f"📋 Restam na fila: {len(fila) - len(processadas)} ferramenta(s)")
        print(f"⏱️ Tempo total decorrido: ~{len(ferramentas_processar) * 3} minutos")
        print("="*70 + "\n")
        
        # Desliga PC se confirmado no início
        if desligar_ao_final:
            print("\n" + "="*70)
            print("⚡ DESLIGAMENTO AUTOMÁTICO PROGRAMADO")
            print("="*70)
            print("\n⏳ Desligando o computador em 10 segundos...")
            print("💡 Pressione Ctrl+C para CANCELAR\n")
            try:
                time.sleep(10)
                import subprocess
                subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            except KeyboardInterrupt:
                print("\n❌ Desligamento cancelado pelo usuário")
            except Exception as e:
                print(f"\n⚠️ Erro ao desligar: {e}")
                print("💡 Execute manualmente: shutdown /s /f /t 0")
    
    else:
        print("\n❌ Opção inválida\n")

if __name__ == "__main__":
    main()
