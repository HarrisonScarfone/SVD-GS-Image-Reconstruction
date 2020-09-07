import PySimpleGUI as sg
import os.path
import matplotlib
import cv2
import numpy as np

from matplotlib.image import imread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CANVAS_IDS = [
    '-CANVAS1-', '-CANVAS2-', '-CANVAS3-', '-CANVAS4-', '-CANVAS5-', '-CANVAS6-', '-CANVAS7-', '-CANVAS8-', '-CANVAS9-'
    ]

N_VALS = [1, 2, 3, 4, 5, 10, 25, 50, 100]

file_list_column = [
    [
        sg.Text("Base Image Path"),
        sg.In(size=(40, 1), enable_events=True, key="-IMAGEPATH-"),
        sg.FileBrowse(),
        sg.VSeparator(),
        sg.Text('Original Image:'),
        sg.Canvas(key='-ORIGINAL-')
    ],
    [
        sg.Button('Reconstruct my image!', key="-GO-"), 
        sg.Button('Clear Images', key='-CLEAR-'), 
        sg.Button('Exit', key='-EXIT-')
    ],
    [sg.HSeparator()],
    [
        sg.Text('Singular Values (Diagonal)', size=(55,1), justification='center'), 
        sg.Text('Singular Values Cumulative Sum', size=(60,1), justification='center'), 
    ],
    [
        sg.Canvas(key='-SINGLE-'), 
        sg.Canvas(key='-SINGLESUM-'), 

    ],
]

def generate_reconstruction_column():
    image_viewer_column = []
    text_col = []
    image_col = []
    for i, (n, canvas_id) in enumerate(zip(N_VALS, CANVAS_IDS)):
        text_col.append(sg.Text(f'n={n}', size=(20,1), justification='center'))
        image_col.append(sg.Canvas(key=canvas_id))
        if i % 3 == 2:
            image_viewer_column.append(text_col)
            image_viewer_column.append(image_col)
            text_col, image_col = [], []
    return image_viewer_column
            
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(generate_reconstruction_column()),
    ]
]

window = sg.Window("Greyscale Image Reconstruction With Singular Value Decomposition", layout, finalize=True)
sg.SetOptions(icon='icon_base64')

matplotlib.use("TKAgg")

def get_approximation_figure(image_path, n, need_S=False):

    A = imread(image_path)
    A = cv2.resize(A, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
    X = np.mean(A, -1)

    U, S, VT = np.linalg.svd(X, full_matrices=False)
    S = np.diag(S)

    Xapprox = U[:,:n] @ S[0:n,:n] @ VT[:n,:]

    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    fig.figimage(Xapprox, cmap='gray', resize=True)

    if need_S: 
        return S, fig 
    return fig

def get_singular_figure(S):
    fig = matplotlib.figure.Figure(figsize=(4, 3), dpi=100)
    fig.add_subplot(111, yscale='log').plot(np.diag(S))
    return fig

def get_singular_values_sum_figure(S):
    fig = matplotlib.figure.Figure(figsize=(4, 3), dpi=100)
    fig.add_subplot(111).plot(np.cumsum(np.diag(S) / np.sum(np.diag(S))))
    return fig

def get_resized_original(img_path):
    A = imread(image_path)
    A = cv2.resize(A, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
    A = np.mean(A, -1)
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    fig.figimage(A, cmap='gray', resize=True)
    return fig

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

FIGURES = []
S_MATRIX = None

while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == '-GO-':
        try:
            while FIGURES:
                figure = FIGURES.pop()
                figure.get_tk_widget().pack_forget()
            image_path = values['-IMAGEPATH-']
            fig = draw_figure(window['-ORIGINAL-'].TKCanvas, get_resized_original(image_path))
            FIGURES.append(fig)
            for n, canvas_id in zip(N_VALS, CANVAS_IDS):
                if canvas_id == CANVAS_IDS[-1]:
                    S_MATRIX, fig = get_approximation_figure(image_path, n, True)
                    fig = draw_figure(window[canvas_id].TKCanvas, fig)
                    FIGURES.append(fig)
                    fig = draw_figure(window['-SINGLE-'].TKCanvas, get_singular_figure(S_MATRIX))
                    FIGURES.append(fig)
                    fig = draw_figure(window['-SINGLESUM-'].TKCanvas, get_singular_values_sum_figure(S_MATRIX))
                    FIGURES.append(fig)
                    continue
                fig = draw_figure(window[canvas_id].TKCanvas, get_approximation_figure(image_path, n))  
                FIGURES.append(fig)
        except Exception as e:
            print(e)
    
    if event == '-CLEAR-':
        while FIGURES:
            figure = FIGURES.pop()
            figure.get_tk_widget().pack_forget()


window.close()