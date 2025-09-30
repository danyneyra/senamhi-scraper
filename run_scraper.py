"""
Script de ejemplo mostrando cómo usar el nuevo sistema de scraping modular.

Este script permite:
1. Consulta por mes específico (Month mode)
2. Consulta por año completo (Year mode) 
3. Consulta por periodo de años (Period mode)

Cada modo permite guardar archivos individuales o consolidados.
"""

import asyncio
from main import main

def show_usage_examples():
    """Muestra ejemplos de uso del sistema"""
    print("🔍 EJEMPLOS DE USO DEL SISTEMA DE SCRAPING")
    print("=" * 60)
    print("🔍 INGRESE EL CÓDIGO DE LA ESTACIÓN:")
    print("   - Puedes encontrar los códigos en el archivo 'data/estaciones.json'")
    print("Código (ejemplo: 472D30C8): 472D30C8")

    print("📅 MODO MONTH (Mes específico):")
    print("   - Descarga datos de un año y mes específico")
    print("   - Ejemplo: 2024, mes 09 → TICAPAMPA-202409.csv")
    print()
    
    print("📅 MODO YEAR (Año completo):")
    print("   - Descarga todos los meses de un año")
    print("   - Opción de archivos individuales o consolidado")
    print("   - Ejemplo: 2024 → 12 archivos individuales o TICAPAMPA-2024.csv")
    print()
    
    print("📅 MODO PERIOD (Periodo de años):")
    print("   - Descarga datos de múltiples años")
    print("   - Opción de archivos individuales o consolidado")
    print("   - Ejemplo: 2020-2025 → múltiples archivos o TICAPAMPA-2020-2025.csv")
    print()
    
    print("💾 OPCIONES DE GUARDADO:")
    print("   - Individual: Un archivo CSV por cada mes")
    print("   - Consolidado: Todos los datos en un solo archivo con columna de periodo")
    print()
    
    print("📁 ESTRUCTURA DE ARCHIVOS GENERADOS:")
    print("   output/")
    print("   ├── TICAPAMPA-202409.csv       (modo month)")
    print("   ├── TICAPAMPA-2024.csv         (modo year consolidado)")
    print("   ├── TICAPAMPA-2020-2025.csv    (modo period consolidado)")
    print("   └── TICAPAMPA-202401.csv       (archivos individuales)")
    print("       TICAPAMPA-202402.csv")
    print("       ...")
    print()

def run_interactive_example():
    """Ejecuta el sistema de manera interactiva"""
    show_usage_examples()
    
    print("🚀 INICIANDO SCRAPER INTERACTIVO")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    run_interactive_example()