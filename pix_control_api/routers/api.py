from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from apscheduler.schedulers.background import BackgroundScheduler
from services.transferencia_service import processar_transferencias
from services.comprovante_service import processar_comprovante
from middleware.auth import verify_token


# Criar router com autenticação
# router = APIRouter(
#     prefix="/api", tags=["extractors"], dependencies=[Depends(verify_token)]
# )


scheduler = BackgroundScheduler()

# Agenda para rodar a cada minuto (como um cron)
scheduler.add_job(processar_transferencias, 'cron', minute='*')
scheduler.start()

router = APIRouter(prefix="/api", tags=["extractors"])


# Rota para validar comprovante com transferências bancárias
@router.post("/validar-comprovante", summary="Validar comprovante")
async def validar_comprovante(
    file: UploadFile = File(...),
    author_number: str = Query(...),
    from_number: str = Query(...),
    to_number: str = Query(...),
    is_group_msg: int = Query(...),
    timestamp: int = Query(...),
    from_me: int = Query(...),
):
    try:
        # Lê o arquivo enviado
        content = await file.read()

        # Define a menssagem
        message = {
            "from_number": from_number,
            "to_number": to_number,
            "author_number": author_number,
            "is_group_msg": is_group_msg,
            "timestamp": timestamp,
            "from_me": from_me,
        }

        # Processa o comprovante
        res = processar_comprovante(content, file, message)

        # Retorna o JSON com os dados do comprovante
        return {"response": res}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


# Rota para extrair transferencias bancárias
@router.get("/extrair-transferencias", summary="Extrair transferências")
async def validar_comprovante():
    try:
        # Retorna o JSON com os dados do comprovante
        return processar_transferencias()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")
