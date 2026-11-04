// Serviço simples inspirado no ApiService do repositório de exemplo.
export default class ApiService {
    constructor(token = null) {
        this.token = token;
    }

    async requisicao(metodo, uri, dados = null) {
        const headers = { "Content-Type": "application/json" };
        if (this.token) {
            headers.Authorization = "Bearer " + this.token;
        }

        const opcoes = { method: metodo, headers: headers };
        if (dados !== null) {
            opcoes.body = JSON.stringify(dados);
        }

        let resposta;
        try {
            resposta = await fetch(uri, opcoes);
        } catch {
            throw new Error("Não foi possível conectar à API. Confira se o servidor está ligado.");
        }

        const json = await resposta.json().catch(() => null);
        if (!resposta.ok || !json || json.success !== true) {
            const mensagem = json?.error?.message || json?.message || "Erro HTTP " + resposta.status;
            const erro = new Error(mensagem);
            erro.status = resposta.status;
            erro.resposta = json;
            throw erro;
        }
        return json;
    }

    get(uri) {
        return this.requisicao("GET", uri);
    }

    getById(uri, id) {
        return this.get(uri + "/" + id);
    }

    post(uri, dados) {
        return this.requisicao("POST", uri, dados);
    }

    put(uri, id, dados) {
        return this.requisicao("PUT", uri + "/" + id, dados);
    }

    delete(uri, id) {
        return this.requisicao("DELETE", uri + "/" + id);
    }

    // Envia o arquivo como bytes em vez de converter para JSON.
    async enviarImagem(uri, arquivo) {
        const headers = { "Content-Type": arquivo.type };
        if (this.token) headers.Authorization = "Bearer " + this.token;

        let resposta;
        try {
            resposta = await fetch(uri, {
                method: "POST",
                headers,
                body: arquivo
            });
        } catch {
            throw new Error("Não foi possível conectar à API para enviar a imagem.");
        }

        const json = await resposta.json().catch(() => null);
        if (!resposta.ok || json?.success !== true) {
            throw new Error(json?.error?.message || json?.message || "Erro HTTP " + resposta.status);
        }
        return json;
    }
}
