# TFM – Modelo de Riesgo de Crédito y Scorecard  

Este repositorio contiene el código, datos y resultados finales desarrollados para mi **Trabajo de Fin de Máster en Big Data, Data Science e Inteligencia Artificial (UCM)**.  
El proyecto aborda la **detección de malos pagadores** mediante modelos de Machine Learning y la elaboración de una **Scorecard crediticia** basada en técnicas de *Credit Scoring*.

---

## Descripción del proyecto
El objetivo del trabajo es construir un sistema de evaluación crediticia capaz de:

- Identificar clientes con alta probabilidad de impago (*bad payers*).
- Estimar la calidad crediticia mediante una **scorecard interpretable**.
- Comparar modelos de clasificación bajo métricas orientadas a riesgo.
- Implementar una **aplicación gráfica** que permita calcular la puntuación crediticia de nuevos solicitantes.

Para ello se ha trabajado con un dataset real de comportamiento crediticio (`hmeq.csv`), se ha aplicado preprocesamiento, selección de variables, WOE/IV, modelos logísticos y construcción final de una tarjeta de puntuación.

---

## Contenido del repositorio

### **1. `Anexo_TFM_OscarYanez.ipynb`**
Notebook principal del proyecto. Incluye:
- Exploración y limpieza del dataset.
- Construcción y comparación de distintos modelos. 
- Análisis de variables y WOE/IV.  
- Entrenamiento del modelo de regresión logística.  
- Construcción de la scorecard.  
- Evaluación del rendimiento del modelo.

---

### **2. `Anexo2_Aplicación_Calculadora_calidad_crediticia.py`**
Script Python que implementa una **aplicación gráfica** para calcular la calidad crediticia de un solicitante.  
La aplicación permite introducir las variables relevantes y obtener:  
- Score final  
- Probabilidad estimada de impago  
- Categoría de riesgo  

---

### **3. `hmeq.csv`**
Dataset original utilizado en el proyecto.  
Incluye información histórica de operaciones crediticias y variables relevantes para el análisis de riesgo.

---

### **4. `scorecard_table.xlsx`**
Scorecard final generada a partir del modelo logístico.  
Se incluye como referencia práctica para su uso en entornos analíticos o didácticos.
