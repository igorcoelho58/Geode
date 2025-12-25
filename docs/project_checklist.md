# Checklist do Projeto Geode - Ordem de Execução Otimizada

---

## ✅ FASES CONCLUÍDAS (1-8)

---

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

## 🟢 Fase 4: Refinamento Visual & UX (Concluída)
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
-   **6. Otimização Visual da Homepage:**
    -   [x] **6.1:** Hero Carousel (automático, play/pause, indicadores)
    -   [x] **6.2:** Cards de Categorias (cores, gradientes, animações, badges)
    -   [x] **6.3:** Seção Produtividade & Gestão (4ª categoria)
    -   [x] **6.4:** Grid responsivo (4→3→2→1 colunas)

## 🟢 Fase 5: Backup e Versionamento (Concluída)
- [x] **Git Repository:** Repositório GitHub criado e conectado (https://github.com/igorcoelho58/Geode)
- [x] **Git Ignore:** Arquivo .gitignore configurado e otimizado
- [x] **Commits Regulares:** Histórico de commits estabelecido (6 commits principais)
- [x] **Branch Main:** Branch principal configurada e sincronizada com origin
- [x] **Versionamento Ativo:** Todo o código está versionado e rastreado

## 🟢 Fase 6: Páginas Essenciais MVP (Concluída)

### 1. Correção de Links do Rodapé - CONCLUÍDA ✅
- [x] **1.1:** Editar `layouts/partials/footer.html` e corrigir links:
    - [x] Mudar `/about` → `/sobre`
    - [x] Mudar `/contact` → `/contato`
    - [x] Mudar `/privacy` → `/politica-privacidade`
    - [x] Mudar `/termos` → `/termos-uso`

### 2. Páginas Institucionais (Menu Cabeçalho) - CONCLUÍDA ✅
- [x] **2.1:** Criar `content/solucoes.md` - Apresentação das 4 categorias de ferramentas
- [x] **2.2:** Criar `content/precos.md` - Transparência sobre modelo de afiliados
- [x] **2.3:** Criar `content/recursos.md` - Guias, blog, comparativos
- [x] **2.4:** Criar `content/sobre.md` - Manifesto, missão, valores, equipe
- [x] **2.5:** Criar `content/contato.md` - Formulário ou email de contato

### 3. Páginas de Compliance LGPD (Rodapé) - CONCLUÍDA ✅
- [x] **3.1:** Criar `content/politica-privacidade.md` - LGPD Lei 13.709/2018
- [x] **3.2:** Criar `content/termos-uso.md` - Condições de uso
- [x] **3.3:** Criar `content/aviso-afiliado.md` - Transparência sobre comissões
- [x] **3.4:** Usar geradores (iubenda, privacypolicies.com) e adaptar ao Brasil

## 🟢 Fase 7: SEO Técnico Básico (Concluída)

### 1. Arquivos SEO Essenciais - CONCLUÍDO ✅
- [x] **1.1:** Criar `static/robots.txt` para controle de crawlers
- [x] **1.2:** Verificar `sitemap.xml` (gerado automaticamente pelo Hugo)
- [x] **1.3:** Configurar sitemap.xml com prioridades e changefreq

### 2. Meta Tags e Structured Data - CONCLUÍDO ✅
- [x] **2.1:** Canonical URLs configuradas (PaperMod já tem)
- [x] **2.2:** Meta tags Open Graph otimizadas (PaperMod já tem)
- [x] **2.3:** Schema.org (Product/Review) adicionado para análises
- [x] **2.4:** Schema.org (Organization) para homepage
- [x] **2.5:** Schema.org (BreadcrumbList) para navegação
- [x] **2.6:** Schema.org (Article) para páginas institucionais

### 3. Google Analytics - PREPARADO ✅
- [x] **3.1:** Campo preparado no `hugo.toml` com instruções claras

## 🟢 Fase 8: Sistema de Newsletter MVP (Concluída)

### 1. Coleta Offline (Pré-Lançamento) - CONCLUÍDA ✅
- [x] **1.1:** Criar formulário funcional no rodapé
- [x] **1.2:** Implementar validação de email no frontend
- [x] **1.3:** Adicionar checkbox de consentimento LGPD
- [x] **1.4:** Implementar mensagens de sucesso/erro/warning
- [x] **1.5:** Salvar emails localmente (localStorage)
- [x] **1.6:** Criar função de exportação para CSV
- [x] **1.7:** Adicionar estilos e animações de feedback

### 2. Documentação
- [x] **2.1:** Criar guia de exportação (`docs/newsletter_export_guide.md`)

---

## � Fase 9: Refinamento Visual das Páginas de Análise (Concluída)

### 1. Componente Veredicto
- [x] **1.1:** Criar `.verdict-box` com gradiente verde (#dcfce7 → #f0fdf4)
- [x] **1.2:** Adicionar SVG checkmark circular verde
- [x] **1.3:** Implementar estrutura HTML com `<strong>` no título
- [x] **1.4:** Adicionar template em 55 ferramentas via script PowerShell

### 2. Tabela de Preços Editorial
- [x] **2.1:** Criar `.pricing-editorial-container` com borda azul esquerda
- [x] **2.2:** Estruturar 4 planos: Grátis, Básico, Profissional, Enterprise
- [x] **2.3:** Implementar design com fundo branco (#ffffff) e sombra suave
- [x] **2.4:** Adicionar template em 55 ferramentas via script PowerShell

### 3. Cards de Prós e Contras (Soft UI)
- [x] **3.1:** Criar `.pros-cons-grid` com layout duas colunas
- [x] **3.2:** Implementar `.pros-column` (fundo verde #f0fdf4, borda #dcfce7)
- [x] **3.3:** Implementar `.cons-column` (fundo rosa #fef2f2, borda #fecaca)
- [x] **3.4:** Adicionar emojis ✅ e ❌ nos títulos
- [x] **3.5:** Adicionar template em 55 ferramentas via script PowerShell

### 4. Botão CTA Premium
- [x] **4.1:** Criar `.cta-button` com azul vibrante (#2563EB)
- [x] **4.2:** Implementar dupla sombra (azul + cinza escuro)
- [x] **4.3:** Adicionar hover effect com elevação (translateY)
- [x] **4.4:** Adicionar template em 55 ferramentas via script PowerShell

### 5. Aviso de Afiliado
- [x] **5.1:** Adicionar seção transparente após header
- [x] **5.2:** Implementar ícone SVG de informação
- [x] **5.3:** Centralizar conteúdo e espaçamento
- [x] **5.4:** Integrar em `single.html` global

### 6. Padronização de Títulos de Seção
- [x] **6.1:** Uniformizar `.related-tools-section .section-title` (1.5rem, 6px padding)
- [x] **6.2:** Uniformizar `.most-read-label` (1.5rem, 6px padding, underline azul 3px)
- [x] **6.3:** Adicionar `.most-read-label .emoji` sem borda
- [x] **6.4:** Resolver conflitos CSS com definições duplicadas

### 7. Refinamento "Análises Mais Lidas"
- [x] **7.1:** Criar cards brancos com largura fixa (600px) e min-height (80px)
- [x] **7.2:** Implementar barra superior azul no hover
- [x] **7.3:** Remover animações de movimento (padding-left)
- [x] **7.4:** Ajustar transições para `box-shadow` apenas
- [x] **7.5:** Remover `.most-read-item::before` que causava caixas douradas

### 8. Refinamento "Mais Análises"
- [x] **8.1:** Implementar gradiente azul no topo dos cards no hover
- [x] **8.2:** Remover animações de deslocamento horizontal
- [x] **8.3:** Padronizar transições suaves

### 9. Correções de Publicidade
- [x] **9.1:** Remover duplicação de label "PUBLICIDADE" (HTML + CSS `::before`)
- [x] **9.2:** Uniformizar padding dos placeholders (45px 20px)
- [x] **9.3:** Remover bordas duplicadas (outer + inner `<p>`)
- [x] **9.4:** Garantir altura consistente em todos os placeholders

### 10. Correções da Home Page
- [x] **10.1:** Adicionar `max-width: 1400px` no `.portal-main` para controlar hero
- [x] **10.2:** Implementar separação `hook` (curto) vs `description` (longo)
- [x] **10.3:** Atualizar `index.html` para usar `{{ .Params.hook | plainify | truncate 80 }}`
- [x] **10.4:** Evitar renderização de HTML do verdict-box via `.Summary`

### 11. Dividers de Seção
- [x] **11.1:** Adicionar `.section-divider` antes do CTA
- [x] **11.2:** Adicionar dividers antes de Ferramentas Relacionadas
- [x] **11.3:** Adicionar dividers antes de Mais Lidas
- [x] **11.4:** Usar cor cinza suave (#cbd5e1)

### 12. Automação e Scripts
- [x] **12.1:** Criar `scripts/add_variables.ps1` para adicionar campo `hook`
- [x] **12.2:** Executar script (53 arquivos atualizados, 5 já tinham)
- [x] **12.3:** Criar `scripts/add_structure.ps1` para inserir templates HTML
- [x] **12.4:** Executar script (1 arquivo atualizado, 54 já tinham estrutura)
- [x] **12.5:** Deletar scripts após execução

---

## 🔴 FASES PENDENTES (10-15)

---

## 🔴 Fase 10: Curadoria de Conteúdo Profundo (CRÍTICO - Diferencial Competitivo)

### 1. Análises Completas por Ferramenta
- [ ] **1.1:** Para CADA uma das 50+ ferramentas:
    - [ ] Pesquisar 3-5 vídeos de review/análise no YouTube
    - [ ] Extrair transcrições dos vídeos
    - [ ] Usar Gemini Pro 3 para sintetizar com base humana
    - [ ] Redigir análise completa (5-10 min de leitura)
    - [ ] Incluir casos de uso reais
    - [ ] Adicionar screenshots e imagens relevantes

### 2. Harmonização Visual das Análises
- [ ] **2.1:** Criar template baseado no G1: Texto → Publicidade → Texto → Conclusão
- [ ] **2.2:** Adicionar seção FAQ por ferramenta
- [ ] **2.3:** Incluir comparativos com alternativas
- [ ] **2.4:** Incorporar vídeos dos reviews pesquisados
- [ ] **2.5:** Criar checklist de qualidade para cada análise

## 🔴 Fase 12: Deploy e Lançamento (Quando Conteúdo Completo)

### 1. Preparação do Deploy
- [ ] **1.1:** Fazer commit e push de todas as mudanças
- [ ] **1.2:** Testar build local: `hugo --minify`
- [ ] **1.3:** Verificar que não há erros de build

### 2. Deploy na Vercel
- [ ] **2.1:** Criar conta na Vercel
- [ ] **2.2:** Conectar repositório GitHub
- [ ] **2.3:** Configurar comando de build: `hugo --minify`
- [ ] **2.4:** Configurar diretório de publicação: `public`
- [ ] **2.5:** Fazer primeiro deploy

### 3. Domínio e SSL
- [ ] **3.1:** Registrar domínio hubgeode.com ($10-15/ano)
- [ ] **3.2:** Configurar DNS apontando para Vercel
- [ ] **3.3:** Ativar SSL/HTTPS automático
- [ ] **3.4:** Testar site em produção

### 4. Testes Finais
- [ ] **4.1:** Testar em Chrome, Firefox, Safari, Edge
- [ ] **4.2:** Testar em dispositivos móveis (iOS e Android)
- [ ] **4.3:** Validar todos os links (interno e externos)
- [ ] **4.4:** Verificar formulário de newsletter
- [ ] **4.5:** Testar links de afiliados

## 🟡 Fase 13: Ativação Pós-Lançamento (Dia 1 após Deploy)

### 1. Google Analytics 4 - ATIVAÇÃO
- [ ] **1.1:** Criar propriedade Google Analytics 4 (GA4)
- [ ] **1.2:** Obter ID de medição (G-XXXXX)
- [ ] **1.3:** Descomentar googleAnalytics no `hugo.toml`
- [ ] **1.4:** Fazer commit e redeploy

### 2. Google Search Console - SUBMISSÃO
- [ ] **2.1:** Criar conta Google Search Console
- [ ] **2.2:** Verificar propriedade do domínio (DNS ou HTML)
- [ ] **2.3:** Submeter sitemap: `https://hubgeode.com/sitemap.xml`
- [ ] **2.4:** Solicitar indexação das principais páginas

### 3. Newsletter - INTEGRAÇÃO COM PLATAFORMA
- [ ] **3.1:** Escolher plataforma (Mailchimp, ConvertKit, Buttondown)
- [ ] **3.2:** Criar conta e obter API key
- [ ] **3.3:** Exportar emails coletados: `window.exportNewsletterEmails()`
- [ ] **3.4:** Importar CSV na plataforma escolhida
- [ ] **3.5:** Atualizar `static/js/newsletter.js` com integração real
- [ ] **3.6:** Configurar double opt-in
- [ ] **3.7:** Criar template de email de boas-vindas
- [ ] **3.8:** Testar fluxo completo
- [ ] **3.9:** Fazer commit e redeploy

### 4. Banner de Cookies LGPD
- [ ] **4.1:** Escolher solução (Cookiebot, OneTrust, ou próprio)
- [ ] **4.2:** Implementar banner conforme LGPD
- [ ] **4.3:** Adicionar página de política de cookies
- [ ] **4.4:** Configurar categorias (essenciais, analytics, afiliados)

## 🟡 Fase 14: Infraestrutura Operacional (Primeira Semana)

### 1. Propriedade Digital
- [ ] **1.1:** Criar LinkedIn Company Page (Geode)
- [ ] **1.2:** Reservar @hubgeode no Instagram
- [ ] **1.3:** Reservar @hubgeode no Pinterest
- [ ] **1.4:** Atualizar URLs reais no rodapé do site

### 2. Analytics Avançado
- [ ] **2.1:** Criar conta Microsoft Clarity
- [ ] **2.2:** Configurar heatmaps e gravações
- [ ] **2.3:** Configurar Google Tag Manager
- [ ] **2.4:** Implementar eventos personalizados (cliques em afiliados)

### 3. Infraestrutura Financeira
- [ ] **3.1:** Abrir conta Wise ou Payoneer
- [ ] **3.2:** Obter dados bancários em USD/EUR
- [ ] **3.3:** Cadastrar em PartnerStack
- [ ] **3.4:** Cadastrar em Impact
- [ ] **3.5:** Cadastrar programas individuais (HubSpot, ActiveCampaign, etc.)

## 🟡 Fase 15: Sistemas Dinâmicos (Quando Houver Tráfego)

### 1. Sistema de Rankeamento
- [ ] **1.1:** Implementar tracking de visualizações (GA4 + backend)
- [ ] **1.2:** Criar algoritmo: visualizações + tempo de permanência
- [ ] **1.3:** Atualizar seção "Análises Mais Lidas" dinamicamente
- [ ] **1.4:** Ativar badges automáticos (Popular, Top 10, Novo)

### 2. Sistema de Busca
- [ ] **2.1:** Implementar busca no cabeçalho
- [ ] **2.2:** Criar índice de ferramentas
- [ ] **2.3:** Adicionar filtros por categoria
- [ ] **2.4:** Implementar autocomplete

### 3. Monitoramento de Afiliados
- [ ] **3.1:** Tracking de cliques em links
- [ ] **3.2:** UTM parameters automáticos
- [ ] **3.3:** Dashboard de performance
- [ ] **3.4:** Alertas para links quebrados

### 4. CMS Interno (Futuro)
- [ ] **4.1:** Painel admin para equipe Geode
- [ ] **4.2:** Formulário de criação de análises
- [ ] **4.3:** Sistema de preview
- [ ] **4.4:** Automação de publicação

### 5. Sistema de Destaque Hero
- [ ] **5.1:** Interface para selecionar destaques
- [ ] **5.2:** Agendamento automático
- [ ] **5.3:** Rotação semanal

## 🟡 Fase 16: Otimização e Crescimento (Contínuo)

### 1. Performance Web
- [ ] **1.1:** Converter logos para WebP
- [ ] **1.2:** Lazy loading de imagens
- [ ] **1.3:** Minificação CSS/JS com Hugo Pipes
- [ ] **1.4:** Otimizar Core Web Vitals
- [ ] **1.5:** Implementar Service Worker

### 2. Engajamento
- [ ] **2.1:** Sistema de comentários (Giscus/Disqus)
- [ ] **2.2:** Botões de compartilhamento social
- [ ] **2.3:** Popup de saída com oferta de newsletter
- [ ] **2.4:** Programa de indicação

### 3. Monetização Avançada
- [ ] **3.1:** Parcerias diretas com SaaS
- [ ] **3.2:** Landing pages exclusivas
- [ ] **3.3:** Comparativos patrocinados
- [ ] **3.4:** Banners publicitários estratégicos

---

## 📊 Métricas de Sucesso (Definir Após Lançamento)
- Taxa de conversão de afiliados por categoria
- Taxa de inscrição na newsletter
- Tempo médio de permanência nas análises
- Taxa de rejeição por página
- Ferramentas mais buscadas/acessadas
- Receita mensal de comissões
