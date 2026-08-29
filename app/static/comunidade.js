async function atualizarComunidade(id) {

    const dados = new FormData();

    // Como isso é de teste, ao clicar no botão
    // ele muda para esses valores.
    dados.append("nome", "Rock Atualizado");
    dados.append("descricao", "Descrição atualizada");
    dados.append("imagem_url", "https://exemplo.com/imagem.jpg");

    const resposta = await fetch(`/comunidade/${id}`, {
        method: "PUT",
        body: dados
    });

    console.log("Status:", resposta.status);
    console.log("Resposta:", await resposta.text());
}


async function apagarComunidade(id) {

    const resposta = await fetch(`/comunidade/${id}`, {
        method: "DELETE"
    });

    console.log("Status:", resposta.status);

    if (resposta.ok) {
        window.location.href = "/home";
        return;
    }

    console.log("Resposta:", await resposta.text());
}