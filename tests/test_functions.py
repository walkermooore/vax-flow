import os

from fastapi import UploadFile
from pytest import fixture, mark, raises

from app import error, util


@fixture
def header():
    yield ["c1", "c2", "c3"]


@fixture
def data():
    yield [["l1c1", "l2c2", "l1c3"], ["l2c1", "l2c2", "l3c3"]]


@fixture
def path():
    yield "./app/uploads/"


@fixture
def filename(header, data):
    yield util.save_csv_file("./app/uploads/", header, data)


@mark.asyncio
async def test_save_file_deve_retornar_http_exception(path):
    with open(os.path.join("tests/file_test", "video.mp4"), "rb") as f:
        upload_file = UploadFile(file=f)
        with raises(error.CustomHTTPException) as e:
            filename = await util.save_file("path", upload_file, "video")
        assert e.value.detail == "Arquivo ou diretorio não encontrado"


def test_save_csv_file_deve_retornar_nome_do_arquivo_str(path, header, data):
    filename = util.save_csv_file(path, header, data)
    assert type(filename) == str


def test_save_csv_file_mensagem_diretorio_nao_encontrado_str(header, data):
    path = "./aapp/uploads/"
    with raises(error.CustomHTTPException) as e:
        util.save_csv_file(path, header, data)
    assert e.value.detail == "Arquivo ou diretorio não encontrado"


def test_delete_file_deve_retornar_true(path, filename):
    response = util.delete_file(path, filename)
    assert response == True


def test_delete_file_erro_diretorio_nao_encontrado_str(header, data):
    path = "./aapp/uploads/"
    with raises(error.CustomHTTPException) as e:
        util.delete_file(path, filename)
    assert e.value.detail == "Arquivo ou diretorio não encontrado"


def test_generate_cpf_deve_retornar_um_cpf_valido_com_11_digitos():
    cpf = util.generate_cpf()
    assert len(cpf) == 11
