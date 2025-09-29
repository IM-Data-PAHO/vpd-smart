// ...existing code...
document.getElementById('lang-en').addEventListener('click', function() {
    setLanguage('en');
    this.classList.add('bg-primary', 'text-white');
    this.classList.remove('bg-gray-100', 'text-gray-600');
    document.getElementById('lang-es').classList.remove('bg-primary', 'text-white');
    document.getElementById('lang-es').classList.add('bg-gray-100', 'text-gray-600');
});

document.getElementById('lang-es').addEventListener('click', function() {
    setLanguage('es');
    this.classList.add('bg-primary', 'text-white');
    this.classList.remove('bg-gray-100', 'text-gray-600');
    document.getElementById('lang-en').classList.remove('bg-primary', 'text-white');
    document.getElementById('lang-en').classList.add('bg-gray-100', 'text-gray-600');
});

// Función para traducir los elementos con data-translate
function setLanguage(lang) {
    window.currentLanguage = lang;
    document.querySelectorAll('[data-translate]').forEach(el => {
        if (window.translations && window.translations[lang] && window.translations[lang][el.getAttribute('data-translate')]) {
            el.textContent = window.translations[lang][el.getAttribute('data-translate')];
        }
    });
}
// Inicializa el idioma en inglés al cargar
window.addEventListener('DOMContentLoaded', function() {
    setLanguage('en');
});