from integrations.directus_api import DirectusAPI


# Classe para manipular funcionarios na API do Directus
class TransferenciaAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def get_by_id_bullbank(self, id_bullbank):
        try:
            transferencias = self.directus_api.get_directus(
                endpoint="/items/transferencias",
                params={"filter[id_bullbank]": id_bullbank},
            )["data"]

            return transferencias

        except Exception as e:
            raise Exception(f"{str(e)}")

    def get_all(self):
        try:
            transferencias = self.directus_api.get_directus(
                endpoint="/items/transferencias"
            )["data"]

            return transferencias

        except Exception as e:
            raise Exception(f"{str(e)}")

    def create(self, transferencias):
        try:
            transferencia = self.directus_api.post_directus(
                endpoint="/items/transferencias",
                json_data=transferencias,
            )

            return transferencia

        except Exception as e:
            raise Exception(f"{str(e)}")

    def update(self, id, transferencia):
        try:
            transferencia = self.directus_api.patch_directus(
                endpoint=f"/items/transferencias/{id}",
                json_data=transferencia,
            )

            return transferencia

        except Exception as e:
            raise Exception(f"{str(e)}")
