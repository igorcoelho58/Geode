# Guia de Exportação de Emails da Newsletter

## Sistema Atual: Coleta Offline (Pré-Lançamento)

O sistema de newsletter está configurado para coletar emails **localmente** no navegador dos visitantes até a integração com plataforma de email marketing ser concluída.

---

## Como Funciona

### 1. **Coleta de Emails**
- Visitantes preenchem o formulário no rodapé
- Sistema valida email e exige consentimento LGPD
- Email é salvo em `localStorage` do navegador
- Mensagem de sucesso é exibida

### 2. **Dados Salvos**
Cada inscrição armazena:
```json
{
  "email": "usuario@exemplo.com",
  "timestamp": "2025-12-24T10:30:00.000Z",
  "consent": true,
  "source": "footer-newsletter"
}
```

### 3. **Proteções Implementadas**
- ✅ Validação de email (formato HTML5)
- ✅ Checkbox LGPD obrigatório
- ✅ Detecção de emails duplicados
- ✅ Feedback visual (sucesso/erro/aviso)

---

## Como Exportar Emails Coletados

### Opção 1: Exportação Via Console (Recomendado)

1. **Abrir o site** em produção (após deploy)
2. **Abrir Console do Navegador:**
   - Chrome/Edge: `F12` ou `Ctrl+Shift+J`
   - Firefox: `F12` ou `Ctrl+Shift+K`
   - Safari: `Cmd+Option+C`

3. **Executar comando:**
   ```javascript
   window.exportNewsletterEmails()
   ```

4. **Resultado:**
   - Arquivo CSV será baixado automaticamente
   - Nome: `newsletter_emails_2025-12-24.csv` (data atual)
   - Formato: `Email,Data,Consentimento,Origem`

### Opção 2: Visualizar Dados Brutos

No console do navegador:
```javascript
JSON.parse(localStorage.getItem('geode_newsletter'))
```

Retorna array com todos os emails salvos.

### Opção 3: Exportação Manual

```javascript
// Copiar dados em JSON
console.log(JSON.stringify(
  JSON.parse(localStorage.getItem('geode_newsletter')),
  null,
  2
))
```

---

## Migração para Plataforma de Email

### Quando o site estiver no ar:

1. **Escolher plataforma** (ConvertKit, Mailchimp, Buttondown)
2. **Exportar emails** usando método acima
3. **Importar CSV** na plataforma escolhida
4. **Atualizar código:**
   - Editar `static/js/newsletter.js`
   - Substituir função `saveEmailToFile()` por integração com API
   - Exemplo ConvertKit:
   ```javascript
   async function saveEmailToFile(data) {
     const response = await fetch('https://api.convertkit.com/v3/forms/{FORM_ID}/subscribe', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
         api_key: 'SEU_API_KEY',
         email: data.email,
         timestamp: data.timestamp
       })
     });
     return response.json();
   }
   ```

5. **Testar fluxo completo**
6. **Configurar double opt-in** na plataforma
7. **Criar email de boas-vindas**
8. **Remover localStorage** (opcional - pode manter como backup)

---

## Estrutura do CSV Exportado

```csv
Email,Data,Consentimento,Origem
usuario1@exemplo.com,2025-12-24T10:30:00.000Z,true,footer-newsletter
usuario2@exemplo.com,2025-12-24T11:45:00.000Z,true,footer-newsletter
usuario3@exemplo.com,2025-12-24T14:20:00.000Z,true,footer-newsletter
```

**Colunas:**
- `Email`: Endereço de email do inscrito
- `Data`: ISO timestamp da inscrição
- `Consentimento`: Sempre `true` (LGPD)
- `Origem`: `footer-newsletter` (pode ter outras fontes no futuro)

---

## Limitações do Sistema Atual

⚠️ **Importante:**
- Emails salvos apenas no navegador do VISITANTE
- Não há servidor backend coletando dados
- Você precisa acessar o site em produção e exportar periodicamente
- Ou implementar backend para salvar em banco de dados

### Solução Temporária (Até Integração):

**Criar endpoint backend simples:**
```javascript
// Netlify Function ou Vercel Serverless
exports.handler = async (event) => {
  const { email, timestamp, consent } = JSON.parse(event.body);
  
  // Salvar em Google Sheets via API
  // Ou enviar email para você
  // Ou salvar em Airtable
  
  return { statusCode: 200 };
};
```

Depois atualizar `saveEmailToFile()` para enviar para esse endpoint.

---

## Checklist Pós-Lançamento

- [ ] Escolher plataforma de email (ConvertKit recomendado)
- [ ] Criar conta na plataforma
- [ ] Exportar emails coletados offline
- [ ] Importar CSV na plataforma
- [ ] Configurar API key no código
- [ ] Atualizar `saveEmailToFile()` com integração real
- [ ] Testar inscrição end-to-end
- [ ] Configurar double opt-in
- [ ] Criar email de boas-vindas
- [ ] Limpar localStorage antigo (ou manter como backup)

---

## Dúvidas ou Problemas

- Função não encontrada? Verifique que `static/js/newsletter.js` está carregado
- CSV vazio? Pode ser que ninguém tenha se inscrito ainda
- Erro de CORS? Backend precisa permitir origem do domínio

**Documentação completa em:** `docs/project_checklist.md` → Fase 8
