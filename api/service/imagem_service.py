from pathlib import Path
from uuid import uuid4
from api.utils.error_response import ErrorResponse


class ImagemService:
    def salvar(self, conteudo, tipo):
        if not conteudo:
            raise ErrorResponse(400, "Imagem inválida.")
        if len(conteudo) > 2 * 1024 * 1024:
            raise ErrorResponse(413, "Imagem muito grande.", {"message": "O tamanho máximo é 2 MB."})
        tipo = (tipo or "").split(";")[0].strip().lower()
        png = conteudo.startswith(bytes((137, 80, 78, 71, 13, 10, 26, 10)))
        jpg = conteudo.startswith(bytes((255, 216, 255)))
        if png and tipo == "image/png":
            extensao = "png"
        elif jpg and tipo == "image/jpeg":
            extensao = "jpg"
        else:
            raise ErrorResponse(400, "Formato de imagem inválido.", {"message": "Envie PNG ou JPG."})

        pasta = Path(__file__).resolve().parents[2] / "static" / "uploads"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = f"{uuid4()}.{extensao}"
        with (pasta / nome).open("xb") as arquivo:
            arquivo.write(conteudo)
        return "/uploads/" + nome
