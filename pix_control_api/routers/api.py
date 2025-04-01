from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from services.comprovante_service import processar_comprovante
from middleware.auth import verify_token


# Criar router com autenticação
router = APIRouter(
    prefix="/api", tags=["extractors"], dependencies=[Depends(verify_token)]
)


# Rota para validar comprovante com transferências bancárias
@router.post("/validar-comprovante", summary="Validar comprovante")
async def validar_comprovante(
    file: UploadFile = File(...),
    from_number: int = Query(...),
    to_number: int = Query(...),
):
    try:
        # Lê o arquivo enviado
        content = await file.read()

        res = processar_comprovante(content, file, from_number, to_number)

        # Retorna o JSON com os dados do comprovante
        return {"response": res}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


# Rota para extrair transferencias recebidas em extrato
# @router.post("/extrair-transferencias", summary="Extrair transferencias dos extratos")
# async def extrair_transferencias(
#     corpx: Optional[UploadFile] = File(None),
#     itau: Optional[UploadFile] = File(None),
#     pinbank: Optional[UploadFile] = File(None),
#     bullbank: Optional[UploadFile] = File(None),
# ):
#     try:
#         banks = [
#             (BANCOS["CORPX"], corpx),
#             (BANCOS["ITAU"], itau),
#             (BANCOS["PINBANK"], pinbank),
#             (BANCOS["BULLBANK"], bullbank),
#         ]

#         for banco, extrato_file in banks:
#             if extrato_file and extrato_file.filename.split(".")[-1] not in [
#                 "xlsx",
#                 "pdf",
#             ]:
#                 raise Exception("Formato de arquivo não suportado")

#             if extrato_file:
#                 extrato_content = await extrato_file.read()
#                 res = await processar_extrato(extrato_file, extrato_content, banco)

#         return {"message": res}

#     except Exception as e:
#         error(f"Erro ao processar extrato: {str(traceback.format_exc())}")
#         raise HTTPException(status_code=400, detail=f"{str(e)}")
