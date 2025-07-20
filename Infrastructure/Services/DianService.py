from datetime import date, datetime, timedelta
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from Infrastructure.Dtos.TRMDto import TRMDto
from dotenv import load_dotenv
import os
import unicodedata

load_dotenv()

class DianService:
    def __init__(self) -> None:
        self.base_url: str = os.getenv("DIAN_BASE_URL")
        base_date_str: str = os.getenv("DIAN_BASE_DATE")
        self.base_date = datetime.strptime(base_date_str, "%Y-%m-%d").date()
        self.base_id: int = int(os.getenv("DIAN_BASE_ID"))
    
    async def obtener_datos_trm(self, fecha: date) -> TRMDto:
        id_dian: int = self._calcular_id(fecha)
        attempt_count = 0
        max_attempts_without_finding_date = 5
        
        while True:
            soup = self._get_page_soup(id_dian)
            fecha_expedicion = self._extract_date_from_label(soup, "Fecha Expedición:")
            # Imprimir fecha y ID DIAN para depuración
            
            if fecha_expedicion is None:
                attempt_count += 1
                if attempt_count % 2 == 1:
                    id_dian -= 1
                else:
                    id_dian += 2
                if attempt_count > max_attempts_without_finding_date:
                    raise ValueError(f"No se pudo encontrar una TRM válida después de múltiples intentos para la fecha {fecha}. Último ID DIAN probado: {id_dian}")
                continue
            
            if fecha_expedicion == fecha:
                break 
            
            if fecha_expedicion < fecha and self._esta_en_misma_semana(fecha_expedicion, fecha):
                break 
            
            if fecha_expedicion < fecha:
                id_dian += 1
            else:
                id_dian -= 1
            
            attempt_count = 0 
            continue 

        desde = self._extract_date_from_label(soup, "Desde:")
        hasta = self._extract_date_from_label(soup, "Hasta:")
        dolar_americano = self._extract_specific_currency_value(soup, "Dólar Americano")
        otras_cotizaciones_dict = self._extract_all_other_currencies_from_table(soup)
        
        return TRMDto(
            fecha_alta = fecha_expedicion,
            fecha_inicio = desde,
            fecha_final = hasta,
            id_dian = id_dian,
            dolar = dolar_americano,
            otras_cotizaciones = otras_cotizaciones_dict
        )
    
    def _calcular_id(self, fecha : date) -> int:
        delta_dias = (fecha - self.base_date).days
        numero_semanas = delta_dias // 7
        id_calculado = self.base_id + numero_semanas
        if id_calculado < 1:
            raise ValueError(f"ID calculado ({id_calculado}) no puede ser menor a 1. La fecha está demasiado lejos en el pasado.")
        return id_calculado

    def _get_page_soup(self, id_dian: int) -> BeautifulSoup:
        url = self.base_url.format(id_dian=id_dian)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"No se pudo acceder a la página con ID {id_dian}. Estado: {response.status_code}")
        return BeautifulSoup(response.content, 'html.parser')
    
    def _extract_date_from_label(self, soup: BeautifulSoup, label_text: str) -> Optional[date]:
        label = self._find_element_by_text_case_insensitive(soup, 'label', label_text)
        if not label:
            return None
        value_div = label.find_next_sibling('div', class_='form-control-static')
        if not value_div:
            return None 
        date_str = value_div.get_text(strip=True)
        if not date_str: 
            return None
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return None 

    def _extract_specific_currency_value(self, soup: BeautifulSoup, currency_name: str) -> float:
        value_str = self._extract_currency_string_value(soup, currency_name)
        if value_str is None:
            raise ValueError(f"No se encontró el valor para la moneda: {currency_name}")
        return self._parse_currency_value_string(value_str)
    
    def _extract_currency_string_value(self, soup: BeautifulSoup, currency_name: str) -> Optional[str]:
        currency_td = self._find_element_by_text_case_insensitive(soup, 'td', currency_name)
        if currency_td:
            value_td = currency_td.find_next_sibling('td')
            if value_td:
                value_span = value_td.find('span', class_='dollarValue')
                if not value_span:
                    value_span = value_td.find('span', class_='currencyValue')
                if value_span:
                    return value_span.get_text(strip=True)
        return None

    def _extract_all_other_currencies_from_table(self, soup: BeautifulSoup) -> Dict[str, Any]:
        otras_cotizaciones_dict: Dict[str, Any] = {}
        countries_table = soup.find('table', id='countries')
        if countries_table:
            for row in countries_table.find('tbody').find_all('tr'):
                currency_name_td = row.find('td', class_='col-sm-6')
                currency_value_td = currency_name_td.find_next_sibling('td')
                if currency_name_td and currency_value_td:
                    currency_name = currency_name_td.get_text(strip=True)
                    value_span = currency_value_td.find('span', class_='currencyValue')
                    if value_span:
                        raw_value_str = value_span.get_text(strip=True)
                        cleaned_key = self._clean_currency_name_to_key(currency_name)
                        try:
                            value = self._parse_currency_value_string(raw_value_str)
                            otras_cotizaciones_dict[cleaned_key] = value
                        except ValueError:
                            pass
        return otras_cotizaciones_dict

    def _parse_currency_value_string(self, value_str: str) -> float:
        clean_valor = value_str.replace('$', '').replace('U$', '').replace(',', '.').strip()
        try:
            return float(clean_valor)
        except ValueError as e:
            raise ValueError(f"Valor '{clean_valor}' no convertible a float.") from e

    def _clean_currency_name_to_key(self, name: str) -> str:
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        name = name.lower()
        name = name.replace(" ", "_").replace("-", "_")
        clean_name = "".join(c for c in name if c.isalnum() or c == '_')
        clean_name = '_'.join(filter(None, clean_name.split('_'))) 
        return clean_name
    
    def _find_element_by_text_case_insensitive(self, soup: BeautifulSoup, tag: str, text: str):
        elements = soup.find_all(tag, string=lambda s: s and text.lower() in str(s).lower())
        return elements[0] if elements else None
    
    def _esta_en_misma_semana(self, fecha1: date, fecha2: date) -> bool:
        inicio_semana1 = fecha1 - timedelta(days=fecha1.weekday())
        inicio_semana2 = fecha2 - timedelta(days=fecha2.weekday())
        return inicio_semana1 == inicio_semana2
