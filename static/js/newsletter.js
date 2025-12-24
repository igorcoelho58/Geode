// Sistema de Newsletter - Coleta Offline
// Salva emails localmente até integração com plataforma

document.addEventListener('DOMContentLoaded', function() {
    // Formulário do rodapé
    initializeFooterForm();
    
    // Modal popup
    initializeModalForm();
});

// ===================================
// FORMULÁRIO DO RODAPÉ
// ===================================
function initializeFooterForm() {
    const form = document.getElementById('newsletter-form');
    const emailInput = document.getElementById('newsletter-email');
    const consentCheckbox = document.getElementById('newsletter-consent');
    const messageDiv = document.getElementById('newsletter-message');
    const submitBtn = document.getElementById('newsletter-btn');

    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validação
        if (!emailInput.value || !emailInput.validity.valid) {
            showMessage(messageDiv, 'Por favor, insira um email válido.', 'error');
            return;
        }

        if (!consentCheckbox.checked) {
            showMessage(messageDiv, 'Você precisa aceitar a Política de Privacidade.', 'error');
            return;
        }

        // Preparar dados
        const emailData = {
            email: emailInput.value,
            timestamp: new Date().toISOString(),
            consent: true,
            source: 'footer-newsletter'
        };

        // Desabilitar botão durante processamento
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processando...';

        try {
            // Salvar localmente (localStorage como backup)
            saveEmailLocally(emailData, messageDiv);

            // Tentar enviar para servidor (se houver endpoint configurado)
            await saveEmailToFile(emailData);

            // Sucesso
            showMessage(messageDiv, '✅ Inscrito com sucesso! Obrigado por se juntar à nossa comunidade.', 'success');
            emailInput.value = '';
            consentCheckbox.checked = false;

            // Resetar formulário após 5 segundos
            setTimeout(() => {
                messageDiv.textContent = '';
                messageDiv.className = 'newsletter-message';
            }, 5000);

        } catch (error) {
            console.error('Erro ao salvar email:', error);
            if (error.message !== 'Email já cadastrado') {
                showMessage(messageDiv, 'Ocorreu um erro. Por favor, tente novamente.', 'error');
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Assinar';
        }
    });
}

// ===================================
// MODAL POPUP
// ===================================
function initializeModalForm() {
    const modal = document.getElementById('newsletter-modal');
    const openBtn = document.getElementById('open-newsletter-modal');
    const closeBtn = document.querySelector('.newsletter-modal-close');
    const overlay = document.querySelector('.newsletter-modal-overlay');
    const form = document.getElementById('newsletter-modal-form');
    const emailInput = document.getElementById('newsletter-modal-email');
    const consentCheckbox = document.getElementById('newsletter-modal-consent');
    const messageDiv = document.getElementById('newsletter-modal-message');
    const submitBtn = document.getElementById('newsletter-modal-btn');

    if (!modal || !openBtn) return;

    // Abrir modal
    openBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        emailInput.focus();
    });

    // Fechar modal (botão X)
    closeBtn.addEventListener('click', function() {
        closeModal();
    });

    // Fechar modal (clique no overlay)
    overlay.addEventListener('click', function() {
        closeModal();
    });

    // Fechar modal (tecla ESC)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restaurar scroll
        // Limpar mensagens
        messageDiv.textContent = '';
        messageDiv.className = 'newsletter-message';
    }

    // Submit do formulário do modal
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Limpar mensagens anteriores
        messageDiv.textContent = '';
        messageDiv.className = 'newsletter-message';

        // Validação
        if (!emailInput.value || !emailInput.validity.valid) {
            showMessage(messageDiv, 'Por favor, insira um email válido.', 'error');
            return;
        }

        if (!consentCheckbox.checked) {
            showMessage(messageDiv, 'Você precisa aceitar a Política de Privacidade.', 'error');
            return;
        }

        // Preparar dados
        const emailData = {
            email: emailInput.value,
            timestamp: new Date().toISOString(),
            consent: true,
            source: 'modal-popup'
        };

        // Desabilitar botão durante processamento
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processando...';

        try {
            // Salvar localmente
            saveEmailLocally(emailData, messageDiv);
            await saveEmailToFile(emailData);

            // Sucesso
            showMessage(messageDiv, '✅ Inscrito com sucesso! Obrigado por se juntar à nossa comunidade.', 'success');
            emailInput.value = '';
            consentCheckbox.checked = false;

            // Fechar modal após 2 segundos
            setTimeout(() => {
                closeModal();
            }, 2000);

        } catch (error) {
            console.error('Erro ao salvar email:', error);
            if (error.message !== 'Email já cadastrado') {
                showMessage(messageDiv, 'Ocorreu um erro. Por favor, tente novamente.', 'error');
            }
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Assinar Gratuitamente';
        }
    });
}

// ===================================
// FUNÇÕES AUXILIARES
// ===================================
function showMessage(messageDiv, message, type) {
    messageDiv.textContent = message;
    messageDiv.className = `newsletter-message ${type}`;
}

function saveEmailLocally(data, messageDiv) {
    try {
        let emails = JSON.parse(localStorage.getItem('geode_newsletter') || '[]');
        
        // Verificar duplicata
        if (emails.some(item => item.email === data.email)) {
            throw new Error('Email já cadastrado');
        }
        
        emails.push(data);
        localStorage.setItem('geode_newsletter', JSON.stringify(emails));
    } catch (error) {
        if (error.message === 'Email já cadastrado') {
            // Mostrar mensagem apropriada
            if (messageDiv) {
                showMessage(messageDiv, 'Este email já está cadastrado na nossa newsletter.', 'warning');
            }
            throw error;
        }
    }
}

async function saveEmailToFile(data) {
    // Esta função seria implementada com um endpoint backend
    // Por enquanto, simula salvamento
    return new Promise((resolve) => {
        // Em produção, fazer POST para /api/newsletter
        // fetch('/api/newsletter', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(data)
        // })
        
        setTimeout(() => {
            console.log('Email salvo:', data);
            resolve();
        }, 500);
    });
}

// Função auxiliar para exportar emails (usar no console do navegador)
window.exportNewsletterEmails = function() {
    const emails = JSON.parse(localStorage.getItem('geode_newsletter') || '[]');
    const csv = 'Email,Data,Consentimento,Origem\n' + 
                emails.map(item => 
                    `${item.email},${item.timestamp},${item.consent},${item.source}`
                ).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `newsletter_emails_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    console.log(`Exportados ${emails.length} emails`);
};
