// ==========================================
// SCAM DETECTION - ENHANCED INTERACTIONS
// ==========================================

class ScamDetectionUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAnimations();
        this.setupFormValidation();
        this.setupProgressIndicators();
    }

    setupEventListeners() {
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', this.handleSmoothScroll.bind(this));
        });

        // Form submission with enhanced UX
        const analyzeForm = document.getElementById('analyzeForm');
        if (analyzeForm) {
            analyzeForm.addEventListener('submit', this.handleFormSubmission.bind(this));
        }

        // Character counter
        const messageInput = document.getElementById('message');
        if (messageInput) {
            messageInput.addEventListener('input', this.updateCharacterCount.bind(this));
            messageInput.addEventListener('focus', this.handleInputFocus.bind(this));
            messageInput.addEventListener('blur', this.handleInputBlur.bind(this));
        }

        // Example buttons
        this.setupExampleButtons();

        // Clear button
        const clearBtn = document.querySelector('.btn-clear');
        if (clearBtn) {
            clearBtn.addEventListener('click', this.handleClearForm.bind(this));
        }

        // Navbar scroll effect
        window.addEventListener('scroll', this.handleNavbarScroll.bind(this));

        // Results page animations
        if (document.querySelector('.results-grid')) {
            this.animateResults();
        }
    }

    handleSmoothScroll(e) {
        e.preventDefault();
        const target = document.querySelector(e.currentTarget.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    handleFormSubmission(e) {
        const messageInput = document.getElementById('message');
        const message = messageInput.value.trim();
        
        if (!this.validateMessage(message)) {
            e.preventDefault();
            return;
        }

        this.showLoadingState();
    }

    validateMessage(message) {
        const messageInput = document.getElementById('message');
        
        if (!message) {
            this.showError('Please enter a message to analyze');
            messageInput.focus();
            return false;
        }

        if (message.length < 5) {
            this.showError('Message must be at least 5 characters long');
            messageInput.focus();
            return false;
        }

        if (message.length > 5000) {
            this.showError('Message is too long (maximum 5000 characters)');
            messageInput.focus();
            return false;
        }

        return true;
    }

    showError(message) {
        // Remove existing error
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <div class="alert alert-danger" style="
                background: rgba(255, 71, 87, 0.1);
                border: 1px solid rgba(255, 71, 87, 0.3);
                color: var(--primary-red);
                padding: 15px 20px;
                border-radius: 10px;
                margin-top: 15px;
                backdrop-filter: blur(10px);
                animation: fadeInUp 0.3s ease;
            ">
                <i class="fas fa-exclamation-triangle"></i> ${message}
            </div>
        `;

        // Insert after form group
        const formGroup = document.querySelector('.form-group');
        formGroup.appendChild(errorDiv);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => errorDiv.remove(), 300);
            }
        }, 5000);
    }

    showLoadingState() {
        const submitBtn = document.querySelector('.btn-analyze');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                Analyzing Message...
            `;
            submitBtn.classList.add('loading');
        }

        // Show progress overlay
        this.showProgressOverlay();
    }

    showProgressOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'progress-overlay';
        overlay.innerHTML = `
            <div class="progress-content">
                <div class="progress-spinner">
                    <div class="spinner"></div>
                </div>
                <h3>Analyzing Your Message</h3>
                <div class="progress-steps">
                    <div class="step active" data-step="1">
                        <i class="fas fa-language"></i>
                        <span>Detecting Language</span>
                    </div>
                    <div class="step" data-step="2">
                        <i class="fas fa-brain"></i>
                        <span>AI Analysis</span>
                    </div>
                    <div class="step" data-step="3">
                        <i class="fas fa-shield-alt"></i>
                        <span>Security Check</span>
                    </div>
                    <div class="step" data-step="4">
                        <i class="fas fa-chart-line"></i>
                        <span>Risk Assessment</span>
                    </div>
                </div>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .progress-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                backdrop-filter: blur(10px);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease;
            }
            
            .progress-content {
                text-align: center;
                color: white;
                max-width: 500px;
                padding: 40px;
            }
            
            .progress-spinner {
                margin-bottom: 30px;
            }
            
            .spinner {
                width: 60px;
                height: 60px;
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-top: 3px solid var(--primary-red);
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .progress-content h3 {
                margin-bottom: 40px;
                font-size: 1.5rem;
                color: var(--text-light);
            }
            
            .progress-steps {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }
            
            .step {
                padding: 15px;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
                opacity: 0.5;
            }
            
            .step.active {
                opacity: 1;
                background: rgba(255, 71, 87, 0.2);
                border-color: var(--primary-red);
                transform: scale(1.05);
            }
            
            .step i {
                display: block;
                font-size: 1.5rem;
                margin-bottom: 8px;
                color: var(--primary-red);
            }
            
            .step span {
                font-size: 0.9rem;
                color: var(--text-muted);
            }
            
            .step.active span {
                color: var(--text-light);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        `;
        
        document.head.appendChild(style);
        document.body.appendChild(overlay);

        // Animate progress steps
        this.animateProgressSteps();
    }

    animateProgressSteps() {
        const steps = document.querySelectorAll('.step');
        let currentStep = 0;

        const interval = setInterval(() => {
            if (currentStep > 0) {
                steps[currentStep - 1].classList.remove('active');
            }
            
            if (currentStep < steps.length) {
                steps[currentStep].classList.add('active');
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, 800);
    }

    updateCharacterCount() {
        const messageInput = document.getElementById('message');
        const charCount = document.getElementById('charCount');
        
        if (messageInput && charCount) {
            const count = messageInput.value.length;
            charCount.textContent = count;
            
            // Color coding
            if (count > 4500) {
                charCount.style.color = 'var(--primary-red)';
            } else if (count > 4000) {
                charCount.style.color = 'var(--primary-orange)';
            } else {
                charCount.style.color = 'var(--text-muted)';
            }
        }
    }

    handleInputFocus(e) {
        e.target.parentElement.classList.add('focused');
    }

    handleInputBlur(e) {
        e.target.parentElement.classList.remove('focused');
    }

    setupExampleButtons() {
        const examples = {
            scam: "URGENT: Your PayPal account has been limited due to unusual activity. Click here immediately to verify your identity at http://paypal-verify.com or your account will be permanently closed within 24 hours. Act now!",
            spam: "🎉 CONGRATULATIONS! You've won $10,000! Click this link now to claim your prize: http://fake-lottery.com. Limited time offer - don't miss out on this amazing opportunity!",
            safe: "Hi! Just wanted to check in and see how you're doing. Would love to grab coffee tomorrow at 10am if you're free. Let me know what works for you. Thanks!"
        };

        document.querySelectorAll('.btn-example').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.currentTarget.classList.contains('scam') ? 'scam' :
                           e.currentTarget.classList.contains('spam') ? 'spam' : 'safe';
                
                this.loadExample(type, examples[type]);
            });
        });
    }

    loadExample(type, text) {
        const messageInput = document.getElementById('message');
        if (messageInput) {
            // Clear existing content
            messageInput.value = '';
            
            // Animate typing effect
            this.typeText(messageInput, text);
            
            // Update character count
            setTimeout(() => {
                this.updateCharacterCount();
            }, text.length * 20 + 100);
        }
    }

    typeText(element, text) {
        let i = 0;
        element.focus();
        
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                element.value += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
                element.dispatchEvent(new Event('input'));
            }
        }, 20);
    }

    handleClearForm(e) {
        e.preventDefault();
        const messageInput = document.getElementById('message');
        const charCount = document.getElementById('charCount');
        
        if (messageInput) {
            messageInput.value = '';
            messageInput.focus();
        }
        
        if (charCount) {
            charCount.textContent = '0';
            charCount.style.color = 'var(--text-muted)';
        }

        // Remove any error messages
        const errorMessage = document.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(0, 0, 0, 0.95)';
                navbar.style.backdropFilter = 'blur(20px)';
            } else {
                navbar.style.background = 'var(--glass-bg)';
                navbar.style.backdropFilter = 'blur(20px)';
            }
        }
    }

    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.step-card, .detail-card, .result-card').forEach(el => {
            observer.observe(el);
        });
    }

    setupFormValidation() {
        const messageInput = document.getElementById('message');
        if (messageInput) {
            messageInput.addEventListener('input', () => {
                // Remove error message when user starts typing
                const errorMessage = document.querySelector('.error-message');
                if (errorMessage) {
                    errorMessage.remove();
                }
            });
        }
    }

    setupProgressIndicators() {
        // Add progress indicators for form completion
        const messageInput = document.getElementById('message');
        if (messageInput) {
            messageInput.addEventListener('input', this.updateFormProgress.bind(this));
        }
    }

    updateFormProgress() {
        const messageInput = document.getElementById('message');
        const message = messageInput.value.trim();
        
        // Remove existing progress indicator
        const existingProgress = document.querySelector('.form-progress');
        if (existingProgress) {
            existingProgress.remove();
        }

        if (message.length > 0) {
            const progress = Math.min((message.length / 50) * 100, 100);
            const progressDiv = document.createElement('div');
            progressDiv.className = 'form-progress';
            progressDiv.innerHTML = `
                <div class="progress-bar-container" style="
                    width: 100%;
                    height: 4px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 2px;
                    margin-top: 10px;
                    overflow: hidden;
                ">
                    <div class="progress-bar" style="
                        height: 100%;
                        background: linear-gradient(90deg, var(--primary-red), var(--primary-orange));
                        border-radius: 2px;
                        width: ${progress}%;
                        transition: width 0.3s ease;
                    "></div>
                </div>
            `;
            
            messageInput.parentElement.appendChild(progressDiv);
        }
    }

    animateResults() {
        // Animate risk score and confidence bars
        setTimeout(() => {
            const riskBar = document.querySelector('.risk-bar');
            const confidenceBar = document.querySelector('.confidence-bar');
            
            if (riskBar) {
                const width = riskBar.style.width;
                riskBar.style.width = '0%';
                setTimeout(() => {
                    riskBar.style.width = width;
                }, 500);
            }
            
            if (confidenceBar) {
                const width = confidenceBar.style.width;
                confidenceBar.style.width = '0%';
                setTimeout(() => {
                    confidenceBar.style.width = width;
                }, 800);
            }
        }, 300);

        // Animate verdict icon
        const verdictIcon = document.querySelector('.verdict-icon');
        if (verdictIcon) {
            verdictIcon.style.transform = 'scale(0)';
            setTimeout(() => {
                verdictIcon.style.transform = 'scale(1)';
                verdictIcon.style.transition = 'transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            }, 200);
        }

        // Animate reason items
        const reasonItems = document.querySelectorAll('.reason-item');
        reasonItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
                item.style.transition = 'all 0.3s ease';
            }, 1000 + (index * 100));
        });
    }
}

