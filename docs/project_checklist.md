# Checklist do Projeto Geode

## 🟢 Fase 1: Estratégia (Concluída)
- [x] **Escolha do Nicho:** Automação de IA para PMEs (Oceano Azul).
- [x] **Definição de Personas:** Empreendedor "Polvo", Gestor "Sobrecarregado", CLT "Aspirante".
- [x] **Topic Clusters:** Definição dos 4 pilares (Atendimento, Vendas, Marketing, Produtividade).

## � Fase 2: Estrutura Técnica (Concluída)
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
- [x] **Geração em Massa:** Script para criar páginas de review automaticamente via Hugo Archetypes.
- [x] **Conteúdo Pilar:** Escrever os 4 guias definitivos (Humanos).

## 🟡 Fase 4: Refinamento Visual & UX (A Fazer)
- [ ] **Identidade Visual:** Definir Logo, Favicon e Paleta de Cores (CSS Variables).
- [ ] **Tipografia:** Ajustar tamanho de fonte e entrelinha para leitura densa (foco em retenção).
- [ ] **Mobile Check:** Garantir que tabelas comparativas e grids não quebrem no celular.
- [ ] **CTA Design:** Melhorar o destaque visual dos botões de "Ver Preço" e "Visitar Site".
- [ ] **Dark Mode:** Verificar contraste dos elementos customizados (cards) no modo escuro.

## 🔴 Fase 5: Lançamento e Legal (A Fazer)
- [ ] **Compliance:** Páginas de Termos de Uso, Política de Privacidade e Disclaimer de Afiliado.
- [ ] **Página Sobre:** Manifesto e "Quem Somos".
- [ ] **Deploy:** Configurar Netlify/Vercel + GitHub.
- [ ] **Analytics:** Configurar GA4 ou Plausible.
