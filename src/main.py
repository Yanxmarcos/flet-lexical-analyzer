import os
import subprocess
from pathlib import Path

import flet as ft

ENGINE = Path(__file__).resolve().parents[1] / 'build' / 'programa.exe'

def main(page: ft.Page):
    #Configuraciones de ventana
    page.window.bgcolor = ft.Colors.WHITE
    page.bgcolor = ft.Colors.WHITE
    page.window.always_on_bottom = False
    page.window.always_on_top = False
    page.window.frameless = False #Si la ventana de la aplicación debe no tener marco.
    page.window.full_screen = False
    page.window.ignore_mouse_events = False
    page.window.resizable = True #Si se puede cambiar el tamaño de la ventana de la aplicación.
    page.window.title_bar_hidden = True #Ocultar barra de arriba
    page.window.title_bar_buttons_hidden = True #Ocultar barra de arriba
    page.window.shadow = True
    page.padding = 0
    page.window.maximized = True

    def minimizar(e):
        page.window.minimized = True
        page.update()

    def maximizar(e):
        page.window.maximized = True
        page.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]  # Tomar el primer archivo seleccionado
            with open(file.path, "r", encoding="utf-8") as f:
                contenido = f.read()  # Leer el contenido del archivo .txt

            # Agregar una nueva pestaña con el contenido cargado
            pestanias_codigo.tabs.append(
                ft.Tab(
                    tab_content=ft.Row([
                        ft.Text(f"   {file.name}   ", tooltip=f"{file.path}"),
                        ft.Icon(name=None,color="red"),
                        ft.IconButton(ft.Icons.CLOSE, icon_size=18, tooltip="Cerrar pestaña", on_click=cerrar_pestania_codigo)
                    ], spacing=0),
                    content=CodeEditor(contenido_inicial=contenido)  # Pasar contenido leído
                )
            )
            pestanias_codigo.selected_index = len(pestanias_codigo.tabs) - 1
            pestanias_codigo.update()
        else:
            print("Nada")

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            file_path = e.path
            index = pestanias_codigo.selected_index
            if not file_path.lower().endswith(".txt"):  # Verificar si tiene la extensión .txt
                file_path += ".txt"  # Agregar .txt si no está presente

            contexto = pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

            # MIO AGREGADO
            texto_procesado = '\n'.join([
                linea.rstrip()  # Solo elimina espacios del lado derecho
                for linea in contexto.splitlines()
                if linea.strip() != ""  # Mantiene la indentación izquierda
            ])
            # MIO AGREGADO

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(texto_procesado)  # Guardar el contenido del TextField en el archivo .txt

            file_name = os.path.basename(file_path)  # Obtener solo el nombre del archivo
            pestanias_codigo.tabs[index].tab_content.controls[0].value = f"   {file_name}   "
            pestanias_codigo.tabs[index].tab_content.controls[0].tooltip=f"{file_path}"
            pestanias_codigo.tabs[index].tab_content.update()
            pestanias_codigo.update()
        else:
            print("Operación cancelada")

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)



    dialogo_archivo_actualizado = ft.AlertDialog(
        title=ft.Text("Archivo actualizado.",color="green",font_family="Consolas"),
        icon=ft.Icon(ft.Icons.SAVE_SHARP,color="green",size=30),
        open=False,
        bgcolor="#bdc3c7",
    )

    page.overlay.append(dialogo_archivo_actualizado)

    def guardar_archivo_verificar(e):
        index = pestanias_codigo.selected_index
        ruta_archivo = pestanias_codigo.tabs[index].tab_content.controls[0].tooltip
        if ruta_archivo == None:
            save_file_dialog.save_file(
                file_name="programa_fuente.txt",
                allowed_extensions=["txt"]
            )
        else:
            contexto = pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

            # MIO AGREGADO
            texto_procesado = '\n'.join([
                linea.rstrip()  # Solo elimina espacios del lado derecho
                for linea in contexto.splitlines()
                if linea.strip() != ""  # Mantiene la indentación izquierda
            ])
            # MIO AGREGADO

            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(texto_procesado)
            dialogo_archivo_actualizado.open = True
            page.update()
        quitar_simbolo_no_guardado(e)

    def poner_simbolo_no_guardado(e):
        index = pestanias_codigo.selected_index
        nombre_archivo = pestanias_codigo.tabs[index].tab_content.controls[0].value
        if nombre_archivo != "   Sin título   ":
            pestanias_codigo.tabs[index].tab_content.controls[1].name = ft.Icons.SAVE_OUTLINED
            pestanias_codigo.update()

    def quitar_simbolo_no_guardado(e):
        index = pestanias_codigo.selected_index
        pestanias_codigo.tabs[index].tab_content.controls[1].name = None
        pestanias_codigo.update()

    def CodeEditor(contenido_inicial=""):
        numero_de_lineas = ft.Text(
            value="1",
            font_family="Consolas",
            size=17,
            color="#8b92b9",
            width=50,
            text_align=ft.TextAlign.RIGHT,
            weight="bold"
        )
        ingreso_de_codigo = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=1,
            max_lines=None,
            content_padding=ft.Padding(top=68, left=20,right=0,bottom=0),
            text_style=ft.TextStyle(font_family="Cascadia Code",color="#000000"),
            hint_text="Ingrese aquí el código para analizar...",
            hint_style=ft.TextStyle(font_family="Cascadia Code",color="#000000"),
            cursor_color = "black",
            dense=True,
            value=contenido_inicial,
            autofocus=True,
            mouse_cursor=ft.MouseCursor.TEXT
            #counter_text="{value_length} caracteres."
        )

        scroll_contenedor = ft.Column(
            [
                ft.Row(
                    [ingreso_de_codigo],
                    scroll="auto",
                    expand=True,
                    vertical_alignment="start"
                )
            ],
            expand=True
        )

        num_caracteres = ft.Text("[0]", color="#8b92b9",weight="bold",text_align=ft.TextAlign.RIGHT,width=50)

        def update_line_numbers(e):
            lines = ingreso_de_codigo.value.split('\n')
            numero_de_lineas.value = '\n'.join(str(i + 1) for i in range(len(lines) or 1))
            num_caracteres.value = f"[{len(ingreso_de_codigo.value)}]"
            num_caracteres.update()
            numero_de_lineas.update()

        def padre_update(e):
            update_line_numbers(e)
            poner_simbolo_no_guardado(e)

        ingreso_de_codigo.on_change = padre_update
        ingreso_de_codigo.on_focus = update_line_numbers

        return ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column([num_caracteres,numero_de_lineas]),
                        scroll_contenedor
                    ],
                    spacing=5,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            ],
            expand=True,
            spacing=0,
        )

    def cerrar_pestania_codigo(e):
        # Obtener el botón de la pestaña cerrada
        boton_cerrar = e.control
        # Buscar la pestaña asociada al botón
        for i, tab in enumerate(pestanias_codigo.tabs):
            if boton_cerrar in tab.tab_content.controls:
                # Eliminar la pestaña encontrada
                del pestanias_codigo.tabs[i]
                # Ajustar el índice de la pestaña seleccionada
                if pestanias_codigo.selected_index >= len(pestanias_codigo.tabs):
                    pestanias_codigo.selected_index = max(0, len(pestanias_codigo.tabs) - 1)
                pestanias_codigo.update()
                break

    pestanias_codigo = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        divider_color="white",
        divider_height=3,
        label_color="#30419b",
        label_text_style=ft.TextStyle(weight="bold"),
        overlay_color="white",
        unselected_label_color = "black",
        unselected_label_text_style=ft.TextStyle(weight=ft.FontWeight.NORMAL),
        indicator_color="#30419b",
        indicator_thickness = 4,
        tabs=[
            ft.Tab(
                tab_content=ft.Row([ft.Text("   Sin título   "),ft.Icon(name=None,color="red"),ft.IconButton(ft.Icons.CLOSE,icon_size=18,tooltip="Cerrar pestaña",on_click=cerrar_pestania_codigo)],spacing=0),
                content=CodeEditor()
            )
        ],
        expand=True,
    )

    def crear_pestania_codigo(e):
        pestanias_codigo.tabs.append(
            ft.Tab(
                tab_content=ft.Row([ft.Text("   Sin título   "),ft.Icon(name=None,color="red"),ft.IconButton(ft.Icons.CLOSE,icon_size=18,tooltip="Cerrar pestaña",on_click=cerrar_pestania_codigo)],spacing=0),
                content=CodeEditor()
            )
        )
        pestanias_codigo.selected_index= len(pestanias_codigo.tabs) - 1
        pestanias_codigo.update()

    dialogo_debes_guardar_primero = ft.AlertDialog(
        title=ft.Text("Guarda el archivo fuente antes de Analizarlo.",color="pink",font_family="Consolas"),
        icon=ft.Icon(ft.Icons.ANNOUNCEMENT_ROUNDED,color="pink",size=30),
        open=False,
        bgcolor="#bdc3c7",
    )

    page.overlay.append(dialogo_debes_guardar_primero)

    # Botón para ejecutar el analizador léxico
    def ejecutar_analizador(e):

        index = pestanias_codigo.selected_index
        ruta_archivo = pestanias_codigo.tabs[index].tab_content.controls[0].tooltip
        if ruta_archivo == None:
            dialogo_debes_guardar_primero.open = True
            page.update()
            return

        try:
            contenedor_archivos.content.controls[17].visible = True
            contenedor_archivos.update()
            if pestanias_codigo.tabs[index].tab_content.controls[1].name != None:
                contexto = pestanias_codigo.tabs[index].content.controls[0].controls[1].controls[0].controls[0].value

                # MIO AGREGADO
                texto_procesado = '\n'.join([
                    linea.rstrip()  # Solo elimina espacios del lado derecho
                    for linea in contexto.splitlines()
                    if linea.strip() != ""  # Mantiene la indentación izquierda
                ])
                # MIO AGREGADO

                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(texto_procesado)
                pestanias_codigo.tabs[index].tab_content.controls[1].name = None
                pestanias_codigo.update()

            resultado = subprocess.run(
                [str(ENGINE), ruta_archivo],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
            )
            pestanias_resultado.tabs[0].content.controls[2].content.controls[0].controls = None
            pestanias_resultado.tabs[0].content.controls[0].content.controls[0].controls = None

            for linea in resultado.stdout.split("\n"):
                linea = linea.strip()

                # Detectar errores léxicos
                if linea.startswith(">"):
                    signo,linea,error = linea.split("|", 2)
                    print(f"Linea: {linea}")
                    pestanias_resultado.tabs[0].content.controls[2].content.controls[0].controls.append(
                        ft.CupertinoListTile(
                            additional_info=ft.Text(f"Línea: {linea}",selectable=True),
                            bgcolor_activated=ft.Colors.BLUE,
                            leading=ft.Icon(name=ft.Icons.ERROR),
                            title=ft.Text(f"Error léxico: {error}",selectable=True),
                            #subtitle=ft.Text("Línea",selectable=True),
                            trailing=ft.Icon(name=ft.Icons.DRAW_OUTLINED),
                            on_click=tile_clicked,
                            bgcolor="#951414"
                        ),
                    ),

                if linea.startswith("+"):
                    signo, token, datos = linea.split("|", 2)
                    lexema, nombre_token = datos.rsplit("|", 1)
                    print(f"Token: {token} Lexema{lexema}")
                    pestanias_resultado.tabs[0].content.controls[0].content.controls[0].controls.append(
                        ft.CupertinoListTile(
                            additional_info=ft.Text(f"Número: {token}",selectable=True),
                            bgcolor_activated=ft.Colors.BLUE,
                            leading=ft.Icon(name=ft.Icons.TOKEN),
                            title=ft.Text(f"{nombre_token}",selectable=True),
                            subtitle=ft.Text(f"Token:  {lexema}",selectable=True, weight="bold"),
                            trailing=ft.Icon(name=ft.Icons.EMOJI_SYMBOLS),
                            on_click=tile_clicked,
                        ),
                    )

            panel_resultados.height = 450
            nonlocal panel_height
            panel_height = 450
            panel_resultados.update()
        except Exception as e:
            page.open(ft.SnackBar(ft.Text(f"No se pudo ejecutar el analizador: {e}")))

        # Actualizar la página
        contenedor_archivos.content.controls[17].visible = False
        page.update()

    def limpiar_resultados(e):
        pestanias_resultado.tabs[0].content.controls[2].content.controls[0].controls = None
        pestanias_resultado.tabs[0].content.controls[0].content.controls[0].controls = None
        panel_resultados.height = 58
        nonlocal panel_height
        panel_height = 58
        contenedor_archivos.content.controls[17].visible = False
        page.update()

    contenedor_archivos = ft.Container(
        content=ft.Column([
            ft.Text("ANALIZADOR LÉXICO",size=26,font_family="Bauhaus 93"),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=40),
            ft.ElevatedButton("Analizar archivo fuente",icon=ft.Icons.SMART_DISPLAY_SHARP, bgcolor="#239b56",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "#f1c40f",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,},
                color={ft.ControlState.HOVERED: "#f1c40f",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,},
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, "#239b56"),
                    ft.ControlState.HOVERED: ft.BorderSide(2, "#f1c40f"),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                },
                alignment=ft.alignment.center_left
            ), height=40, width=260, on_click=ejecutar_analizador),
            ft.Container(height=40),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=10),
            #===============================================================================================
            #Botones abajo de ANÁLISIS
            ft.ElevatedButton("Nuevo archivo fuente",icon=ft.Icons.INSERT_DRIVE_FILE_ROUNDED, bgcolor="#30419b",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260, on_click=crear_pestania_codigo),

            ft.Container(height=20),

            ft.ElevatedButton("Abrir archivo fuente",icon=ft.Icons.FILE_OPEN, bgcolor="#30419b",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260,on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=["txt"]  # Solo archivos .txt
                    ),),

            ft.Container(height=20),

            ft.ElevatedButton("Guardar archivo fuente",icon=ft.Icons.SAVE, bgcolor="#30419b",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260,on_click=guardar_archivo_verificar
            ),
            ft.Container(height=20),
            ft.Divider(color="white",trailing_indent=200, leading_indent=0),
            ft.Container(height=20),
            ft.ElevatedButton("Limpiar resultados",icon=ft.Icons.CLEANING_SERVICES, bgcolor="#30419b",style=ft.ButtonStyle(
                icon_size=25,
                text_style=ft.TextStyle(size=16,weight="bold"),
                icon_color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                color={ft.ControlState.HOVERED: "white",
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE70,},
                shape=ft.RoundedRectangleBorder(radius=5),
                alignment=ft.alignment.center_left
            ), height=40, width=260,on_click=limpiar_resultados
            ),
            ft.Container(height=50),
            ft.Container(content=ft.Column([
                ft.Text("          Analizando          ",font_family="Consolas",color="yellow",size=15,weight="bold"),
                ft.ProgressBar(expand=True,color="yellow")
            ],alignment="center"),visible=False),

            ft.Container(content=ft.Row([ft.Icon(ft.Icons.COPYRIGHT,size=18),ft.Text("Escuela de Informática-UNT",font_family="Consolas")]),expand=True,alignment=ft.alignment.bottom_center,padding=10)
        ],spacing=0),
        bgcolor="#30419b", width=300,margin=0, padding=ft.Padding(left=20,right=20,top=10,bottom=0)
    )
    contenedor_compilador = ft.Container(content=pestanias_codigo,bgcolor=ft.Colors.WHITE, expand=True, margin=0,padding=0,height=800)

    # Altura inicial del panel de resultados
    panel_height = 58
    min_panel_height = 58
    max_panel_height = 450  # Máxima expansión

    def manija_de_arrastre(e: ft.DragUpdateEvent):
        nonlocal panel_height
        # Ajustar la altura con el desplazamiento vertical
        panel_height -= e.delta_y
        panel_height = max(min_panel_height, min(panel_height, max_panel_height))
        panel_resultados.height = panel_height
        panel_resultados.update()  # Actualizar la UI

    def tile_clicked(e):
        print("clikc")

    pestanias_resultado = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        divider_color="#30419b",
        divider_height=3,
        label_color="white",
        label_text_style=ft.TextStyle(weight="bold"),
        overlay_color="blue",
        unselected_label_color = "white",
        unselected_label_text_style=ft.TextStyle(weight=ft.FontWeight.NORMAL),
        indicator_color="white",
        indicator_thickness = 4,
        tabs=[
            ft.Tab(
                tab_content=ft.Row([ft.Icon(ft.Icons.DASHBOARD_OUTLINED,size=18),ft.Text("  RESULTADO LÉXICO")],spacing=0),
                content=ft.Row([
                    ft.Container(
                        expand=True,
                        bgcolor="transparent",
                        margin=20,
                        content=ft.ListView(
                            controls=[
                                ft.Column(
                                    [
                                    ],
                                    scroll="auto",
                                    alignment="start",
                                    expand=True
                                )
                            ],
                            expand=True,
                            spacing=0,
                        )
                    ),
                    ft.VerticalDivider(color="#30419b",thickness=4,width=0),
                    ft.Container(
                        expand=True,
                        bgcolor="transparent",
                        margin=20,
                        content=ft.ListView(
                            controls=[
                                ft.Column(
                                    [
                                    ],
                                    scroll="auto",
                                    alignment="start",
                                    expand=True
                                )
                            ],
                            expand=True,
                            spacing=0,
                        )
                    )
                ])
            ),
            ft.Tab(
                tab_content=ft.Row([ft.Icon(ft.Icons.DATA_OBJECT_ROUNDED,size=18),ft.Text("  RESULTADO SINTÁCTICO")],spacing=0),
                content=ft.Text("<<Implementación futura>>",italic=True,size=16)
            ),
        ],
        expand=True,
    )

    # Panel de resultados Consola
    panel_resultados = ft.Container(
        height=panel_height,
        content=ft.Column(
            [
                # Barra superior arrastrable
                ft.GestureDetector(
                    content=ft.Container(
                        height=8, bgcolor="#30419b"
                    ),
                    on_vertical_drag_update=manija_de_arrastre,  # Detectar arrastre
                    mouse_cursor=ft.MouseCursor.RESIZE_UP_DOWN
                ),
                # Contenido de la consola
                ft.Container(
                    expand=True,
                    bgcolor="#2b303c",
                    content=pestanias_resultado,
                ),
            ],
            spacing=0,
        ),
        bgcolor=ft.Colors.GREY_900,
    )

    page.add(
        ft.Row([
            contenedor_archivos,
            ft.Column([
                ft.Row([
                    ft.WindowDragArea(ft.Container(content=ft.Row([ft.Image(src="buscar.png",height=25),ft.Text("Analizador", font_family="Harlow Solid",weight="bold",color="#000000",size=25)]), bgcolor=ft.Colors.WHITE, padding=10), expand=True),
                    ft.Container(content=ft.Row([
                        ft.IconButton(
                        ft.Icons.ARROW_CIRCLE_DOWN_OUTLINED,
                        on_click=minimizar,
                        bgcolor="white",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.HOVERED: ft.Colors.RED,
                                ft.ControlState.FOCUSED: "#30419b",
                                ft.ControlState.DEFAULT: "#30419b"
                            }
                        ),
                        tooltip="Minimizar"
                    ),
                    ft.IconButton(
                        ft.Icons.CROP_SQUARE,
                        on_click=maximizar,
                        bgcolor="white",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.HOVERED: ft.Colors.RED,
                                ft.ControlState.FOCUSED: "#30419b",
                                ft.ControlState.DEFAULT: "#30419b"
                            }
                        ),
                        tooltip="Maximizar"
                    ),
                    ft.IconButton(
                        ft.Icons.CLOSE,
                        on_click=lambda _: page.window.close(),
                        bgcolor="white",
                        style=ft.ButtonStyle(
                            color={
                                ft.ControlState.HOVERED: ft.Colors.RED,
                                ft.ControlState.FOCUSED: "#30419b",
                                ft.ControlState.DEFAULT: "#30419b"
                            }
                        ),
                        tooltip="Cerrar"
                    ),
                    ],spacing=0),bgcolor="white",height=56,width=125)
                ],spacing=0),

                ft.Stack(
                    [
                        contenedor_compilador,  # Fondo Editor de código
                        ft.Container(  # Panel flotante sobre el editor
                            content=panel_resultados,
                            bottom=0,
                            left=0,
                            right=0,
                        ),
                    ],
                    expand=True,
                )
            ],expand=True,spacing=0)
        ],expand=True,spacing=0)
    )

ft.app(main, assets_dir=str(Path(__file__).resolve().parent / "assets"))