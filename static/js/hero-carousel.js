document.addEventListener('DOMContentLoaded', function() {
  const track = document.querySelector('.hero-carousel-track');
  const slides = document.querySelectorAll('.hero-slide');
  const prevBtn = document.querySelector('.carousel-prev');
  const nextBtn = document.querySelector('.carousel-next');
  const indicators = document.querySelectorAll('.indicator-dot');
  const playPauseBtn = document.querySelector('.carousel-play-pause');
  
  if (!track || slides.length === 0) return;
  
  let currentIndex = 0;
  let autoplayInterval;
  let progressInterval;
  let isPlaying = true;
  let progress = 0;
  const AUTOPLAY_DELAY = 6000; // 6 segundos
  const PROGRESS_STEP = 100; // Atualizar a cada 100ms
  
  function updateProgressBar() {
    const activeIndicator = indicators[currentIndex];
    const progressBar = activeIndicator.querySelector('.progress-bar');
    
    if (progressBar) {
      const percentage = (progress / AUTOPLAY_DELAY) * 100;
      progressBar.style.width = `${percentage}%`;
    }
  }
  
  function resetProgress() {
    progress = 0;
    updateProgressBar();
  }
  
  function startProgress() {
    resetProgress();
    progressInterval = setInterval(() => {
      progress += PROGRESS_STEP;
      updateProgressBar();
      
      if (progress >= AUTOPLAY_DELAY) {
        clearInterval(progressInterval);
      }
    }, PROGRESS_STEP);
  }
  
  function stopProgress() {
    clearInterval(progressInterval);
  }
  
  function goToSlide(index) {
    // Parar progresso atual
    stopProgress();
    
    // Remover active de todos
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(dot => {
      dot.classList.remove('active');
      const progressBar = dot.querySelector('.progress-bar');
      if (progressBar) progressBar.style.width = '0%';
    });
    
    // Adicionar active no atual
    slides[index].classList.add('active');
    indicators[index].classList.add('active');
    
    // Mover o track
    const offset = -index * 100;
    track.style.transform = `translateX(${offset}%)`;
    
    currentIndex = index;
    
    // Iniciar novo progresso se estiver tocando
    if (isPlaying) {
      startProgress();
    }
  }
  
  function nextSlide() {
    const next = (currentIndex + 1) % slides.length;
    goToSlide(next);
  }
  
  function prevSlide() {
    const prev = (currentIndex - 1 + slides.length) % slides.length;
    goToSlide(prev);
  }
  
  function startAutoplay() {
    if (!isPlaying) return;
    stopAutoplay(); // Limpar qualquer interval existente
    startProgress();
    autoplayInterval = setInterval(nextSlide, AUTOPLAY_DELAY);
  }
  
  function stopAutoplay() {
    clearInterval(autoplayInterval);
    stopProgress();
  }
  
  function togglePlayPause() {
    isPlaying = !isPlaying;
    
    if (isPlaying) {
      playPauseBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>';
      playPauseBtn.setAttribute('aria-label', 'Pausar');
      startAutoplay();
    } else {
      playPauseBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
      playPauseBtn.setAttribute('aria-label', 'Reproduzir');
      stopAutoplay();
    }
  }
  
  // Event listeners
  prevBtn.addEventListener('click', () => {
    prevSlide();
    stopAutoplay();
    if (isPlaying) {
      startAutoplay();
    }
  });
  
  nextBtn.addEventListener('click', () => {
    nextSlide();
    stopAutoplay();
    if (isPlaying) {
      startAutoplay();
    }
  });
  
  indicators.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      goToSlide(index);
      stopAutoplay();
      if (isPlaying) {
        startAutoplay();
      }
    });
  });
  
  playPauseBtn.addEventListener('click', togglePlayPause);
  
  // Pausar autoplay quando hover
  const carouselWrapper = document.querySelector('.hero-carousel-wrapper');
  carouselWrapper.addEventListener('mouseenter', () => {
    if (isPlaying) {
      stopAutoplay();
    }
  });
  
  carouselWrapper.addEventListener('mouseleave', () => {
    if (isPlaying) {
      startAutoplay();
    }
  });
  
  // Suporte para swipe em mobile
  let touchStartX = 0;
  let touchEndX = 0;
  
  track.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
    if (isPlaying) stopAutoplay();
  });
  
  track.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
    if (isPlaying) startAutoplay();
  });
  
  function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        nextSlide();
      } else {
        prevSlide();
      }
    }
  }
  
  // Iniciar
  goToSlide(0);
  startAutoplay();
});
