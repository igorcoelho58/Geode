# Arquitetura de Topic Clusters - Projeto Geode (SEO Sênior)

Este documento define a estrutura de conteúdo do site, organizada em **Topic Clusters** para maximizar a autoridade semântica no Google e a conversão de afiliados.

**Objetivo:** Dominar a intenção de busca "Comercial" e "Transacional" para ferramentas de IA focadas em PMEs no Brasil.

---

## 1. As 4 Categorias Pilares (Pastas Raiz)

Baseado nas dores das personas (Empreendedor "Polvo" e Gestor "Sobrecarregado"), definimos os seguintes pilares:

1.  **Atendimento & Chatbots** (Dor: "Escravidão do WhatsApp / Suporte 24h")
2.  **Vendas & CRM** (Dor: "Perder leads / Falta de Follow-up")
3.  **Marketing & Conteúdo** (Dor: "Criatividade bloqueada / Custo de Agência")
4.  **Gestão & Produtividade** (Dor: "Caos operacional / Falta de tempo")

---

## 2. Estrutura de Conteúdo Satélite

### 🤖 Pilar 1: Atendimento & Chatbots (`/atendimento`)
*Foco: Automação de WhatsApp, Instagram Direct e Suporte.*

| Tipo | Título Sugerido (H1) | Palavra-chave Foco | Intenção |
| :--- | :--- | :--- | :--- |
| **Review** | Typebot é bom? Análise completa e preços 2025 | `typebot review` | Comercial |
| **Comparativo** | ManyChat vs Typebot: Qual o melhor para PMEs? | `manychat ou typebot` | Comercial |
| **Lista** | 7 Melhores Chatbots para WhatsApp (Grátis e Pagos) | `melhores chatbots whatsapp` | Investigação |
| **Caso de Uso** | Como automatizar agendamentos de Clínica com IA | `agendamento automatico whatsapp` | Informacional/Transacional |
| **Tutorial** | Como criar um atendente de IA no WhatsApp sem programar | `criar chatbot whatsapp ia` | Informacional |
| **Técnico** | Z-API vale a pena? Tudo sobre a API de WhatsApp | `z-api review` | Comercial |

### 💰 Pilar 2: Vendas & CRM (`/vendas`)
*Foco: Gestão de Leads, Prospecção e Fechamento.*

| Tipo | Título Sugerido (H1) | Palavra-chave Foco | Intenção |
| :--- | :--- | :--- | :--- |
| **Lista** | 5 Melhores CRMs com IA para Pequenas Empresas | `crm com ia para pme` | Investigação |
| **Comparativo** | Kommo (AmoCRM) vs RD Station: Qual escolher? | `kommo vs rd station` | Comercial |
| **Review** | Apollo.io funciona no Brasil? Preço e Funcionalidades | `apollo.io review brasil` | Comercial |
| **Caso de Uso** | Como recuperar carrinhos abandonados usando IA | `recuperação carrinho ia` | Transacional |
| **Guia** | Funil de Vendas Automático: O Guia Definitivo | `funil de vendas automatico` | Informacional (Pilar) |
| **Review** | Instantly.ai: A melhor ferramenta de Cold Email? | `instantly review` | Comercial |

### 🎨 Pilar 3: Marketing & Conteúdo (`/marketing`)
*Foco: Criação de Copy, Imagens e Vídeos.*

| Tipo | Título Sugerido (H1) | Palavra-chave Foco | Intenção |
| :--- | :--- | :--- | :--- |
| **Comparativo** | Jasper AI vs ChatGPT Plus: Qual escreve melhor? | `jasper vs chatgpt` | Comercial |
| **Lista** | Top 10 Ferramentas de IA para Criar Posts de Instagram | `ia para instagram` | Investigação |
| **Review** | HeyGen: Crie vídeos com avatares realistas (Teste) | `heygen review` | Comercial |
| **Caso de Uso** | Como fazer SEO Local para sua loja usando IA | `seo local com ia` | Informacional |
| **Lista** | Melhores Geradores de Imagem IA para E-commerce | `ia gerador imagem produtos` | Investigação |

### ⚡ Pilar 4: Gestão & Produtividade (`/produtividade`)
*Foco: Organização, Reuniões e Financeiro.*

| Tipo | Título Sugerido (H1) | Palavra-chave Foco | Intenção |
| :--- | :--- | :--- | :--- |
| **Comparativo** | Notion AI vs ClickUp Brain: Batalha de Gestão | `notion ai vs clickup` | Comercial |
| **Review** | Fireflies.ai: Transcreva reuniões em Português | `fireflies ai funciona portugues` | Comercial |
| **Lista** | 5 Ferramentas para Automatizar Notas Fiscais | `automatizar notas fiscais` | Investigação |
| **Caso de Uso** | Como usar o ChatGPT para escrever e-mails difíceis | `chatgpt para emails` | Informacional |
| **Review** | Gamma App: Crie apresentações em segundos | `gamma app review` | Comercial |

---

## 3. Projeção da Estrutura de Pastas (Hugo)

A estrutura física dos arquivos no Hugo deve refletir exatamente a hierarquia semântica.

```text
content/
├── atendimento/
│   ├── _index.md                   <-- Página Pilar (Hub de Conteúdo)
│   ├── manychat-vs-typebot.md      <-- Artigo Satélite
│   ├── melhores-chatbots-2025.md
│   └── typebot-review.md
├── vendas/
│   ├── _index.md
│   ├── kommo-vs-rd-station.md
│   └── melhores-crms-ia.md
├── marketing/
│   ├── _index.md
│   └── jasper-vs-chatgpt.md
└── produtividade/
    ├── _index.md
    └── notion-ai-review.md
```

---

## 4. Estratégia de Linkagem Interna (The Spiderweb)

Para fortalecer a autoridade do domínio, usaremos a seguinte regra de ouro:

1.  **Satélite -> Pilar:** Todo artigo satélite (ex: "ManyChat vs Typebot") deve ter no primeiro parágrafo um link para a Página Pilar da categoria (ex: "Veja nosso guia completo de **Automação de Atendimento**").
    *   *Objetivo:* Jogar autoridade para a página principal que rankeia para termos head-tail.

2.  **Pilar -> Satélite:** A Página Pilar (`_index.md`) deve funcionar como um índice curado, listando e linkando para todos os artigos satélites com âncoras ricas.

3.  **Satélite <-> Satélite:** Artigos do mesmo cluster devem se linkar.
    *   Ex: O review do "Typebot" deve linkar para o tutorial "Como criar chatbot no WhatsApp".
    *   *Objetivo:* Aumentar o tempo de permanência e páginas por sessão.

4.  **Links de Afiliado:** Devem estar presentes principalmente nos artigos de **Review** e **Comparativo**, preferencialmente em botões de CTA ("Testar Grátis", "Ver Preço") e no primeiro terço do texto.
