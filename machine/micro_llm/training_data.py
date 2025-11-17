import random
import re
from typing import List, Tuple

# Dataset original
pedido_texts = [
    "quiero pedir", "voy a ordenar", "mostrame el menú", "quiero un postre",
    "necesito hacer un pedido", "me das una hamburguesa?", "qué opciones tenés?",
    "quiero pedir algo", "me gustaría pedir", "tenés algo con chocolate?",
    "me das la carta?", "me mostrás el menú?", "qué recomiendan?",
    "qué tienen hoy?", "me das una bebida?", "puedo pedir ahora?",
]

cuenta_texts = [
    "la cuenta por favor", "necesito el recibo", "la factura",
    "voy a ir pidiendo la cuenta", "quiero pagar", "me cobrás?",
    "pasame la cuenta", "cuánto te debo?", "queremos pagar", "cobranos",
]

esperar_texts = [
    "no gracias", "por ahora no necesito nada", "ahora no", "te agradezco",
    "no hace falta", "esperame un minuto", "dame un momento", "todavía no",
    "estoy viendo", "más tarde", "en un rato", "dejame pensar",
]

queja_texts = [
    "no es lo que pedí", "la comida está fría", "está feo",
    "me trajiste cualquier cosa", "quiero hablar con el gerente",
    "esto es un desastre", "tardan mucho", "no me gusta", "es una mierda",
    "que caca", "que garcha"
]

# ==================== TÉCNICAS DE EXPANSIÓN ====================

# 1. VARIACIONES ORTOGRÁFICAS Y DE PUNTUACIÓN
def add_orthographic_variations(texts: List[str]) -> List[str]:
    """Agrega variaciones con/sin tildes, mayúsculas, signos"""
    variations = []
    for text in texts:
        # Original
        variations.append(text)
        
        # Sin tildes
        no_accent = text.replace('á', 'a').replace('é', 'e').replace('í', 'i')
        no_accent = no_accent.replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
        variations.append(no_accent)
        
        # Todo minúsculas sin signos
        variations.append(re.sub(r'[¿?!¡]', '', text.lower()))
        
        # Con signos de exclamación
        if not text.endswith(('?', '!')):
            variations.append(text + '!')
    
    return list(set(variations))

# 2. COMBINACIONES CON PALABRAS COMUNES
def add_common_prefixes_suffixes(texts: List[str]) -> List[str]:
    """Agrega prefijos/sufijos comunes del habla coloquial"""
    prefixes = ["che", "ey", "disculpá", "perdón", "una pregunta", "hola", ""]
    suffixes = ["por favor", "porfa", "dale", "ya", "ahora", ""]
    
    expanded = list(texts)
    for text in texts[:10]:  # Solo expandir algunos para no explotar el dataset
        for pre in random.sample(prefixes, 3):
            for suf in random.sample(suffixes, 2):
                if pre or suf:
                    new_text = f"{pre} {text} {suf}".strip()
                    new_text = re.sub(r'\s+', ' ', new_text)  # Limpiar espacios
                    expanded.append(new_text)
    
    return expanded

# 3. SINÓNIMOS Y VARIACIONES LÉXICAS
def add_synonym_variations(texts: List[str], intent: str) -> List[str]:
    """Reemplaza palabras clave con sinónimos"""
    synonyms = {
        "pedido": {
            "quiero": ["necesito", "quisiera", "me das", "dame", "podés traerme"],
            "pedir": ["ordenar", "llevar", "pedir", "encargar"],
            "menú": ["carta", "opciones", "platos", "comidas"],
        },
        "cuenta": {
            "cuenta": ["factura", "ticket", "recibo", "comprobante"],
            "pagar": ["abonar", "cobrar", "cancelar"],
            "cobrás": ["cobrás", "me cobrás", "pasás la cuenta"],
        },
        "esperar": {
            "momento": ["minuto", "segundo", "rato", "toque"],
            "esperar": ["aguantar", "dame tiempo", "todavía no"],
        },
        "queja": {
            "fría": ["helada", "congelada", "sin calentar"],
            "feo": ["horrible", "malo", "terrible", "desastre"],
            "tardaron": ["demoran", "tardan mucho", "muy lento"],
        }
    }
    
    expanded = list(texts)
    if intent in synonyms:
        for text in texts[:15]:
            for word, syns in synonyms[intent].items():
                if word in text.lower():
                    for syn in syns:
                        new_text = text.lower().replace(word, syn)
                        expanded.append(new_text)
    
    return expanded