// Enhanced download report function
function downloadReport() {
    const verdict = document.querySelector('.verdict-title')?.textContent || 'Unknown';
    const riskScore = document.querySelector('.risk-percentage')?.textContent || '0';
    const confidence = document.querySelector('.confidence-percentage')?.textContent || '0';
    const message = document.querySelector('.message-box p')?.textContent || '';
    const timestamp = new Date().toLocaleString();
    const reasons = Array.from(document.querySelectorAll('.reason-item span')).map(el => el.textContent);

    const report = `
╔════════════════════════════════════════════════════════════╗
║                 SCAM DETECTION REPORT                      ║
║                   Advanced AI Analysis                     ║
╚════════════════════════════════════════════════════════════╝

Generated: ${timestamp}
Report ID: ${Date.now().toString(36).toUpperCase()}

═══════════════════════════════════════════════════════════════
📧 ANALYZED MESSAGE
═══════════════════════════════════════════════════════════════

${message}

═══════════════════════════════════════════════════════════════
🔍 ANALYSIS RESULTS
═══════════════════════════════════════════════════════════════

🏷️  Verdict:           ${verdict}
📊 Risk Score:         ${riskScore}%
🧠 AI Confidence:      ${confidence}%
🌐 Language:           ${document.querySelector('.detail-value')?.textContent || 'Unknown'}

═══════════════════════════════════════════════════════════════
💡 ANALYSIS REASONING
═══════════════════════════════════════════════════════════════

${reasons.map((reason, index) => `${index + 1}. ${reason}`).join('\n')}

═══════════════════════════════════════════════════════════════
⚠️  IMPORTANT DISCLAIMER
═══════════════════════════════════════════════════════════════

This analysis is provided by an AI system that estimates fraud 
probability based on language patterns and URL analysis. 

❌ This system does NOT:
   • Verify factual accuracy of claims
   • Provide legal confirmation of fraud
   • Replace human judgment and verification

✅ Always verify important information through official channels
   before taking any action based on this analysis.

═══════════════════════════════════════════════════════════════
📋 SYSTEM INFORMATION
═══════════════════════════════════════════════════════════════

System:     Scam Detection AI v2.0
Engine:     Advanced Machine Learning
Features:   Multi-language support, URL analysis, Pattern recognition
Generated:  ${timestamp}

© 2024 Scam Detection System - All Rights Reserved
    `.trim();

    const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `scam-analysis-report-${Date.now()}.txt`;
    
    // Add download animation
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    // Show success message
    showNotification('Report downloaded successfully!', 'success');
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px 20px;
            color: var(--text-light);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            box-shadow: var(--shadow-light);
        }
        
        .notification-success {
            border-left: 4px solid var(--primary-green);
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .notification-success i {
            color: var(--primary-green);
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    `;
    
    if (!document.querySelector('#notification-styles')) {
        style.id = 'notification-styles';
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ScamDetectionUI();
});

// Global functions for backward compatibility
window.loadExample = function(type) {
    const examples = {
        scam: "URGENT: Your PayPal account has been limited due to unusual activity. Click here immediately to verify your identity at http://paypal-verify.com or your account will be permanently closed within 24 hours.",
        spam: "AMAZING OFFER! Get rich quick with our exclusive investment opportunity! Limited slots available. Click now to earn passive income. Don't miss out!",
        safe: "Hi! Just wanted to check in and see how you're doing. Would love to grab coffee tomorrow at 10am. Let me know if you're free. Thanks!"
    };
    
    const messageInput = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    
    if (messageInput && examples[type]) {
        messageInput.value = examples[type];
        messageInput.focus();
        
        if (charCount) {
            charCount.textContent = examples[type].length;
        }
    }
};