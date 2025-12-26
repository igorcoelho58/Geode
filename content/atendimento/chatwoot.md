---
title: "Chatwoot"
description: "Plataforma de engajamento que unifica WhatsApp, Site, Facebook e E-mail em uma única caixa de entrada. Flexível, permite auto-hospedagem (self-hosted) para controle total de dados ou uso em nuvem para facilidade imediata."
hook: "Alternativa Open Source ao Zendesk e Intercom para atendimento omnichannel"
date: 2024-12-26
draft: false
categories: ["Atendimento"]
tags: ["atendimento", "help-desk", "omnichannel", "open-source", "whatsapp"]
author: "Geode"
logo: "/logos/chatwoot.png"
official_link: "https://www.chatwoot.com/"

faq:
  - question: "O Chatwoot é realmente gratuito?"
    answer: "Sim e não. A versão 'Community Edition' é gratuita para baixar e instalar no seu próprio servidor (você paga apenas o custo do servidor, como uma VPS na DigitalOcean de 5 dólares). Já a versão Cloud (SaaS), onde eles hospedam para você, tem um plano grátis limitado e planos pagos a partir de 19 dólares."
  
  - question: "Consigo usar o WhatsApp no Chatwoot?"
    answer: "Sim. O Chatwoot integra com a API Oficial do WhatsApp Cloud (Meta) e também via provedores como Twilio e 360Dialog. Vale lembrar que, embora o Chatwoot não cobre taxa extra por isso na versão open source, a Meta cobra pelas conversas iniciadas (modelo de janelas de 24h)."
  
  - question: "Preciso ser programador para usar?"
    answer: "Para a versão Cloud (paga), não. É só criar conta e usar. Para a versão Self-Hosted (gratuita), sim, é necessário conhecimento técnico para configurar servidor, Docker e manutenção básica."
  
  - question: "Ele substitui o RD Station ou HubSpot?"
    answer: "Não totalmente. O Chatwoot é focado em ATENDIMENTO e SUPORTE. Embora tenha CRM básico (cadastro de contatos), ele não tem ferramentas de disparo de e-mail marketing em massa ou landing pages. Ele trabalha melhor integrado a essas ferramentas."
  
  - question: "Tem aplicativo para celular?"
    answer: "Sim, o Chatwoot possui aplicativos oficiais gratuitos para Android e iOS, permitindo que os agentes respondam aos clientes de qualquer lugar."
---

<div class="verdict-box">
  <span class="verdict-label">Veredito</span>
  <p class="verdict-text">O <a href="https://www.chatwoot.com/" target="_blank" rel="noopener">Chatwoot</a> é a escolha <strong>IDEAL para equipes técnicas, startups e PMEs</strong> que precisam de uma solução de atendimento robusta sem pagar os preços proibitivos do Intercom ou Zendesk. O grande diferencial é a liberdade: você pode usar a versão Cloud (SaaS) ou hospedar em seu próprio servidor (Self-hosted) gratuitamente, mantendo 100% da privacidade dos dados. <strong>Vale muito a pena</strong> se você precisa centralizar WhatsApp e chat do site em um só lugar com uma interface limpa. <strong>Evite</strong> a versão self-hosted se você não tiver ninguém técnico na equipe para manter o servidor rodando, pois a configuração inicial pode assustar leigos.</p>
</div>

## O que é?

O <a href="https://www.chatwoot.com/" target="_blank" rel="noopener">Chatwoot</a> é uma plataforma de suporte ao cliente "omnichannel". Na prática, ele resolve a bagunça de ter que abrir 5 abas diferentes para responder clientes (uma para e-mail, uma para WhatsApp, uma para Instagram, etc.). Ele puxa todas essas conversas para uma única tela – uma caixa de entrada compartilhada onde vários atendentes podem trabalhar simultaneamente. Nascido como uma alternativa Open Source (código aberto), ele se posiciona como uma ferramenta transparente, focada na privacidade e na colaboração interna da equipe, permitindo que atendentes conversem entre si "dentro" do chamado do cliente sem que ele veja.

## Para quem é indicado?

É indicado principalmente para **Startups de tecnologia, E-commerces e Agências** que lidam com múltiplos canais de atendimento e querem fugir de custos dolarizados altos. É perfeito para empresas que levam a LGPD e privacidade de dados a sério, pois permite hospedar a ferramenta em infraestrutura própria.

**NÃO é a melhor escolha** para empresas que buscam uma solução "all-in-one" que inclua CRM de vendas complexo e automação de marketing pesada nativa (como HubSpot ou RD Station) – o foco aqui é conversação e suporte. Também não indicamos a versão self-hosted para empreendedores "solo" sem conhecimento técnico em servidores Linux/Docker.

