document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 Multimodal AI Demo loaded - Ready for some fun!');
    console.log('%c🎉 Welcome to the Multimodal AI Playground!', 'color: #6a11cb; font-size: 16px; font-weight: bold;');
    console.log('%c💡 Tip: Press Ctrl+Enter to quickly submit your request!', 'color: #2575fc; font-size: 14px;');
    createWelcomeEffect();
});

function createWelcomeEffect() {
    const header = document.querySelector('.header h1');
    if (header) {
        header.style.animation = 'pulse 2s infinite';
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
    }
}

function switchTab(tabIndex) {
    document.querySelectorAll('.tab').forEach((tab, index) => {
        if (index === tabIndex) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    document.querySelectorAll('.tab-content').forEach((content, index) => {
        if (index === tabIndex) {
            content.classList.add('active');
            content.style.animation = 'fadeIn 0.5s ease';
        } else {
            content.classList.remove('active');
        }
    });
    
    if (tabIndex === 4) {
        loadSystemInfo();
    }
}

function previewImage(input, previewId) {
    const file = input.files[0];
    const preview = document.getElementById(previewId);
    const button = getButtonForInput(input.id);
    
    if (file) {
        if (!file.type.startsWith('image/')) {
            showError('Please upload an image file (JPEG, PNG, etc.)');
            input.value = '';
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) {
            showError('File size exceeds 10MB limit. Please choose a smaller image.');
            input.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            preview.style.animation = 'fadeIn 0.5s ease';
            preview.style.border = '3px solid #4ade80';
            preview.style.borderRadius = '10px';
            
            if (button) button.disabled = false;
            showSuccess(`Image loaded successfully! (${formatFileSize(file.size)})`);
        }
        reader.readAsDataURL(file);
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showError(message) {
    let errorDiv = document.getElementById('global-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'global-error';
        errorDiv.className = 'error';
        document.querySelector('.container').prepend(errorDiv);
    }
    errorDiv.textContent = message;
    
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => {
            errorDiv.remove();
        }, 300);
    }, 5000);
}

function showSuccess(message) {
    let successDiv = document.getElementById('global-success');
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.id = 'global-success';
        successDiv.className = 'success-message';
        document.querySelector('.container').prepend(successDiv);
    }
    successDiv.textContent = message;
    
    setTimeout(() => {
        successDiv.style.opacity = '0';
        setTimeout(() => {
            successDiv.remove();
        }, 300);
    }, 3000);
}

function getButtonForInput(inputId) {
    switch(inputId) {
        case 'vqa-file': return document.getElementById('vqa-btn');
        case 'caption-file': return document.getElementById('caption-btn');
        case 'ocr-file': return document.getElementById('ocr-btn');
        case 'detection-file': return document.getElementById('detection-btn');
        default: return null;
    }
}

function showLoading(buttonId, loadingText = "Processing...") {
    const button = document.getElementById(buttonId);
    if (button) {
        button.innerHTML = `<span class="loading"></span> ${loadingText}`;
        button.disabled = true;
    }
}

function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        const activeTab = document.querySelector('.tab-content.active');
        if (activeTab) {
            const button = activeTab.querySelector('button:not(:disabled)');
            if (button) {
                button.click();
                showSuccess('🚀 Request submitted with Ctrl+Enter!');
            }
        }
    }
    
    if (e.key === 'Escape') {
        clearCurrentForm();
    }
});

function clearCurrentForm() {
    const activeTab = document.querySelector('.tab-content.active');
    if (activeTab) {
        const inputs = activeTab.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            if (input.type === 'file') {
                input.value = '';
            } else {
                input.value = '';
            }
        });
        
        const previews = activeTab.querySelectorAll('.preview');
        previews.forEach(preview => {
            preview.style.display = 'none';
        });
        
        const buttons = activeTab.querySelectorAll('button');
        buttons.forEach(button => {
            if (!button.classList.contains('btn-secondary')) {
                button.disabled = true;
            }
        });
        
        const results = activeTab.querySelectorAll('.result');
        results.forEach(result => {
            result.style.display = 'none';
        });
        
        showSuccess('🧹 Form cleared!');
    }
}