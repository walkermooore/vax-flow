from pytest import fixture, raises

from app import core, error, util


@fixture
def body():
    yield util.template_string(
        "new_account.html", {"nome_usuario": "jose", "link": "link"}
    )


def test_email_template_sucess():
    assert (
        type(
            util.template_string(
                "new_account.html", {"nome_usuario": "jose", "link": "link"}
            )
        )
        == str
    )


def test_send_email__sucess(body):
    assert util.send_email("email@example.com", "Testando", body) == None
