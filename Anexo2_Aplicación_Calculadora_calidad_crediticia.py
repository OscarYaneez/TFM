import pandas as pd
import numpy as np
import joblib
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tmsg
from PIL import Image, ImageTk
import os
import optbinning

# Importamos nuestra scorecard
scorecard = joblib.load(os.getcwd() + r'\scorecard.pkl')
file_path = ''

# Función para seleccionar el documento a importar
def upload(): 
    global file_path
    document_label_text.set('Ningún documento seleccionado')
    document_uploaded_label.config(fg='red')

    file_path = filedialog.askopenfilename(
        initialdir='/Escritorio',
        title='Selecciona un archivo',
        filetypes=(
            ('Archivos csv', '*.csv'),
            ('Archivos Excel', '*.xlsx')
        )
    )
    
    if file_path == '':
        tmsg.showwarning(
            'Alerta!',
            'Por favor selecciona un documento para importar.'
        )
        return

    document_label_text.set('Documento importado correctamente')
    document_uploaded_label.config(fg='#30C657')
    
    return

# Función para preprocesar los nuevos datos de manera que sean usables
# para nuestra scorecard
def preprocess(data):
    data = data.replace('', pd.NA)

    data['JOB'] = data['JOB'].replace('Sales', 'Other')

    data['MVR'] = data['MORTDUE'] / data['VALUE']
    data.drop(columns='MORTDUE', inplace=True)

    log_var = ['LOAN', 'VALUE', 'YOJ']
    for var in log_var:
        data[var] = np.log1p(data[var])
        data = data.rename(columns={var : f'{var}_log'})
    return data

# Función para aplicar la decisión de negocio según el score
def decision(score, threshold_approve=578.509, threshold_review=537.425):
    if score >= threshold_approve:
        return 'Aceptado'
    elif score >= threshold_review:
        return 'A revisar'
    else:
        return 'Rechazado'

# Función para guardar los resultados en un Excel
def save(data):
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Guardar resultados como...",
        initialfile='Resultados_scoring'
    )

    if save_path == '':
        tmsg.showwarning(
            'Alerta!',
            'Por favor selecciona una ubicación de guardado.'
        )
        return
    
    data.to_excel(save_path, index=False)
    return

# Función para calcular el score de los clientes importados
def predict():
    global file_path
    try:
        if file_path == '':
            tmsg.showerror(
                'Alerta!',
                'Ningún documento seleccionado.'
            )
            return
        elif file_path.endswith('csv'):
            df_new = pd.read_csv(file_path)
        else:
            df_new = pd.read_excel(file_path)
    except:
        tmsg.showerror(
            'Alerta!',
            'El documento puede estar corrupto o tener algún problema.'
        )

    try:
        # Preprocesar nuevos datos
        df_processed = preprocess(df_new)
        # Calcular los scores de cada cliente
        scores = scorecard.score(df_processed)
         # Crear dataframe con los resultados
        df_results = df_new.copy()
        df_results["Score"] = scores
        df_results["Decisión"] = df_results["Score"].apply(decision)
        
        # Guardar resultados en un Excel a parte
        save(df_results)
        tmsg.showinfo('', 'Archivo guardado correctamente.')
        document_label_text.set('Ningún documento seleccionado')
        document_uploaded_label.config(fg='red')
        file_path = ''
    except:
        tmsg.showerror(
            'Error!',
            'Ha ocurrido un error al procesar los datos importados.'
        )

    return

def open_window(title, message):
    window = Toplevel(root)
    window.title(title)
    window.geometry('600x100')
    window.resizable(False, False)

    Label(window, text=message, justify=LEFT, pady=10).pack()

def open_tutorial():
    open_window(
        'Qué hace el programa?',
        '1. Importa un documento csv o Excel con información de los nuevos potenciales clientes.\n'
        '2. Calcula la calidad crediticia (score) de cada cliente.\n'
        '3. Determina una decisión de negocio para cada cliente de acuerdo a unos umbrales de score establecidos.\n'
        '4. Genera un Excel con los resultados.'
        )

def open_notes():
    open_window(
        'Notas de uso',
        '- Los archivos que contengan la información de los nuevos clientes que quieres evaluar,\n'
        '  deben seguir la plantilla del dataset orginial.\n'
        '- Evidentemente, si no se conoce el valor de BAD, se debe dejar en blanco.\n'
        '  Pero nunca puede eliminarse la columna.\n'
        '- No eliminar los archivos del directorio donde se encuentra el ejectuable.\n'
        '  Eso provocaría un error en la aplicación.'
    )

root = Tk()
root.title('Calculador de calidad crediticia')
root.wm_iconbitmap(r'GUI_icon.ico')
root.geometry('800x500')	 
root.maxsize(1000, 500)
root.minsize(600, 500)

menubar = Menu(root)

menu1 = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Guía de uso',menu=menu1)
menu1.add_command(label='Qué hace el programa?', command=open_tutorial)
menu1.add_command(label='Notas de uso', command=open_notes)

menu2 = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Contacto',menu=menu2)
menu2.add_command(label='Email: yanezgranadososcar22@gmail.com')

root.config(menu=menubar)

Label(text='Calculador de calidad crediticia',bg='#7ACDE6',font=('Times New Roman',18),height=2).pack(fill=X)

frame1 = Frame()
frame1.config(bg='white')
Label(frame1,text='Selecciona documento:',bg='white',font=('Times New Roman',15),width = 20).pack(side=LEFT)
Label(frame1,text='Formatos válidos: .csv/.xlsx',bg='white',width=30).pack(side=RIGHT,padx=5)
Button(frame1,text='Importar documento', bg='#B5ECFC',font=('Times New Roman',15),width=70,command=upload).pack(side=RIGHT)
frame1.pack(fill=X,pady=10)

document_label_text = StringVar()
document_label_text.set('Ningún documento seleccionado')
document_uploaded_label = Label(textvariable=document_label_text,fg='red',font=('Times New Roman',12))
document_uploaded_label.pack()

Button(text='Calcular',bg='#B5ECFC',font=('Times New Roman',15),width=70,command=predict).pack(pady=10)

Label(text='Desarrollado por Oscar Yáñez',font=('Times New Roman',12,'italic'),bg='grey',fg='white').pack(side=BOTTOM,fill=X)
image = Image.open(r'ucm_logo_gui.png')
image = image.resize((380, 200))
ucm_image = ImageTk.PhotoImage(image)
Label(image=ucm_image).pack(side=BOTTOM)

root.mainloop()