## Prós e Contras

<div class="pros-cons-grid">
  <div class="pros-column">
    <h3>Prós</h3>
    <ul>
      <li><strong>Open Source</strong> Código auditável e versão Community gratuita para auto-hospedagem</li>
      <li><strong>Omnichannel Real</strong> Unifica WhatsApp, E-mail, SMS, Telegram, Line e Chat de Site</li>
      <li><strong>Colaboração</strong> Notas privadas permitem que a equipe converse sobre o problema no próprio chat</li>
      <li><strong>Aplicativos Móveis</strong> Apps para Android e iOS funcionais para atender em movimento</li>
      <li><strong>Chatbots</strong> Integração facilitada com Dialogflow e Rasa para automatizar o início da conversa</li>
      <li><strong>Interface Limpa</strong> UX muito similar ao Intercom, facilitando o treinamento da equipe</li>
    </ul>
  </div>
  <div class="cons-column">
    <h3>Contras</h3>
    <ul>
      <li><strong>Configuração Técnica</strong> A versão self-hosted exige conhecimento em Docker/Heroku/Caprover</li>
      <li><strong>Automação Nativa Limitada</strong> Depende de webhooks/n8n para automações complexas de marketing</li>
      <li><strong>Relatórios Básicos</strong> Os dashboards são funcionais, mas menos profundos que os do Zendesk Enterprise</li>
      <li><strong>Custo do WhatsApp</strong> A integração oficial do WhatsApp (Cloud API) tem custos da Meta, não é "grátis"</li>
      <li><strong>Tradução</strong> Alguns termos nas configurações profundas podem estar em inglês ou com tradução parcial</li>
    </ul>
  </div>
</div>

## Preços

<div class="pricing-editorial-container">
  <div class="pricing-plan-item">
    <div class="plan-info">
      <span class="plan-name">Hacker</span>
      <p class="plan-description">Até 2 agentes, histórico de 30 dias, ideal para testes e validação inicial</p>
    </div>
    <span class="plan-price">$0/agente/mês</span>
  </div>

  <div class="pricing-plan-item">
    <div class="plan-info">
      <span class="plan-name">Startups</span>
      <p class="plan-description">Usuários e histórico ilimitados, relatórios básicos e domínio personalizado</p>
    </div>
    <span class="plan-price">$19/agente/mês</span>
  </div>

  <div class="pricing-plan-item">
    <div class="plan-info">
      <span class="plan-name">Business</span>
      <p class="plan-description">CSAT (pesquisa de satisfação), equipes avançadas e deduplicação de contatos</p>
    </div>
    <span class="plan-price">$39/agente/mês</span>
  </div>

  <div class="pricing-plan-item">
    <div class="plan-info">
      <span class="plan-name">Enterprise</span>
      <p class="plan-description">Gestor de conta dedicado, SLA de suporte e logs de auditoria corporativos</p>
    </div>
    <span class="plan-price">$99/agente/mês</span>
  </div>

  <div class="pricing-plan-item">
    <div class="plan-info">
      <span class="plan-name">Community Edition</span>
      <p class="plan-description">Auto-hospedagem: você instala no seu servidor (VPS). Recursos ilimitados sem suporte oficial</p>
    </div>
    <span class="plan-price">Gratuito</span>
  </div>
</div>

## Como Funciona na Prática?

A primeira coisa que chama a atenção no <a href="https://www.chatwoot.com/" target="_blank" rel="noopener">Chatwoot</a> é a familiaridade. Se você já usou WhatsApp Web ou Facebook Messenger, a curva de aprendizado é praticamente zero. A interface é dividida em três colunas clássicas: lista de conversas à esquerda, o chat ativo no centro e as informações do cliente (CRM básico) à direita.

No dia a dia, a mágica acontece na **Caixa de Entrada Unificada**. Um cliente pode mandar um "Oi" pelo widget do seu site e, 10 minutos depois, mandar um e-mail. O Chatwoot consegue (se configurado corretamente) mesclar isso, permitindo que o atendente veja todo o histórico.

Um recurso muito elogiado nos vídeos de análise é a função de **Notas Privadas**. Imagine que um cliente faz uma pergunta técnica difícil. Em vez de gritar para o colega do lado ou abrir o Slack, o atendente digita `@tecnico` dentro da conversa, em uma caixa amarela invisível para o cliente. A equipe colabora ali mesmo e a resposta sai unificada.

