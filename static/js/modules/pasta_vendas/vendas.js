// static/js/modules/pasta_vendas/vendas.js

// ============================================
// DASHBOARD DE VENDAS - MÓDULO PRINCIPAL
// ============================================

function formatarMoeda(valor) {
    let valorStr = valor.toFixed(2);
    let partes = valorStr.split('.');
    let inteiroFormatado = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return 'R$ ' + inteiroFormatado + ',' + partes[1];
}

async function carregarDados() {
    const inputData = document.getElementById('selecionar_data');
    const dataSelecionada = inputData ? inputData.value : '';

    let url = '/vendas/hoje';
    if (dataSelecionada) {
        url += `?data=${dataSelecionada}`;
    }

    document.getElementById('atualizacao').innerHTML = 
        `🔄 Atualizado em: ${new Date().toLocaleString('pt-BR')}`;

    try {
        const respHoje = await fetch(url);
        const dadosHoje = await respHoje.json();

        if (dadosHoje.status === 'sucesso') {
            // 🔥 ATUALIZA OS CARDS
            document.getElementById('hoje_vendas').textContent = dadosHoje.total_vendas;
            document.getElementById('hoje_faturamento').textContent = 
                formatarMoeda(dadosHoje.faturamento);

            // 🔥 CORREÇÃO: ATUALIZA TODOS OS TÍTULOS DOS CARDS
            if (dadosHoje.data_consulta) {
                const dataFormatada = new Date(dadosHoje.data_consulta + 'T00:00:00')
                    .toLocaleDateString('pt-BR');
                
                // Atualiza TODOS os títulos dos cards
                const labels = document.querySelectorAll('.card h3');
                labels.forEach(label => {
                    // Só atualiza se não for um dos títulos fixos (Vendas, Faturamento, etc)
                    if (!label.innerHTML.includes('📦') && 
                        !label.innerHTML.includes('💰') && 
                        !label.innerHTML.includes('✅') && 
                        !label.innerHTML.includes('❌')) {
                        label.innerHTML = `📅 ${dataFormatada}`;
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

document.addEventListener('DOMContentLoaded', function() {
    const inputData = document.getElementById('selecionar_data');
    if (inputData) {
        const hoje = new Date().toISOString().split('T')[0];
        inputData.value = hoje;
        carregarDados();
        inputData.addEventListener('change', carregarDados);
    } else {
        carregarDados();
    }
});

setInterval(carregarDados, 30000);