# 4. ERRORES TIPOGRÁFICOS COMUNES
def add_typos(texts: List[str], num_typos: int = 3) -> List[str]:
    """Simula errores de tipeo comunes en celular"""
    expanded = list(texts)
    typo_map = {
        'q': ['que', 'k'], 'k': ['q', 'que'], 
        'x': ['por'], 'xq': ['porque', 'por que'],
        'tb': ['también'], 'tmb': ['también'],
    }
    
    for text in random.sample(texts, min(num_typos, len(texts))):
        for orig, replacements in typo_map.items():
            for repl in replacements:
                if repl in text:
                    expanded.append(text.replace(repl, orig))
    
    return expanded

# 5. COMBINACIONES INTRA-CATEGORÍA
def add_combinations(texts: List[str], num_combos: int = 10) -> List[str]:
    """Combina dos frases de la misma categoría"""
    expanded = list(texts)
    for _ in range(num_combos):
        if len(texts) >= 2:
            t1, t2 = random.sample(texts, 2)
            # Eliminar signos finales antes de combinar
            t1 = re.sub(r'[?!]+$', '', t1)
            t2 = re.sub(r'[?!]+$', '', t2)
            combined = f"{t1} y {t2}"
            expanded.append(combined)
    
    return expanded

# ==================== APLICAR EXPANSIONES ====================

def expand_dataset(texts: List[str], label: str, aggressive: bool = False) -> Tuple[List[str], List[str]]:
    """Aplica todas las técnicas de expansión"""
    expanded = texts.copy()
    
    # Aplicar técnicas
    expanded = add_orthographic_variations(expanded)
    expanded = add_common_prefixes_suffixes(expanded)
    expanded = add_synonym_variations(expanded, label)
    expanded = add_typos(expanded)
    
    if aggressive:
        expanded = add_combinations(expanded, num_combos=20)
    
    # Eliminar duplicados
    expanded = list(set(expanded))
    
    labels = [label] * len(expanded)
    return expanded, labels


# ==================== EXPANSIÓN COMPLETA ====================

print("📊 EXPANDIENDO DATASET...")
print(f"Dataset original: {len(pedido_texts + cuenta_texts + esperar_texts + queja_texts)} ejemplos\n")

# Expandir cada categoría
pedido_exp, pedido_labels = expand_dataset(pedido_texts, "pedido", aggressive=True)
cuenta_exp, cuenta_labels = expand_dataset(cuenta_texts, "cuenta", aggressive=True)
esperar_exp, esperar_labels = expand_dataset(esperar_texts, "esperar", aggressive=False)
queja_exp, queja_labels = expand_dataset(queja_texts, "queja", aggressive=True)

print(f"✅ Pedido:  {len(pedido_texts):3d} → {len(pedido_exp):4d} (+{len(pedido_exp)-len(pedido_texts)})")
print(f"✅ Cuenta:  {len(cuenta_texts):3d} → {len(cuenta_exp):4d} (+{len(cuenta_exp)-len(cuenta_texts)})")
print(f"✅ Esperar: {len(esperar_texts):3d} → {len(esperar_exp):4d} (+{len(esperar_exp)-len(esperar_texts)})")
print(f"✅ Queja:   {len(queja_texts):3d} → {len(queja_exp):4d} (+{len(queja_exp)-len(queja_texts)})")

# Combinar todo
all_texts = pedido_exp + cuenta_exp + esperar_exp + queja_exp
all_labels = pedido_labels + cuenta_labels + esperar_labels + queja_labels

print(f"\n📈 Dataset expandido total: {len(all_texts)} ejemplos")

# ==================== EXPORTAR DATASET ====================
import os

path = "machine/micro_llm"
dataset_filename = os.path.join(path, 'dataset_expandido.txt')

print("\n💾 Guardando dataset expandido...")
with open(dataset_filename, 'w', encoding='utf-8') as f:
    for text, label in zip(all_texts, all_labels):
        f.write(f"{label}\t{text}\n")

print("✅ Guardado en 'dataset_expandido.txt'")