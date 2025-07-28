// Mobile Navigation Toggle
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    
    // Animate hamburger menu
    navToggle.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.service-item, .portfolio-item, .package-card, .about-content, .testimonial').forEach(el => {
    observer.observe(el);
});

// Contact form handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        
        // Simple form validation
        const requiredFields = ['name', 'email'];
        let isValid = true;
        
        requiredFields.forEach(field => {
            const input = this.querySelector(`[name="${field}"]`);
            if (!formObject[field] || formObject[field].trim() === '') {
                input.style.borderColor = '#ff0000';
                isValid = false;
            } else {
                input.style.borderColor = '#ddd';
            }
        });
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const emailInput = this.querySelector('[name="email"]');
        if (formObject.email && !emailRegex.test(formObject.email)) {
            emailInput.style.borderColor = '#ff0000';
            isValid = false;
        }
        
        if (isValid) {
            // Show success message
            showMessage('Thank you for your message! We\'ll get back to you soon.', 'success');
            this.reset();
        } else {
            showMessage('Please fill in all required fields correctly.', 'error');
        }
    });
}

// Message display function
function showMessage(message, type) {
    // Remove existing messages
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message ${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        text-align: center;
        font-weight: 500;
        ${type === 'success' ? 
            'background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;' : 
            'background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;'
        }
    `;
    
    // Insert message
    const form = document.querySelector('.contact-form');
    form.insertBefore(messageDiv, form.firstChild);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Portfolio image lightbox effect
document.querySelectorAll('.portfolio-item').forEach(item => {
    item.addEventListener('click', function() {
        const img = this.querySelector('img');
        if (img) {
            openLightbox(img.src, img.alt);
        }
    });
});

// Lightbox functionality
function openLightbox(src, alt) {
    // Create lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        cursor: pointer;
    `;
    
    // Create image
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: 4px;
    `;
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 30px;
        background: none;
        border: none;
        color: white;
        font-size: 3rem;
        cursor: pointer;
        z-index: 10000;
    `;
    
    lightbox.appendChild(img);
    lightbox.appendChild(closeBtn);
    document.body.appendChild(lightbox);
    
    // Close lightbox events
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target === closeBtn) {
            document.body.removeChild(lightbox);
        }
    });
    
    // Close with escape key
    document.addEventListener('keydown', function escapeHandler(e) {
        if (e.key === 'Escape') {
            if (document.body.contains(lightbox)) {
                document.body.removeChild(lightbox);
            }
            document.removeEventListener('keydown', escapeHandler);
        }
    });
}

// Package card interactions
document.querySelectorAll('.package-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px)';
    });
    
    card.addEventListener('mouseleave', function() {
        if (!this.classList.contains('featured')) {
            this.style.transform = 'translateY(0)';
        }
    });
});

// Lazy loading for images
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src || img.src;
            img.classList.remove('lazy');
            imageObserver.unobserve(img);
        }
    });
});

document.querySelectorAll('img[data-src]').forEach(img => {
    imageObserver.observe(img);
});

// Scroll to top functionality
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '↑';
scrollToTopBtn.className = 'scroll-to-top';
scrollToTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background-color: #000;
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
`;

document.body.appendChild(scrollToTopBtn);

// Show/hide scroll to top button
window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        scrollToTopBtn.style.opacity = '1';
        scrollToTopBtn.style.visibility = 'visible';
    } else {
        scrollToTopBtn.style.opacity = '0';
        scrollToTopBtn.style.visibility = 'hidden';
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroImage = document.querySelector('.hero-image img');
    if (heroImage) {
        heroImage.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add loading state to buttons
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function() {
        if (this.type === 'submit') {
            this.style.opacity = '0.7';
            this.style.pointerEvents = 'none';
            
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.pointerEvents = 'auto';
            }, 2000);
        }
    });
});

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add fade-in class to hero elements
    setTimeout(() => {
        document.querySelector('.hero-text').classList.add('fade-in');
    }, 300);
    
    // Stagger animation for navigation links
    document.querySelectorAll('.nav-link').forEach((link, index) => {
        setTimeout(() => {
            link.style.opacity = '1';
            link.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Form input focus effects
document.querySelectorAll('.form-group input, .form-group textarea').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
        if (this.value === '') {
            this.parentElement.classList.remove('focused');
        }
    });
});

// Add CSS for focused form groups
const style = document.createElement('style');
style.textContent = `
    .form-group.focused input,
    .form-group.focused textarea {
        border-color: #000;
        box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
    }
    
    .nav-link {
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.3s ease;
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style);