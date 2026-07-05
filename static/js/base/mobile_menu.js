// static/js/base/mobile_menu.js

/**
 * MENU LATERAL - MOBILE
 * Controla a abertura/fechamento do menu em telas pequenas
 */

// Abre o menu
function abrirMenu() {
    const menu = document.getElementById('menuLateral');
    const overlay = document.getElementById('overlay');
    
    if (menu) menu.classList.add('aberto');
    if (overlay) overlay.classList.add('ativo');
    
    // 🔥 Impede o scroll do body quando o menu está aberto
    document.body.style.overflow = 'hidden';
}

// Fecha o menu
function fecharMenu() {
    const menu = document.getElementById('menuLateral');
    const overlay = document.getElementById('overlay');
    
    if (menu) menu.classList.remove('aberto');
    if (overlay) overlay.classList.remove('ativo');
    
    // 🔥 Libera o scroll do body
    document.body.style.overflow = '';
}

// 🔥 Fecha o menu ao redimensionar para desktop
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        fecharMenu();
    }
});

// 🔥 Fecha o menu ao pressionar ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        fecharMenu();
    }
});

// 🔥 Previne o clique no overlay de fechar o menu ao clicar no menu
document.addEventListener('DOMContentLoaded', function() {
    const menu = document.getElementById('menuLateral');
    const overlay = document.getElementById('overlay');
    
    if (overlay) {
        overlay.addEventListener('click', fecharMenu);
    }
    
    // 🔥 Impede que o clique dentro do menu feche ele
    if (menu) {
        menu.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
});