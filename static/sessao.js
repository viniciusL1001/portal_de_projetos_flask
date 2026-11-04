// O login da API retorna data.token e data.user.usuario.
export function obterSessao() {
    try {
        const dados = JSON.parse(localStorage.getItem("userData"));
        const usuario = dados?.data?.user?.usuario;
        const token = dados?.data?.token;
        if (token && Number.isInteger(usuario?.idUsuario) && usuario.idUsuario > 0) {
            return { token: token, usuario: usuario };
        }
    } catch {
        // Sessão ausente ou inválida.
    }

    window.location.href = "Login.html";
    return null;
}

export function sair() {
    localStorage.removeItem("userData");
    window.location.href = "Login.html";
}

export function mostrarMensagem(elemento, mensagem, erro = false) {
    elemento.textContent = mensagem;
    elemento.className = "mensagem " + (erro ? "erro" : "sucesso");
}
