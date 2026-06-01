from fastapi import HTTPException
from pytest import fixture, raises

from app import error, util


@fixture
def cpf():
    yield "63924271046"


@fixture
def cnpj():
    yield "73951435000195"


@fixture
def string():
    yield "string"


def test_cpf_validate_tamanho_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cpf("121435")

        assert (
            e.value.detail
            == "CPF invalido, O campo deve conter exatamente 11 digitos numericos"
        )


def test_cpf_validate_opcional_nulo():
    """
    Tests the CPF validation function with a None value.

    Verifies that the function correctly handles the absence of a CPF value.

    Parameters:
    None

    Returns:
    None
    """
    assert util.validate_cpf(None) == None


def test_cpf_validate_cpf_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cpf("99999999999")
    assert e.value.detail == "CPF invalido"


def test_cpf_validate_cpf_valido():
    cpf = util.generate_cpf()
    assert util.validate_cpf(cpf) == cpf


def test_cnpj_validate_tamanho_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cnpj("1111111")
    assert (
        e.value.detail
        == "CNPJ invalido, O campo deve conter exatamente 14 digitos numericos"
    )


def test_cnpj_validate_opcional_nulo():
    assert util.validate_cnpj(None) == None


def test_cnpj_validate_cnpj_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cnpj("99999999999999")
    assert e.value.detail == "CNPJ invalido"


def test_cnpj_validate_cnpj_valido():
    cnpj = "73951435000195"
    assert util.validate_cnpj(cnpj) == cnpj


def test_cpf_cnpj_validate_tamanho_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cnpj_cpf("121435")
    assert e.value.detail == "Deve conter um CPF ou CNPJ valido"


def test_cnpj_cpf_validate_opcional_nulo():
    assert util.validate_cnpj_cpf(None) == None


def test_cnpj_cpf_validate_cnpj_invalido():
    with raises(error.CustomHTTPException) as e:
        util.validate_cnpj_cpf("99999999999999")
    assert e.value.detail == "CNPJ invalido"


def test_cnpj_cpf_validate_cnpj_valido(cnpj):
    assert util.validate_cnpj_cpf(cnpj) == cnpj


def test_cnpj_cpf_validate_cpf_valido(cpf):
    assert util.validate_cnpj_cpf(cpf) == cpf


def test_normalize_capitalize_optional():
    assert util.normalize_capitalize(None) == None


def test_normalize_capitalize_sucesso(string):
    assert util.normalize_capitalize(string) == string.capitalize()


def test_normalize_uper_optional():
    assert util.normalize_uper(None) == None


def test_normalize_uper_sucesso(string):
    assert util.normalize_uper(string) == string.upper()


def test_normalize_lower_optional():
    assert util.normalize_lower(None) == None


def test_normalize_lower_sucesso(string):
    assert util.normalize_lower(string) == string.lower()


def test_normalize_password_optional():
    assert util.normalize_password(None) == None


def test_normalize_password_sucesso(string):
    assert type(util.normalize_password(string)) == bytes


def test_normalize_telefone_optional():
    assert util.normalize_phone(None) == None


def test_normalize_telefone_sucesso():
    fone = "9999999999999"
    assert util.normalize_phone(fone) == fone


def test_normalize_telefone_tamanho_invalido():
    with raises(error.CustomHTTPException) as e:
        util.normalize_phone("9999999")
    assert (
        e.value.detail
        == "Formato de telefone invalido, deve conter no minimo 11 e no maximo 13 digitos"
    )


def test_normalize_email_optional():
    assert util.normalize_email(None) == None


def test_normalize_email_sucesso():
    assert util.normalize_email("decayi1181@hrisland.com") == "decayi1181@hrisland.com"


def test_normalize_email_email_invalido():
    with raises(HTTPException) as e:
        util.normalize_email("exampleexmple")
    assert e.value.detail == "Formato de email invalido"
