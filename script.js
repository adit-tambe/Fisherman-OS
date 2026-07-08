/* =====================================================
   FISHERMAN OS — Pitch Deck JavaScript
   Handles: Scroll animations, counter, nav, WhatsApp chat
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation scroll effect ---
    const nav = document.getElementById('nav');
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 60) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Hamburger toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
        });
    }

    // Close mobile menu on link click
    document.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
    });

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // --- Intersection Observer for animations ---
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Trigger counter animation for hero stats
                if (entry.target.classList.contains('slide-hero')) {
                    animateCounters();
                }
                
                // Trigger WhatsApp chat animation
                if (entry.target.classList.contains('slide-solution')) {
                    animateWhatsAppChat();
                }
            }
        });
    }, observerOptions);

    // Observe slides
    document.querySelectorAll('.slide').forEach(slide => {
        observer.observe(slide);
    });

    // Observe problem cards with stagger
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.problem-card').forEach(card => {
        cardObserver.observe(card);
    });

    // --- Counter Animation ---
    let countersAnimated = false;
    
    function animateCounters() {
        if (countersAnimated) return;
        countersAnimated = true;
        
        document.querySelectorAll('.hero-stat-number').forEach(counter => {
            const target = parseInt(counter.dataset.count);
            const duration = 1500;
            const start = performance.now();
            
            function update(currentTime) {
                const elapsed = currentTime - start;
                const progress = Math.min(elapsed / duration, 1);
                
                // Ease out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.round(eased * target);
                
                counter.textContent = current;
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            }
            
            requestAnimationFrame(update);
        });
    }

    // --- WhatsApp Chat Animation ---
    let chatAnimated = false;
    
    function animateWhatsAppChat() {
        if (chatAnimated) return;
        chatAnimated = true;
        
        const messages = document.querySelectorAll('.wa-message');
        messages.forEach((msg, index) => {
            setTimeout(() => {
                msg.classList.add('visible');
            }, index * 600);
        });
    }

    // --- Feature card interaction ---
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', () => {
            featureCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
        
        card.addEventListener('mouseenter', () => {
            featureCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
    });

    // --- Particle Background ---
    function createParticles() {
        const container = document.getElementById('particles');
        if (!container) return;
        
        const particleCount = 30;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 3 + 1}px;
                height: ${Math.random() * 3 + 1}px;
                background: rgba(0, 212, 170, ${Math.random() * 0.3 + 0.1});
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${Math.random() * 6 + 4}s ease-in-out infinite;
                animation-delay: ${Math.random() * 4}s;
                pointer-events: none;
            `;
            container.appendChild(particle);
        }
    }
    
    createParticles();

    // --- Proof cards counter on scroll ---
    const proofObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numEl = entry.target.querySelector('.proof-number');
                if (numEl && !numEl.dataset.animated) {
                    numEl.dataset.animated = 'true';
                    const text = numEl.textContent;
                    const match = text.match(/[\d,.]+/);
                    if (match) {
                        const target = parseFloat(match[0].replace(/,/g, ''));
                        const prefix = text.substring(0, text.indexOf(match[0]));
                        const suffix = text.substring(text.indexOf(match[0]) + match[0].length);
                        const duration = 1200;
                        const start = performance.now();
                        
                        function update(currentTime) {
                            const elapsed = currentTime - start;
                            const progress = Math.min(elapsed / duration, 1);
                            const eased = 1 - Math.pow(1 - progress, 3);
                            let current;
                            
                            if (target >= 1000) {
                                current = Math.round(eased * target).toLocaleString();
                            } else if (Number.isInteger(target)) {
                                current = Math.round(eased * target);
                            } else {
                                current = (eased * target).toFixed(1);
                            }
                            
                            numEl.textContent = prefix + current + suffix;
                            
                            if (progress < 1) {
                                requestAnimationFrame(update);
                            } else {
                                numEl.textContent = text;
                            }
                        }
                        
                        requestAnimationFrame(update);
                    }
                }
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.proof-card').forEach(card => {
        proofObserver.observe(card);
    });

    // --- Expansion path animation ---
    const expObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const nodes = entry.target.querySelectorAll('.expansion-node');
                const connectors = entry.target.querySelectorAll('.expansion-connector');
                
                nodes.forEach((node, i) => {
                    setTimeout(() => {
                        node.style.opacity = '1';
                        node.style.transform = 'translateY(0)';
                    }, i * 200);
                });
                
                connectors.forEach((conn, i) => {
                    setTimeout(() => {
                        conn.style.opacity = '1';
                        conn.style.transform = 'scaleX(1)';
                    }, i * 200 + 100);
                });
            }
        });
    }, { threshold: 0.3 });

    const expansionPath = document.querySelector('.expansion-path');
    if (expansionPath) {
        // Set initial state
        expansionPath.querySelectorAll('.expansion-node').forEach(node => {
            node.style.opacity = '0';
            node.style.transform = 'translateY(20px)';
            node.style.transition = 'all 0.5s ease';
        });
        expansionPath.querySelectorAll('.expansion-connector').forEach(conn => {
            conn.style.opacity = '0';
            conn.style.transform = 'scaleX(0)';
            conn.style.transition = 'all 0.5s ease';
        });
        
        expObserver.observe(expansionPath);
    }

    // --- Active nav link on scroll ---
    const sections = document.querySelectorAll('.slide[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        document.querySelectorAll('.nav-link').forEach(link => {
            link.style.color = '';
            if (link.getAttribute('href') === `#${current}`) {
                link.style.color = 'var(--accent-teal)';
            }
        });
    });
});
