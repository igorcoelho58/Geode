"""
GEODE - FORMATADOR DE ARTIGOS v1.1
====================================
Converte arquivos _raw.md gerados pelo Gemini para o layout Hugo final.

PADRÕES VISUAIS UTILIZADOS:
---------------------------
Este script usa componentes pré-configurados no projeto:

1. SHORTCODES HUGO (layouts/shortcodes/):
   - {{< product_card id="tool-slug" rating="4.5" >}}
   - {{< button href="url" label="Texto" >}}

2. CLASSES CSS CUSTOMIZADAS (assets/css/extended/custom.css):
   - .verdict-box (com .verdict-label e .verdict-text)
   - .pros-cons-grid (com .pros-column e .cons-column)
   - .pricing-editorial-container (com .pricing-plan-item)

IMPORTANTE: Não modifique a estrutura HTML sem verificar o CSS!

Uso:
    python formatar_artigo.py
    
O script processa todos os arquivos *_raw.md encontrados nas pastas de categoria.
"""

import os
import re
import yaml
from datetime import datetime

# Caminho base do projeto
BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")


def extrair_frontmatter_raw(conteudo):
    """Extrai o frontmatter do arquivo _raw.md (formato texto livre)"""
    match = re.search(r'^---\n(.*?)\n---', conteudo, re.DOTALL)
    if not match:
        return {}
    
    # Extrai os campos manualmente (não é YAML válido)
    frontmatter_text = match.group(1)
    metadata = {}
    
    for linha in frontmatter_text.split('\n'):
        linha = linha.strip()
        if ':' in linha and not linha.startswith('ANÁLISE'):
            chave, valor = linha.split(':', 1)
            metadata[chave.strip()] = valor.strip()
    
    return metadata