Para quem opta pela versão **Self-Hosted** (hospedagem própria), o processo inicial é mais "hacker". Você vai precisar subir uma instância no Docker, Heroku ou Caprover. Depois de configurado, porém, a estabilidade é excelente e você tem o controle total, sem se preocupar com o número de agentes encarecendo a fatura no final do mês.

## Casos de Uso Reais

**Caso 1: A Software House (Suporte Técnico)**

Empresas de software que precisam dar suporte via chat dentro do seu próprio sistema (SaaS). Eles usam o SDK do Chatwoot para embutir o chat no produto. O diferencial aqui é que, como o Chatwoot identifica o usuário logado, o suporte já sabe quem é o cliente, qual o plano dele e o e-mail, eliminando aquelas perguntas repetitivas de "qual seu CPF?".

**Caso 2: E-commerce PME no WhatsApp**

Uma loja virtual que recebe muitos pedidos via WhatsApp e Direct do Instagram. Antes, o celular ficava na mão de um funcionário só. Com o Chatwoot, eles conectam o número do WhatsApp Business API na plataforma e colocam 5 atendentes respondendo o mesmo número simultaneamente, distribuindo os tickets por departamento (Vendas, Trocas, Dúvidas).

**Caso 3: Empresa Focada em Privacidade (LGPD/GDPR)**

Escritórios de advocacia ou clínicas de saúde que não querem que os dados das conversas com clientes fiquem hospedados em servidores de terceiros (como os do Zendesk nos EUA). Eles usam a versão Community do Chatwoot em um servidor próprio no Brasil, garantindo compliance total com leis de proteção de dados.

## Recursos Principais

**Caixa de Entrada Omnichannel**

É o coração da ferramenta. Conecta nativamente com: Website (Live Chat), Facebook, Instagram, Twitter, Telegram, WhatsApp (via API oficial ou provedores como Twilio/360Dialog), Line, SMS e E-mail. Isso centraliza a operação e evita "alt-tab" entre ferramentas.

**Chatbots e Automação (Dialogflow/Rasa)**

O Chatwoot não tem um construtor de fluxo visual "arrasta e solta" nativo super complexo como o ManyChat, mas ele integra perfeitamente com **Dialogflow (Google)** e **Rasa**. Isso significa que você pode criar bots inteligentes que filtram o atendimento, respondem dúvidas frequentes e só passam para um humano quando necessário. Para desenvolvedores, isso é um prato cheio.

**Aplicativos Móveis**

Diferente de muitas ferramentas open source que negligenciam o mobile, o Chatwoot tem apps oficiais para Android e iOS muito competentes. Isso permite que o dono da PME ou o suporte de plantão responda tickets urgentes do sofá de casa sem perder a rastreabilidade.

**Etiquetas e Atribuição Automática**

Você pode criar regras (automação) do tipo: "Se a mensagem contiver a palavra 'financeiro', atribua automaticamente para o Agente João e coloque a etiqueta 'Urgente'". Isso organiza o fluxo sem intervenção humana manual.

## Integrações e Ecossistema

O <a href="https://www.chatwoot.com/" target="_blank" rel="noopener">Chatwoot</a> aposta na extensibilidade. Ele possui integração nativa com **Slack** (para receber notificações de chats novos lá) e **Wordpress** (plugin simples de instalar).

Porém, o poder real está nos **Webhooks**. Praticamente qualquer evento dentro do Chatwoot (nova mensagem, ticket criado, ticket fechado) pode disparar um dado para o **n8n, Zapier ou Make**. Isso permite criar fluxos incríveis, como: "Quando fechar um ticket no Chatwoot, salve o contato no RD Station e mande uma pesquisa de NPS por e-mail".

A API é robusta e bem documentada, sendo um ponto forte para times de desenvolvimento que querem criar integrações customizadas.

## Nossa Avaliação Final

O **Chatwoot** é, sem dúvidas, uma das melhores ferramentas de código aberto surgidas nos últimos anos. Ele democratizou o acesso a um "Help Desk" de nível enterprise. A experiência de uso (UX) é tão boa quanto a de ferramentas que custam 10x mais.

Para o empreendedor brasileiro, a conta é simples: se você tem um mínimo de conhecimento técnico (ou alguém que faça isso), a versão **Self-Hosted é imbatível** em custo-benefício. Se você prefere não mexer com servidores, a versão Cloud ainda é mais barata que os concorrentes diretos (Intercom/Zendesk). Ele peca apenas na falta de automações de marketing nativas, mas cumpre com excelência o papel de organizar o caos do atendimento. É uma ferramenta honesta, rápida e que coloca a privacidade em primeiro lugar.
