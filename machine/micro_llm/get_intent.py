# ==================== FUNCIÓN MEJORADA ====================
import numpy

def get_intent(msg: str, vectorizer, clf, threshold=0.45) -> str:
    """Predice intención con threshold ajustado"""
    X_pred = vectorizer.transform([msg.lower()])
    probs = clf.predict_proba(X_pred)[0]
    max_prob = numpy.max(probs)
    label = clf.classes_[numpy.argmax(probs)]
    
    if max_prob < threshold:
        return "desconocido"
    
    return label

# ==================== PRUEBAS ====================

# print("\n🧪 PROBANDO MODELO EXPANDIDO:")
# print("-" * 50)

# test_cases = [
#     ("hola, quiero pedir una pizza", "pedido"),
#     ("me das la carta? quiero ver opciones", "pedido"),
#     ("tenes algo con chocolate?", "pedido"),
#     ("che, me cobras?", "cuenta"),
#     ("cuanto te debo?", "cuenta"),
#     ("quiero pagar ya mismo", "cuenta"),
#     ("por ahora no, gracias", "esperar"),
#     ("esperame un segundo", "esperar"),
#     ("todavia no quiero nada", "esperar"),
#     ("esto esta horrible", "queja"),
#     ("la comida vino fria", "queja"),
#     ("me trajeron cualquier cosa", "queja"),
#     ("q onda tenes menu", "pedido"),  # Con typo
#     ("xfa pasame la cuenta", "cuenta"),  # Con abreviatura
#     ("ey mostrame q tienen", "pedido"),  # Coloquial
# ]

# import pickle
# import os

# path = "machine/micro_llm"

# vectorizer_filename = os.path.join(path, "intent_vectorizer.pkl")
# with open(vectorizer_filename, 'rb') as f:
#     vectorizer = pickle.load(f)
    
# classifier_filename = os.path.join(path, "intent_classifier.pkl")
# with open(classifier_filename, 'rb') as f:
#     clf = pickle.load(f)

# correct = 0
# for text, expected in test_cases:
#     predicted = get_intent(text, vectorizer, clf)
#     is_correct = predicted == expected
#     correct += is_correct
#     icon = "✅" if is_correct else "❌"
#     print(f"{icon} '{text}' → {predicted} (esperado: {expected})")

# print(f"\n📊 Exactitud en pruebas: {correct}/{len(test_cases)} ({100*correct/len(test_cases):.1f}%)")

