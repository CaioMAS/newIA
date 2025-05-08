from fastapi import APIRouter # type: ignore
from app.services.treinamento import treinar_modelo, prever_com_modelo

router = APIRouter()

@router.post("/train")
def treinar():
    acuracia = treinar_modelo()
    return {"status": "modelo treinado", "acuracia": acuracia}

@router.get("/sinal")
def obter_sinal():
    resultado = prever_com_modelo()
    return {"sinal": resultado}
