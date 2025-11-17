# ==================== ENTRENAR MODELO MEJORADO ====================
import os

path = "machine/micro_llm"
dataset_filename = os.path.join(path, 'dataset_expandido.txt')

# Leer el archivo
training_texts = []
training_labels = []

with open(dataset_filename, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split('\t')
            if len(parts) == 2:
                label, text = parts
                training_labels.append(label)
                training_texts.append(text)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


# Vectorización mejorada
vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),  # Unigramas, bigramas y trigramas
    max_features=2000,
    min_df=2,  # Ignorar términos muy raros
    sublinear_tf=True  # Escala logarítmica para TF
)

X = vectorizer.fit_transform(training_texts)

# Modelo con regularización ajustada
clf = LogisticRegression(
    C=0.8,  # Menos regularización = más flexible
    max_iter=1000,
    class_weight='balanced'  # Balancear clases automáticamente
)

clf.fit(X, training_labels)

# Validación cruzada
cv_scores = cross_val_score(clf, X, training_labels, cv=5)
print(f"\n🎯 Accuracy promedio (CV): {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Guardar vectorizador y clasificador
import pickle

vectorizer_filename = os.path.join(path, "intent_vectorizer.pkl")
with open(vectorizer_filename, 'wb') as f:
    pickle.dump(vectorizer, f)

classifier_filename = os.path.join(path, "intent_classifier.pkl")
with open(classifier_filename, 'wb') as f:
    pickle.dump(clf, f)