from pydantic import BaseModel
from typing import Literal, Optional

CATE = Literal['EAA', 'PE', 'CP', 'HLM', 'MAP', 'EHA', 'EHMA', 'CO', 'EMA', 'PLU', 'EAMA', 'HLG']

class Estacion(BaseModel):
    nom: str
    cate: CATE
    lat: float
    lon: float
    ico: Literal['M', 'H']
    cod: str
    cod_old: Optional[str] = ""
    estado: Literal['REAL', 'DIFERIDO', 'AUTOMATICA']