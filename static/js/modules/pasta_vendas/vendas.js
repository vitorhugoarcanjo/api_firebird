// static/js/modules/pasta_vendas/vendas.js

let periodoAtual = 'hoje';

function formatarMoeda(valor) {
    let valorStr = valor.toFixed(2);
    let partes = valorStr.split('.');
    let inteiroFormatado = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return 'R$ ' + inteiroFormatado + ',' + partes[1];
}

function mudarPeriodo(periodo) {
    periodoAtual = periodo;

    document.querySelectorAll('.aba').forEach(btn => {
        btn.classList.remove('ativa');
    });
    document.querySelector(`.aba[data-periodo="${periodo}"]`).classList.add('ativa');

    // 🔥 AJUSTA AS DATAS AUTOMATICAMENTE
    ajustarDatasPorPeriodo(periodo);
    carregarDados();
}

function ajustarDatasPorPeriodo(periodo) {
    const inputInicio = document.getElementById('data_inicio');
    const inputFim = document.getElementById('data_fim');
    const hoje = new Date();
    let dataInicio = new Date();
    let dataFim = new Date();

    if (periodo === 'hoje') {
        dataInicio = hoje;
        dataFim = hoje;
    } else if (periodo === 'semanal') {
        dataFim = hoje;
        dataInicio = new Date(hoje);
        dataInicio.setDate(hoje.getDate() - 6);
    } else if (periodo === 'mensal') {
        dataFim = hoje;
        dataInicio = new Date(hoje);
        dataInicio.setDate(hoje.getDate() - 29);
    }

    inputInicio.value = dataInicio.toISOString().split('T')[0];
    inputFim.value = dataFim.toISOString().split('T')[0];
}

async function carregarDados() {
    const inputInicio = document.getElementById('data_inicio');
    const inputFim = document.getElementById('data_fim');
    
    const dataInicio = inputInicio ? inputInicio.value : '';
    const dataFim = inputFim ? inputFim.value : '';

    // 🔥 MONTA A URL COM AS DUAS DATAS
    let url = `/vendas/${periodoAtual}`;
    if (dataInicio && dataFim) {
        url += `?inicio=${dataInicio}&fim=${dataFim}`;
    } else if (dataInicio) {
        url += `?data=${dataInicio}`;
    }

    document.getElementById('atualizacao').innerHTML = 
        `🔄 Atualizado em: ${new Date().toLocaleString('pt-BR')}`;

    try {
        const resp = await fetch(url);
        const dados = await resp.json();

        if (dados.status === 'sucesso') {
            // Atualiza os cards
            document.getElementById('hoje_finalizados').textContent = dados.total_finalizados;
            document.getElementById('hoje_faturamento_finalizados').textContent = 
                formatarMoeda(dados.faturamento_finalizados);

            document.getElementById('hoje_excluidos').textContent = dados.total_excluidos;
            document.getElementById('hoje_faturamento_excluidos').textContent = 
                formatarMoeda(dados.faturamento_excluidos);

            document.getElementById('hoje_abertos').textContent = dados.total_abertos;
            document.getElementById('hoje_faturamento_abertos').textContent = 
                formatarMoeda(dados.faturamento_abertos);

            // Atualiza os títulos dos cards
            if (dados.data_consulta) {
                const labels = document.querySelectorAll('.card h3');
                labels.forEach(label => {
                    if (!label.innerHTML.includes('📦') && 
                        !label.innerHTML.includes('💰') && 
                        !label.innerHTML.includes('✅') && 
                        !label.innerHTML.includes('❌')) {
                        label.innerHTML = `📅 ${dados.data_consulta}`;
                    }
                });
            }

            document.getElementById('erro').style.display = 'none';
        }

    } catch (erro) {
        document.getElementById('erro').textContent = '❌ Erro ao carregar dados: ' + erro.message;
        document.getElementById('erro').style.display = 'block';
    }
}

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const inputInicio = document.getElementById('data_inicio');
    const inputFim = document.getElementById('data_fim');
    
    if (inputInicio && inputFim) {
        const hoje = new Date().toISOString().split('T')[0];
        inputInicio.value = hoje;
        inputFim.value = hoje;
        
        carregarDados();
        
        // 🔥 ATUALIZA QUANDO O USUÁRIO MUDAR AS DATAS
        inputInicio.addEventListener('change', carregarDados);
        inputFim.addEventListener('change', carregarDados);
    } else {
        carregarDados();
    }
});

setInterval(carregarDados, 30000);