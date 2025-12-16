# Checklist do Projeto Geode (Versão Detalhada)

## 🟢 Fase 1: Estratégia (Concluída)
- [x] **Escolha do Nicho:** Automação de IA para PMEs (Oceano Azul).
- [x] **Definição de Personas:** Empreendedor "Polvo", Gestor "Sobrecarregado", CLT "Aspirante".
- [x] **Topic Clusters:** Definição dos 4 pilares (Atendimento, Vendas, Marketing, Produtividade).

## 🟢 Fase 2: Estrutura Técnica (Concluída)
- [x] **Setup Inicial:** Instalação do Hugo e Tema PaperMod.
- [x] **Configuração:** Ajuste do `hugo.toml` e menus.
- [x] **Estrutura de Pastas:** Criação dos diretórios de conteúdo baseados nos clusters.
- [x] **Design System V1:** Criação do Shortcode `product_card` para conversão.
- [x] **Sistema de Links:** Criar `data/links.yaml` para centralizar links de afiliados (Blindagem contra mudanças de URL).
- [x] **Página Inicial (Portal):**
    - [x] Criar layout customizado `layouts/index.html`.
    - [x] Adicionar seção "Hero" com proposta de valor clara.
    - [x] Criar grids de categorias (Atendimento, Vendas, etc.) em vez de lista única.
    - [x] Destacar artigos "Pilar" na home.

## 🟢 Fase 3: A Fábrica de Conteúdo (Concluída)
- [x] **Mineração de Dados:** Criar base de dados (CSV/JSON) com 50+ ferramentas.
- [x] **Geração em Massa:** Script para criar páginas de review automaticamente.
- [x] **Conteúdo Pilar:** Escrever os 4 guias definitivos (Humanos).

## 🟡 Fase 4: Refinamento Visual & UX (A Fazer)
-   **1. Identidade Visual:**
    -   [x] **1.1:** Criar um logo (versões horizontal e ícone) e um favicon.
    -   [x] **1.2:** Adicionar os arquivos de imagem à pasta `static/img/`.
    -   [x] **1.3:** Definir a paleta de cores (ex: a cor dourada `#d4af37` como primária) em um arquivo CSS customizado (`assets/css/custom.css`).
    -   [x] **1.4:** Configurar o `hugo.toml` para usar o favicon e o logo no cabeçalho.
-   **2. Tipografia e Leitura:**
    -   [x] **2.1:** No `custom.css`, aumentar o `line-height` (espaço entre linhas) do corpo do texto para `1.7` para facilitar a leitura.
    -   [x] **2.2:** Definir um `max-width` para os parágrafos (ex: `70ch`) para evitar linhas muito longas em telas grandes.
-   **3. Revisão Mobile:**
    -   [x] **3.1:** Iniciar o servidor local (`hugo server`).
    -   [x] **3.2:** Usar as ferramentas de desenvolvedor do navegador para simular a visualização em dispositivos móveis (iPhone 12, etc.).
    -   [x] **3.3:** **(Ação Crítica)** Adicionar `overflow-x: auto;` ao container das tabelas de "Prós e Contras" para que elas rolem horizontalmente em telas pequenas, em vez de quebrar o layout.
-   **4. Otimização de CTAs (Call-to-Action):**
    -   [x] **4.1:** Revisar a cor do botão principal (verde) para garantir que ele tenha um bom contraste no modo claro e escuro.
    -   [x] **4.2:** Garantir que todos os links importantes, especialmente os de afiliados, se destaquem visualmente do texto normal.
-   **5. Modo Escuro (Dark Mode):**
    -   [x] **5.1:** (Desabilitado temporariamente) Opção removida do `hugo.toml` para focar no lançamento MVP.
-   **6. Refino Visual do Usuário:**
    -   [ ] **6.1:** Ajustes finos de layout e design a serem realizados pelo usuário posteriormente.

##  Fase 5: Setup Operacional & Financeiro (A Fazer)

### Infraestrutura de Código & Deploy (Netlify/GitHub)
- [ ] **GitHub:** Criar e vincular a conta GitHub (Hospedagem do Código).
- [ ] **Netlify:** Criar e vincular a conta Netlify (Hospedagem e Publicação Gratuita).
- [ ] **Domínio:** Registrar e configurar o domínio Geode.ai (Compra e apontamento dos Nameservers).

### Propriedade Digital (Branding & Confiança B2B)
- [ ] **LinkedIn:** Criar a Company Page no LinkedIn (Geode AI).
- [ ] **Redes Sociais:** Garantir perfis de Instagram e Pinterest (reserva de arrobas, alinhado com o nome Geode.ai).
- [x] **Identidade Visual:** Criação do Logotipo e Favicon (para instalar no site).

### Analytics & Rastreamento (Validação da Conversão)
- [ ] **GA4:** Criar a conta Google Analytics 4 (GA4) e obter o ID de Medição (G-XXXXX).
- [ ] **Clarity:** Criar a conta Microsoft Clarity (para Heatmaps e gravações de sessão).

### Infraestrutura Financeira (Recebimento de Comissões)
- [ ] **Conta Global:** Abrir conta em Wise ou Payoneer (para receber em USD/EUR).
- [ ] **Dados Bancários:** Obter os dados bancários em USD para cadastros em plataformas globais.

### Cadastros em Redes de Afiliados (Prioridade)
- [ ] **PartnerStack:** Cadastrar na rede PartnerStack (para a maioria dos SaaS de Vendas/Produtividade).
- [ ] **Impact:** Cadastrar na rede Impact (para HubSpot, Canva e grandes players).

## 🔴 Fase 6: Lançamento e Legal (A Fazer)
-   **1. Páginas de Compliance:**
    -   [ ] **1.1:** Criar os arquivos de conteúdo: `content/termos-de-uso.md`, `content/politica-de-privacidade.md`, `content/aviso-afiliado.md`.
    -   [ ] **1.2:** Usar geradores online para criar um texto base para cada uma dessas páginas.
    -   [ ] **1.3:** Adicionar os links para essas páginas no rodapé do site, editando o template correspondente do tema.
-   **2. Deploy em Produção:**
    -   [ ] **2.1:** Garantir que o projeto está em um repositório no GitHub.
    -   [ ] **2.2:** Criar uma conta na **Vercel** (preferível para Hugo por sua velocidade e simplicidade).
    -   [ ] **2.3:** Na Vercel, importar o repositório do GitHub. As configurações de build (`hugo`) e o diretório de publicação (`public`) geralmente são detectadas automaticamente.
    -   [ ] **2.4:** Apontar um domínio customizado (ex: `geode.com.br`) para o deploy da Vercel.
-   **3. Analytics e SEO:**
    -   [ ] **3.1:** Criar uma propriedade no **Google Analytics 4**.
    -   [ ] **3.2:** Adicionar o ID de medição do GA4 no `hugo.toml` (o tema PaperMod tem um campo específico para isso).
    -   [ ] **3.3:** Criar e submeter um `sitemap.xml` (gerado automaticamente pelo Hugo) ao Google Search Console.
-   **4. Página Sobre:**
    -   [ ] **4.1:** Criar o arquivo `content/sobre.md` com o manifesto do projeto e "Quem Somos".