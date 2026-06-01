import mimetypes
import os
import uuid
from enum import Enum

import magic
from fastapi import (APIRouter, BackgroundTasks, File, Form, Path, UploadFile,
                     responses)
from fastapi.responses import FileResponse

from app import core
from app.core import ApiError
from app.util.functions import save_file

router = APIRouter(prefix="/file", tags=["File"])


class FileType(str, Enum):
    Application = "application"
    Image = "image"
    Text = "text"
    Video = "video"
    Audio = "audio"


@router.post(
    "/",
    summary="Cria novo Arquivo",
    response_model=str,
)
async def create_file(
    file: UploadFile = File(...),
    type_data: FileType = Form(...),
) -> str:
    """
    Cria um novo arquivo.

    Args:
        file (UploadFile): O arquivo a ser enviado.
        type_data (FileType): O tipo de arquivo a ser salvo.

    Returns:
        str: O nome do arquivo salvo.

    Raises:
        HTTPException: Se ocorrer um erro durante o processo de criação do arquivo.

    """
    filename = await save_file(core.settings.UPLOAD_DIR, file, type_data.value)
    return filename


@router.post(
    "/start-recording",
    summary="Inicia nova gravação",
    operation_id="start_recording",
    response_model=dict,
)
async def start_recording(
    type_data: FileType = Form(FileType.Audio),  # Força ser áudio
) -> dict:
    """Inicia uma nova gravação criando um arquivo vazio"""
    try:
        # Cria arquivo vazio
        filename = str(uuid.uuid4()) + ".webm"

        filepath = os.path.join(core.settings.UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            pass  # Cria arquivo vazio

        return {"status": "recording_started", "filename": filename}
    except Exception as e:
        raise ApiError(status_code=500, detail=f"Erro ao iniciar gravação: {str(e)}")


@router.get(
    "/{filename}",
    summary="Visualizar Arquivo",
    response_class=responses.FileResponse,
)
def get_file_by_filename(filename: str = Path(..., description="nome do arquivo")):
    if os.path.exists(f"{core.settings.UPLOAD_DIR}{str(filename)}"):
        image = os.path.join(core.settings.UPLOAD_DIR, str(filename))

        def iterfile():
            with open(image, mode="rb") as file_like:
                yield from file_like

    else:
        raise ApiError(
            status_code=404,
            loc=["body", "filename"],
            msg=f"Arquivo não encontrado",
            type="value_error.auth",
        )

    return responses.StreamingResponse(
        iterfile(),
        media_type=magic.from_file(
            f"{core.settings.UPLOAD_DIR}{str(filename)}", mime=True
        ),
    )


@router.api_route(
    "/download/{filename}",
    summary="Download de Arquivo",
    response_class=FileResponse,
    methods=["GET", "HEAD"],
)
def download_file(filename: str = Path(..., description="nome do arquivo")):
    file_path = os.path.join(core.settings.UPLOAD_DIR, filename)

    if not os.path.isfile(file_path):
        raise ApiError(
            status_code=404,
            loc=["body", "filename"],
            msg="Arquivo não encontrado",
            type="value_error.auth",
        )

    # Detecta o tipo MIME do arquivo
    mime_type = magic.from_file(file_path, mime=True)

    # Obtém a extensão baseada no tipo MIME
    extension = mimetypes.guess_extension(mime_type) or ""

    # Se já tiver uma extensão (ex: filename.pdf), não adiciona de novo
    if not filename.lower().endswith(extension):
        filename_with_ext = f"{filename}{extension}"
    else:
        filename_with_ext = filename

    return FileResponse(
        path=file_path,
        filename=filename_with_ext,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename_with_ext}"',
            "Cache-Control": "no-cache",
        },
    )


@router.get(
    "/files/list/",
    summary="Listar todos os arquivos",
    response_model=list[str],
)
def list_all_files():
    try:
        # Lista todos os arquivos no diretório de upload
        files = os.listdir(core.settings.UPLOAD_DIR)

        # Filtra apenas arquivos (exclui diretórios)
        file_list = [
            f
            for f in files
            if os.path.isfile(os.path.join(core.settings.UPLOAD_DIR, f))
        ]

        return file_list
    except Exception as e:
        raise ApiError(
            status_code=500,
            loc=["server", "files"],
            msg=f"Erro ao listar arquivos: {str(e)}",
            type="server_error",
        )