def extrair_secoes(conteudo):
    """Extrai as seções do artigo bruto usando regex"""
    
    # Remove o frontmatter inicial
    conteudo = re.sub(r'^---\n.*?\n---\n\n', '', conteudo, flags=re.DOTALL)
    
    secoes = {}
    
    # HOOK (50-80 caracteres)
    hook_match = re.search(r'###\s*HOOK\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    secoes['hook'] = hook_match.group(1).strip() if hook_match else ""
    
    # DESCRIPTION (150-250 caracteres)
    desc_match = re.search(r'###\s*DESCRIPTION\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    secoes['description'] = desc_match.group(1).strip() if desc_match else ""
    
    # VEREDITO
    veredito_match = re.search(r'###\s*VEREDITO\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    secoes['veredito'] = veredito_match.group(1).strip() if veredito_match else ""
    
    # O QUE É?
    oque_match = re.search(r'###\s*O QUE É\?\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    secoes['o_que_e'] = oque_match.group(1).strip() if oque_match else ""
    
    # PARA QUEM É INDICADO?
    paraquem_match = re.search(r'###\s*PARA QUEM É INDICADO\?\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    secoes['para_quem'] = paraquem_match.group(1).strip() if paraquem_match else ""
    
    # PRÓS (lista com bullets)
    pros_match = re.search(r'###\s*PRÓS\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    if pros_match:
        pros_text = pros_match.group(1).strip()
        secoes['pros'] = [p.strip().lstrip('-').strip() for p in pros_text.split('\n') if p.strip().startswith('-')]
    else:
        secoes['pros'] = []
    
    # CONTRAS (lista com bullets)
    contras_match = re.search(r'###\s*CONTRAS\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    if contras_match:
        contras_text = contras_match.group(1).strip()
        secoes['contras'] = [c.strip().lstrip('-').strip() for c in contras_text.split('\n') if c.strip().startswith('-')]
    else:
        secoes['contras'] = []
    
    # PREÇOS (pode ter múltiplos planos)
    precos_match = re.search(r'###\s*PREÇOS\s*\n(.+?)(?=\n###|\Z)', conteudo, re.DOTALL)
    if precos_match:
        precos_text = precos_match.group(1).strip()
        secoes['precos'] = extrair_planos_preco(precos_text)
    else:
        secoes['precos'] = []
    
    # CORPO DA ANÁLISE (tudo após "### CORPO DA ANÁLISE")
    corpo_match = re.search(r'###\s*CORPO DA AN[ÁA]LISE\s*\n(.+?)(?=\n###\s*FAQ|\Z)', conteudo, re.DOTALL)
    secoes['corpo'] = corpo_match.group(1).strip() if corpo_match else ""
    
    # FAQ
    faq_match = re.search(r'###\s*FAQ\s*\n```yaml\nfaq:\n(.+?)\n```', conteudo, re.DOTALL)
    if faq_match:
        try:
            faq_yaml = yaml.safe_load("faq:\n" + faq_match.group(1))
            secoes['faq'] = faq_yaml.get('faq', [])
        except:
            secoes['faq'] = []
    else:
        secoes['faq'] = []
    
    return secoes


def extrair_planos_preco(texto_precos):
    """Extrai planos de preço do formato livre do Gemini"""
    planos = []
    
    # Regex para capturar blocos de planos (padrão: **Nome:**, Nome:, Preço:, Descrição:)
    blocos = re.split(r'\*\*[^*]+:\*\*', texto_precos)
    
    for bloco in blocos[1:]:  # Pula o primeiro que geralmente é vazio
        linhas = bloco.strip().split('\n')
        plano = {'nome': '', 'preco': '', 'descricao': ''}
        
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith('- Nome:'):
                plano['nome'] = linha.replace('- Nome:', '').strip()
            elif linha.startswith('- Preço:'):
                plano['preco'] = linha.replace('- Preço:', '').strip()
            elif linha.startswith('- Descrição:'):
                plano['descricao'] = linha.replace('- Descrição:', '').strip()
        
        if plano['nome']:
            planos.append(plano)
    
    return planos


def criar_slug(nome_ferramenta):
    """Cria slug a partir do nome da ferramenta"""
    slug = nome_ferramenta.lower()
    slug = re.sub(r'[^a-z0-9-]', '', slug.replace(' ', '-'))
    return slug


def gerar_artigo_formatado(secoes, metadata):
    """Gera o artigo no formato Hugo final"""
    
    nome_ferramenta = metadata.get('Ferramenta', 'Ferramenta')
    categoria = metadata.get('Categoria', 'geral')
    site_oficial = metadata.get('Site', '#')
    rating = metadata.get('Rating', '4.5')  # Rating padrão
    
    # Gera o frontmatter Hugo
    frontmatter = {
        'title': nome_ferramenta,
        'description': secoes['description'],
        'hook': secoes['hook'],
        'date': datetime.now().strftime('%Y-%m-%d'),
        'categories': [categoria],
        'tags': [nome_ferramenta, "review", "análise"],
        'author': "Equipe Geode",
        'logo': f"/logos/{criar_slug(nome_ferramenta)}.png",
        'official_link': site_oficial,
        'faq': secoes['faq']
    }
    
    # Monta o artigo
    artigo = "---\n"
    artigo += yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    artigo += "---\n\n"
    
    # SHORTCODE: Product Card (com rating e info do produto)
    slug = criar_slug(nome_ferramenta)
    artigo += f'{{{{< product_card id="{slug}" rating="{rating}" >}}}}\n\n'
    
    # SHORTCODE: Botão de Link Oficial
    artigo += f'{{{{< button href="{site_oficial}" label="Visitar Site Oficial" >}}}}\n\n'
    
    # VEREDITO BOX (com classes corretas do custom.css)
    artigo += '<div class="verdict-box">\n'
    artigo += '  <span class="verdict-label">Veredito</span>\n'
    artigo += f'  <p class="verdict-text">{secoes["veredito"]}</p>\n'
    artigo += '</div>\n\n'
    
    # O QUE É?
    artigo += "## O que é?\n\n"
    artigo += secoes['o_que_e'] + "\n\n"
    
    # PARA QUEM É INDICADO?
    artigo += "## Para quem é indicado?\n\n"
    artigo += secoes['para_quem'] + "\n\n"
    
    # PRÓS E CONTRAS
    artigo += "## Prós e Contras\n\n"
    artigo += '<div class="pros-cons-grid">\n'
    artigo += '  <div class="pros-column">\n'
    artigo += '    <h3>Prós</h3>\n'
    artigo += '    <ul>\n'
    for pro in secoes['pros']:
        artigo += f'      <li>{pro}</li>\n'
    artigo += '    </ul>\n'
    artigo += '  </div>\n'
    artigo += '  <div class="cons-column">\n'
    artigo += '    <h3>Contras</h3>\n'
    artigo += '    <ul>\n'
    for contra in secoes['contras']:
        artigo += f'      <li>{contra}</li>\n'
    artigo += '    </ul>\n'
    artigo += '  </div>\n'
    artigo += '</div>\n\n'
    
    # PREÇOS
    if secoes['precos']:
        artigo += "## Preços\n\n"
        artigo += '<div class="pricing-editorial-container">\n'
        for plano in secoes['precos']:
            artigo += '  <div class="pricing-plan-item">\n'
            artigo += '    <div class="plan-info">\n'
            artigo += f'      <span class="plan-name">{plano["nome"]}</span>\n'
            artigo += f'      <p class="plan-description">{plano["descricao"]}</p>\n'
            artigo += '    </div>\n'
            artigo += f'    <span class="plan-price">{plano["preco"]}</span>\n'
            artigo += '  </div>\n\n'
        artigo += '</div>\n\n'
    
    # CORPO DA ANÁLISE (sem título extra, já vem formatado do Gemini)
    artigo += secoes['corpo'] + "\n\n"
    
    return artigo


def processar_arquivo_raw(caminho_raw):
    """Processa um arquivo _raw.md e gera o arquivo formatado"""
    
    print(f"\n📝 Processando: {os.path.basename(caminho_raw)}")
    
    # Lê o arquivo raw
    with open(caminho_raw, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrai metadata e seções
    metadata = extrair_frontmatter_raw(conteudo)
    secoes = extrair_secoes(conteudo)
    
    # Gera artigo formatado
    artigo_formatado = gerar_artigo_formatado(secoes, metadata)
    
    # Define caminho do arquivo final (remove _raw)
    caminho_final = caminho_raw.replace('_raw.md', '.md')
    
    # Salva arquivo formatado
    with open(caminho_final, 'w', encoding='utf-8') as f:
        f.write(artigo_formatado)
    
    print(f"   ✅ Formatado salvo: {os.path.basename(caminho_final)}")
    
    return caminho_final


def main():
    """Processa todos os arquivos _raw.md encontrados"""
    
    print("\n" + "="*70)
    print("  🎨 FORMATADOR DE ARTIGOS GEODE v1.0")
    print("="*70)
    
    # Busca todos os arquivos _raw.md
    arquivos_raw = []
    
    for categoria in ['atendimento', 'marketing', 'produtividade', 'vendas']:
        pasta_categoria = os.path.join(BASE_PATH, categoria)
        if os.path.exists(pasta_categoria):
            for arquivo in os.listdir(pasta_categoria):
                if arquivo.endswith('_raw.md'):
                    arquivos_raw.append(os.path.join(pasta_categoria, arquivo))
    
    if not arquivos_raw:
        print("\n❌ Nenhum arquivo _raw.md encontrado!")
        print(f"   📂 Procurei em: {BASE_PATH}")
        return
    
    print(f"\n📋 Encontrados {len(arquivos_raw)} arquivo(s) para formatar:\n")
    
    for i, arquivo in enumerate(arquivos_raw, 1):
        print(f"   {i}. {os.path.basename(arquivo)}")
    
    # Menu de opções
    print("\n📋 ESCOLHA UMA OPÇÃO:\n")
    print("1️⃣  Formatar TODOS os arquivos")
    print("2️⃣  Formatar UM arquivo específico")
    print("3️⃣  Sair\n")
    
    escolha = input("👉 Sua opção (1-3): ").strip()
    
    if escolha == "3":
        print("\n👋 Até logo!\n")
        return
    
    if escolha == "1":
        # Formata todos
        print(f"\n🚀 Formatando {len(arquivos_raw)} arquivo(s)...\n")
        
        sucesso = 0
        falhas = 0
        
        for arquivo in arquivos_raw:
            try:
                processar_arquivo_raw(arquivo)
                sucesso += 1
            except Exception as e:
                print(f"   ❌ ERRO: {e}")
                falhas += 1
        
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL")
        print("="*70)
        print(f"✅ Formatados com sucesso: {sucesso}")
        print(f"❌ Falhas: {falhas}")
        print("="*70 + "\n")
    
    elif escolha == "2":
        # Formata um específico
        print("\n📋 Arquivos disponíveis:\n")
        for i, arquivo in enumerate(arquivos_raw, 1):
            print(f"   {i}. {os.path.basename(arquivo)}")
        
        try:
            idx = int(input("\n👉 Escolha o número: ").strip()) - 1
            arquivo_escolhido = arquivos_raw[idx]
            
            processar_arquivo_raw(arquivo_escolhido)
            print("\n✅ Formatação concluída!\n")
            
        except (ValueError, IndexError):
            print("\n❌ Opção inválida!\n")
    
    else:
        print("\n❌ Opção inválida!\n")


if __name__ == "__main__":
    main()
