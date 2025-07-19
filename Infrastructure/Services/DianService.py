from datetime import date, datetime
import requests
from bs4 import BeautifulSoup
from typing import Optional
from Infrastructure.Dtos.TRMDto import TRMDto
from dotenv import load_dotenv
import os

load_dotenv()

class DianService:
    def __init__(self) -> None:
        self.base_url: str = os.getenv("DIAN_BASE_URL")
        
        base_date_str: str = os.getenv("DIAN_BASE_DATE")
        self.base_date = datetime.strptime(base_date_str, "%Y-%m-%d").date()
        
        self.base_id: int = int(os.getenv("DIAN_BASE_ID"))
    
    async def obtener_datos_trm(self, fecha: date) -> TRMDto:
        id_dian: int = self._calcular_id(fecha)
        while True:
            url = self.base_url.format(id_dian=id_dian)
            response = requests.get(url)
            
            if response.status_code != 200:
                raise ValueError(f"No se pudo acceder a la página con ID {id_dian}. Estado: {response.status_code}")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            fecha_expedicion = self._extraer_fecha(soup, "Fecha Expedición:")
            if fecha_expedicion != fecha:
                if fecha_expedicion < fecha:
                    id_dian += 1
                    continue
                else:
                    id_dian -= 1
                    continue
            desde = self._extraer_fecha(soup, "Desde:")
            hasta = self._extraer_fecha(soup, "Hasta:")
            
            dolar_americano = self._extraer_y_convertir_valor(soup, "Dólar Americano")
            reminbi_chino = self._extraer_y_convertir_valor(soup, "Reminbi Chino off shore")
            dolar_hong_kong = self._extraer_y_convertir_valor(soup, "Dólar de Hong Kong")
            break
            
        return TRMDto(
            fecha_alta = fecha_expedicion,
            fecha_inicio = desde,
            fecha_final = hasta,
            id_dian = id_dian,
            dolar = dolar_americano,
            dolar_hong_kong = dolar_hong_kong,
            reminbi = reminbi_chino
        )
    
    def _calcular_id(self, fecha : date) -> int:
        delta_dias = (fecha - self.base_date).days
        numero_semanas = delta_dias // 7
        
        id_calculado = self.base_id + numero_semanas
        
        if id_calculado < 1:
            raise ValueError(f"ID calculado ({id_calculado}) no puede ser menor a 1. La fecha está demasiado lejos en el pasado.")
            
        return id_calculado
    
    def _find_element_by_text_case_insensitive(self, soup: BeautifulSoup, tag: str, text: str):
        elements = soup.find_all(tag, string=lambda s: s and text.lower() in str(s).lower())
        return elements[0] if elements else None

    def _extraer_fecha(self, soup: BeautifulSoup, label_text: str) -> str:
        label = self._find_element_by_text_case_insensitive(soup, 'label', label_text)
        if not label:
            raise ValueError(f"No se encontró la etiqueta: {label_text}")
            
        value_div = label.find_next_sibling('div', class_='form-control-static')
        if not value_div:
            raise ValueError(f"No se encontró el valor para: {label_text}")
            
        date_str = value_div.get_text(strip=True)
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    
    def _extraer_y_convertir_valor(self, soup: BeautifulSoup, moneda_nombre: str) -> float:
        valor_str = self._extraer_valor_moneda(soup, moneda_nombre)
        if valor_str is None:
            raise ValueError(f"No se encontró el valor para la moneda: {moneda_nombre}")
        
        clean_valor = valor_str.replace('$', '').replace('U$', '').replace(',', '.').strip()
        
        try:
            return float(clean_valor)
        except ValueError as e:
            raise ValueError(f"Valor '{clean_valor}' no convertible a float para la moneda: {moneda_nombre}") from e
    
    def _extraer_valor_moneda(self, soup: BeautifulSoup, moneda_nombre: str) -> Optional[str]:
        currency_td = self._find_element_by_text_case_insensitive(soup, 'td', moneda_nombre)
        
        if currency_td:
            value_td = currency_td.find_next_sibling('td')
            if value_td:
                value_span = value_td.find('span', class_='dollarValue')
                if not value_span:
                    value_span = value_td.find('span', class_='currencyValue')
                
                if value_span:
                    return value_span.get_text(strip=True)
        
        return None