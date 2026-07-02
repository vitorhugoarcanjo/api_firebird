// static/js/modules/pasta_vendas/vendas.js

async function carregarDados() {
    const agora = new Date().toLocaleString('pt-BR');
    document.getElementById('atualizacao').innerHTML = `🔄 Atualizado em: ${agora}`;

    try {
        // Busca vendas de hoje
        const respHoje = await fetch('/vendas/hoje');
        const dadosHoje = await respHoje.json();

        if (dadosHoje.status === 'sucesso') {
            document.getElementById('hoje_vendas').textContent = dadosHoje.total_vendas;
            document.getElementById('hoje_faturamento').textContent = 
                'R$ ' + dadosHoje.faturamento.toFixed(2).replace('.', ',');
        }

        document.getElementById('erro').style.display = 'none';

    } catch (erro) {
        document.getElementById('erro').textContent = '❌ Erro ao carregar dados: ' + erro.message;
        document.getElementById('erro').style.display = 'block';
    }
}

// Carrega ao abrir a página
carregarDados();

// Atualiza a cada 30 segundos
setInterval(carregarDados, 30000);