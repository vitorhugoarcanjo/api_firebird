// static/js/modules/pasta_conexoes/cadastrar.js

/**
 * MÓDULO: CADASTRO DE CONEXÃO
 */

// ============================================
// BOTÃO PROCURAR ARQUIVO
// ============================================
function procurarArquivo() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.fdb';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const nomeArquivo = file.name;
            
            // Abre prompt para digitar o caminho completo
            const caminhoSugerido = prompt(
                '📁 Digite o caminho completo do arquivo:\n\n' +
                'Exemplo: D:/Sol.NET/Banco de Dados/JI-PARANA/' + nomeArquivo + '\n\n' +
                '💡 Dica: No Explorer, Shift + Clique direito no arquivo → "Copiar como caminho"',
                'D:/Sol.NET/Banco de Dados/JI-PARANA/' + nomeArquivo
            );
            
            if (caminhoSugerido !== null && caminhoSugerido.trim() !== '') {
                document.getElementById('database').value = caminhoSugerido;
            } else {
                document.getElementById('database').value = nomeArquivo;
            }
        }
    };
    input.click();
}

// ============================================
// TESTAR CONEXÃO (AJAX)
// ============================================
async function testarConexao() {
    const btn = document.querySelector('.btn-testar');
    const resultado = document.getElementById('testeResultado');

    const host = document.getElementById('host').value;
    const database = document.getElementById('database').value;
    const usuario = document.getElementById('usuario').value || 'SYSDBA';
    const senha = document.getElementById('senha').value || 'masterkey';
    const porta = document.getElementById('porta').value || 3050;

    // Valida campos obrigatórios
    if (!host || !database) {
        resultado.className = 'teste-resultado erro';
        resultado.innerHTML = '❌ Preencha Host e Caminho do .FDB antes de testar.';
        return;
    }

    // Mostra loading
    btn.textContent = '⏳ Testando...';
    btn.classList.add('testando');
    resultado.className = 'teste-resultado';
    resultado.innerHTML = '';

    try {
        const resp = await fetch('/conexoes/testar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ host, database, usuario, senha, porta })
        });

        const dados = await resp.json();

        if (dados.status === 'sucesso') {
            resultado.className = 'teste-resultado sucesso';
            resultado.innerHTML = `
                ✅ ${dados.mensagem}
                <div class="detalhes">Versão do Firebird: ${dados.versao || 'N/A'}</div>
            `;
        } else {
            resultado.className = 'teste-resultado erro';
            resultado.innerHTML = `❌ ${dados.mensagem}`;
        }
    } catch (erro) {
        resultado.className = 'teste-resultado erro';
        resultado.innerHTML = `❌ Erro ao testar conexão: ${erro.message}`;
    }

    // Volta o botão ao normal
    btn.textContent = '🔌 Testar';
    btn.classList.remove('testando');
}