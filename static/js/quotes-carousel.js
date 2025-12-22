document.addEventListener('DOMContentLoaded', function() {
  const allQuotes = [
    {
      text: "A melhor maneira de prever o futuro é criá-lo.",
      author: "Peter Drucker",
      role: "Pai da Administração Moderna"
    },
    {
      text: "Inovação distingue um líder de um seguidor.",
      author: "Steve Jobs",
      role: "Fundador da Apple"
    },
    {
      text: "O sucesso geralmente vem para aqueles que estão ocupados demais para procurá-lo.",
      author: "Henry David Thoreau",
      role: "Filósofo e Escritor"
    },
    {
      text: "Sua marca é o que as pessoas dizem sobre você quando você não está na sala.",
      author: "Jeff Bezos",
      role: "Fundador da Amazon"
    },
    {
      text: "O único lugar onde sucesso vem antes de trabalho é no dicionário.",
      author: "Vidal Sassoon",
      role: "Empresário e Cabeleireiro"
    },
    {
      text: "Não tenha medo de desistir do bom para perseguir o ótimo.",
      author: "John D. Rockefeller",
      role: "Empresário e Filantropo"
    },
    {
      text: "A maneira de começar é parar de falar e começar a fazer.",
      author: "Walt Disney",
      role: "Fundador da Disney"
    },
    {
      text: "Se você não está disposto a arriscar, esteja preparado para uma vida comum.",
      author: "Jim Rohn",
      role: "Empresário e Autor"
    },
    {
      text: "Oportunidades não acontecem. Você as cria.",
      author: "Chris Grosser",
      role: "Empreendedor"
    },
    {
      text: "Falhar é uma oportunidade para começar de novo de forma mais inteligente.",
      author: "Henry Ford",
      role: "Fundador da Ford"
    },
    {
      text: "Não compare seu começo com o meio de outra pessoa.",
      author: "Jon Acuff",
      role: "Autor e Palestrante"
    },
    {
      text: "O sucesso é ir de fracasso em fracasso sem perder o entusiasmo.",
      author: "Winston Churchill",
      role: "Primeiro-Ministro Britânico"
    },
    {
      text: "A persistência é o caminho do êxito.",
      author: "Charles Chaplin",
      role: "Cineasta"
    },
    {
      text: "Se você não pode fazer grandes coisas, faça pequenas coisas de uma grande maneira.",
      author: "Napoleon Hill",
      role: "Autor de 'Pense e Enriqueça'"
    },
    {
      text: "O empreendedor sempre busca a mudança, reage a ela e a explora como uma oportunidade.",
      author: "Peter Drucker",
      role: "Pai da Administração Moderna"
    },
    {
      text: "Não espere por oportunidades. Crie-as.",
      author: "George Bernard Shaw",
      role: "Escritor e Dramaturgo"
    },
    {
      text: "Sonhe grande e ouse falhar.",
      author: "Norman Vaughan",
      role: "Explorador"
    },
    {
      text: "Seja você mesmo. Todos os outros já foram escolhidos.",
      author: "Oscar Wilde",
      role: "Escritor"
    },
    {
      text: "A única forma de fazer um excelente trabalho é amar o que você faz.",
      author: "Steve Jobs",
      role: "Fundador da Apple"
    },
    {
      text: "Se você quer algo que nunca teve, precisa fazer algo que nunca fez.",
      author: "Thomas Jefferson",
      role: "Presidente dos EUA"
    },
    {
      text: "O fracasso é apenas a oportunidade de começar de novo com mais inteligência.",
      author: "Henry Ford",
      role: "Fundador da Ford"
    },
    {
      text: "Você não aprende a caminhar seguindo regras. Você aprende fazendo e caindo.",
      author: "Richard Branson",
      role: "Fundador da Virgin Group"
    },
    {
      text: "A melhor hora para plantar uma árvore foi 20 anos atrás. A segunda melhor hora é agora.",
      author: "Provérbio Chinês",
      role: "Sabedoria Ancestral"
    },
    {
      text: "Não conte os dias, faça os dias contarem.",
      author: "Muhammad Ali",
      role: "Campeão Mundial de Boxe"
    },
    {
      text: "O que não é começado hoje nunca é terminado amanhã.",
      author: "Johann Wolfgang von Goethe",
      role: "Escritor e Pensador"
    },
    {
      text: "A execução é tudo. A ideia sem execução não vale nada.",
      author: "Ted Turner",
      role: "Fundador da CNN"
    },
    {
      text: "Sua rede é o seu patrimônio líquido.",
      author: "Porter Gale",
      role: "Executiva de Marketing"
    },
    {
      text: "Faça o que você pode, com o que você tem, onde você está.",
      author: "Theodore Roosevelt",
      role: "Presidente dos EUA"
    },
    {
      text: "A velocidade é útil apenas se você estiver indo na direção certa.",
      author: "Claudio Fernández-Aráoz",
      role: "Consultor Executivo"
    },
    {
      text: "Não é sobre ideias. É sobre tornar as ideias realidade.",
      author: "Scott Belsky",
      role: "CPO da Adobe"
    },
    {
      text: "Clientes não medem você por quão difícil você trabalhou, mas pelos resultados que você entrega.",
      author: "Andrew Grove",
      role: "Ex-CEO da Intel"
    },
    {
      text: "O crescimento e o conforto não podem coexistir.",
      author: "Ginni Rometty",
      role: "Ex-CEO da IBM"
    },
    {
      text: "A melhor publicidade é um cliente satisfeito.",
      author: "Bill Gates",
      role: "Fundador da Microsoft"
    },
    {
      text: "Construa sua própria marca ou alguém irá contratá-lo para construir a deles.",
      author: "Farrah Gray",
      role: "Empresário e Autor"
    },
    {
      text: "Toda ação que você toma é um voto para o tipo de pessoa que você deseja se tornar.",
      author: "James Clear",
      role: "Autor de 'Hábitos Atômicos'"
    },
    {
      text: "O perfeccionismo é inimigo do progresso.",
      author: "Winston Churchill",
      role: "Primeiro-Ministro Britânico"
    },
    {
      text: "Se você não está embaraçado com a primeira versão do seu produto, você lançou tarde demais.",
      author: "Reid Hoffman",
      role: "Fundador do LinkedIn"
    },
    {
      text: "Os detalhes não são os detalhes. Eles fazem o design.",
      author: "Charles Eames",
      role: "Designer"
    },
    {
      text: "Marketing não é sobre o que você vende, mas sobre as histórias que você conta.",
      author: "Seth Godin",
      role: "Autor e Empresário"
    },
    {
      text: "Seu tempo é limitado, não o desperdice vivendo a vida de outra pessoa.",
      author: "Steve Jobs",
      role: "Fundador da Apple"
    },
    {
      text: "A única estratégia que garante o fracasso é não correr riscos.",
      author: "Mark Zuckerberg",
      role: "Fundador do Facebook"
    },
    {
      text: "Não é o mais forte que sobrevive, nem o mais inteligente, mas o que melhor se adapta às mudanças.",
      author: "Charles Darwin",
      role: "Naturalista"
    },
    {
      text: "Cultura come estratégia no café da manhã.",
      author: "Peter Drucker",
      role: "Pai da Administração Moderna"
    },
    {
      text: "Se você não consegue explicar algo de forma simples, você não entende bem o suficiente.",
      author: "Albert Einstein",
      role: "Físico"
    },
    {
      text: "Foque em ser produtivo, não em estar ocupado.",
      author: "Tim Ferriss",
      role: "Autor de 'A Semana de 4 Horas'"
    },
    {
      text: "O cliente raramente compra o que a empresa acha que está vendendo.",
      author: "Peter Drucker",
      role: "Pai da Administração Moderna"
    },
    {
      text: "Você não precisa ser grande para começar, mas precisa começar para ser grande.",
      author: "Zig Ziglar",
      role: "Autor e Palestrante"
    },
    {
      text: "A simplicidade é o último grau de sofisticação.",
      author: "Leonardo da Vinci",
      role: "Artista e Inventor"
    },
    {
      text: "Ideias são fáceis. Implementação é difícil.",
      author: "Guy Kawasaki",
      role: "Chief Evangelist da Apple"
    },
    {
      text: "Não construa um produto para todos, porque então você não o constrói para ninguém.",
      author: "Evan Williams",
      role: "Cofundador do Twitter"
    },
    {
      text: "A experiência do usuário é tudo. Ela sempre foi, sempre será.",
      author: "Evan Williams",
      role: "Cofundador do Twitter"
    },
    {
      text: "Dados são o novo petróleo, mas apenas se você souber refiná-los.",
      author: "Clive Humby",
      role: "Cientista de Dados"
    },
    {
      text: "Software está comendo o mundo.",
      author: "Marc Andreessen",
      role: "Fundador da Netscape"
    },
    {
      text: "Move rápido e quebre coisas. Se você não está quebrando coisas, não está se movendo rápido o suficiente.",
      author: "Mark Zuckerberg",
      role: "Fundador do Facebook"
    },
    {
      text: "O conteúdo é rei, mas o engajamento é rainha, e ela manda no lar.",
      author: "Mari Smith",
      role: "Especialista em Marketing Digital"
    },
    {
      text: "Na era digital, você ou é rápido ou está morto.",
      author: "Jack Welch",
      role: "Ex-CEO da General Electric"
    },
    {
      text: "A automação aplicada a uma operação eficiente aumentará a eficiência. Aplicada a uma operação ineficiente aumentará a ineficiência.",
      author: "Bill Gates",
      role: "Fundador da Microsoft"
    },
    {
      text: "A melhor maneira de prever o futuro é inventá-lo.",
      author: "Alan Kay",
      role: "Cientista da Computação"
    },
    {
      text: "Tecnologia é melhor quando aproxima as pessoas.",
      author: "Matt Mullenweg",
      role: "Fundador do WordPress"
    },
    {
      text: "A IA não vai substituir você. Uma pessoa usando IA vai.",
      author: "Satya Nadella",
      role: "CEO da Microsoft"
    },
    {
      text: "Escale com sistemas, não com esforço.",
      author: "Sam Altman",
      role: "CEO da OpenAI"
    },
    {
      text: "As empresas que sobreviverão são aquelas que souberem usar dados para criar experiências.",
      author: "Sundar Pichai",
      role: "CEO do Google"
    },
    {
      text: "Não otimize para o presente. Otimize para o futuro.",
      author: "Larry Page",
      role: "Cofundador do Google"
    },
    {
      text: "Se você quer ir rápido, vá sozinho. Se quer ir longe, vá acompanhado.",
      author: "Provérbio Africano",
      role: "Sabedoria Ancestral"
    },
    {
      text: "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
      author: "Robert Collier",
      role: "Autor"
    },
    {
      text: "Trabalhe duro em silêncio. Deixe o sucesso fazer o barulho.",
      author: "Frank Ocean",
      role: "Músico e Empresário"
    },
    {
      text: "Você é o que você faz repetidamente. A excelência, portanto, não é um ato, mas um hábito.",
      author: "Aristóteles",
      role: "Filósofo"
    },
    {
      text: "A única métrica que importa é o crescimento consistente.",
      author: "Sam Altman",
      role: "CEO da OpenAI"
    },
    {
      text: "Construa algo que 100 pessoas amem, não algo que 1 milhão de pessoas gostem.",
      author: "Paul Graham",
      role: "Fundador da Y Combinator"
    },
    {
      text: "Falhe rápido, aprenda rápido.",
      author: "Eric Ries",
      role: "Autor de 'A Startup Enxuta'"
    },
    {
      text: "Não pergunte o que o cliente quer. Observe o que ele faz.",
      author: "Jeff Bezos",
      role: "Fundador da Amazon"
    },
    {
      text: "A melhor forma de conquistar clientes é exceder suas expectativas.",
      author: "Richard Branson",
      role: "Fundador da Virgin Group"
    },
    {
      text: "Automatize o repetível, humanize o excepcional.",
      author: "Tony Hsieh",
      role: "Ex-CEO da Zappos"
    },
    {
      text: "Não espere até que tudo esteja perfeito. Nunca estará. Sempre haverá desafios e perfeição é um sonho.",
      author: "Sheryl Sandberg",
      role: "COO do Facebook"
    },
    {
      text: "Você não pode construir uma reputação sobre o que você vai fazer.",
      author: "Henry Ford",
      role: "Fundador da Ford"
    },
    {
      text: "O que é medido é gerenciado.",
      author: "Peter Drucker",
      role: "Pai da Administração Moderna"
    },
    {
      text: "Empreendedores são pessoas que pulam de um penhasco e constroem um avião no caminho para baixo.",
      author: "Reid Hoffman",
      role: "Fundador do LinkedIn"
    },
    {
      text: "A motivação é o que te faz começar. O hábito é o que te mantém firme.",
      author: "Jim Ryun",
      role: "Atleta Olímpico"
    },
    {
      text: "Seja obcecado com o cliente, não com o concorrente.",
      author: "Jeff Bezos",
      role: "Fundador da Amazon"
    },
    {
      text: "O lucro não é um evento. É um hábito.",
      author: "Mike Michalowicz",
      role: "Autor de 'Profit First'"
    },
    {
      text: "Toda empresa é uma empresa de software agora.",
      author: "Satya Nadella",
      role: "CEO da Microsoft"
    },
    {
      text: "O produto mais importante que você criará é sua reputação.",
      author: "Naval Ravikant",
      role: "Investidor e Empreendedor"
    },
    {
      text: "Não conte para as pessoas seus planos. Mostre-lhes seus resultados.",
      author: "Unknown",
      role: "Sabedoria Popular"
    },
    {
      text: "A melhor hora para construir relacionamentos é antes de precisar deles.",
      author: "Keith Ferrazzi",
      role: "Autor de 'Never Eat Alone'"
    },
    {
      text: "A atenção é a nova moeda na economia digital.",
      author: "Gary Vaynerchuk",
      role: "Empreendedor e Palestrante"
    },
    {
      text: "Você não precisa ser diferente para ser melhor. Mas para ser melhor, você precisa ser diferente.",
      author: "Seth Godin",
      role: "Autor e Empresário"
    },
    {
      text: "A qualidade não é um ato. É um hábito.",
      author: "Aristóteles",
      role: "Filósofo"
    },
    {
      text: "Construa algo que as pessoas querem é a única regra que importa.",
      author: "Paul Graham",
      role: "Fundador da Y Combinator"
    },
    {
      text: "O marketing de amanhã é o conteúdo de hoje.",
      author: "Ann Handley",
      role: "Chief Content Officer"
    },
    {
      text: "Foque em valor, não em preço.",
      author: "Warren Buffett",
      role: "CEO da Berkshire Hathaway"
    },
    {
      text: "A melhor ferramenta de vendas é um produto incrível.",
      author: "Jason Fried",
      role: "CEO da Basecamp"
    },
    {
      text: "Não tente ser o melhor do mundo. Seja o único no seu mundo.",
      author: "Seth Godin",
      role: "Autor e Empresário"
    },
    {
      text: "O sucesso sustentável vem de fazer coisas difíceis de copiar.",
      author: "Naval Ravikant",
      role: "Investidor e Empreendedor"
    },
    {
      text: "Venda resultados, não recursos.",
      author: "Aaron Ross",
      role: "Autor de 'Predictable Revenue'"
    },
    {
      text: "A melhor defesa no mercado é uma constante ofensiva de inovação.",
      author: "Brian Tracy",
      role: "Autor e Palestrante"
    }
  ];
  // Filtrar apenas frases curtas (até 65 caracteres) para evitar quebra de linha
  const quotes = allQuotes.filter(q => q.text.length <= 65);
  const quoteText = document.querySelector('.quote-text');
  const authorName = document.querySelector('.author-name');
  const authorRole = document.querySelector('.author-role');
  const quoteContent = document.querySelector('.quote-content');
  const quoteAuthor = document.querySelector('.quote-author');
  
  if (!quoteText || !authorName || !authorRole) return;
  
  let usedQuotes = [];
  let currentQuote = null;

  function getRandomQuote() {
    // Se todas as frases já foram usadas, resetar
    if (usedQuotes.length === quotes.length) {
      usedQuotes = [];
    }

    // Pegar frases disponíveis (não usadas)
    const availableQuotes = quotes.filter((_, index) => !usedQuotes.includes(index));
    
    // Selecionar uma frase aleatória das disponíveis
    const randomIndex = Math.floor(Math.random() * availableQuotes.length);
    const selectedQuote = availableQuotes[randomIndex];
    
    // Marcar como usada
    const originalIndex = quotes.indexOf(selectedQuote);
    usedQuotes.push(originalIndex);
    
    return selectedQuote;
  }

  function updateQuote() {
    // Fade out
    quoteContent.classList.add('quote-fade-out');
    quoteAuthor.classList.add('quote-fade-out');

    setTimeout(() => {
      // Pegar nova frase aleatória
      currentQuote = getRandomQuote();
      
      // Remover TODAS as aspas do texto (simples e curvas)
      let cleanText = currentQuote.text.replace(/["""\“\”']/g, '').trim();
      
      // Atualizar conteúdo
      quoteText.textContent = cleanText;
      authorName.textContent = currentQuote.author;
      authorRole.textContent = currentQuote.role;

      // Fade in
      quoteContent.classList.remove('quote-fade-out');
      quoteAuthor.classList.remove('quote-fade-out');
      
      // Reiniciar animação
      quoteContent.style.animation = 'none';
      quoteAuthor.style.animation = 'none';
      
      setTimeout(() => {
        quoteContent.style.animation = '';
        quoteAuthor.style.animation = '';
      }, 10);
    }, 800);
  }

  // Mostrar primeira frase
  updateQuote();

  // Trocar a cada 10 segundos
  setInterval(updateQuote, 10000);
});
