import flet as ft
from utils import password_gen, password_strenght
from controllers.vault_controller import encrypt_and_save
from views.shared.navbar import create_appbar

def AddView(page: ft.Page) -> ft.View:
    #!! separate? return [color , value]
    def check_password(e):
        score = password_strenght.calculate(password_field.value)
        
        if score == 0:
            strength_bar.value = 0
            strength_label.value = ""
        elif score <= 2:
            strength_bar.value = 0.20
            strength_bar.color = ft.Colors.RED
            strength_label.value = "Very weak"
            strength_label.color = ft.Colors.RED
        elif score <= 4:
            strength_bar.value = 0.40
            strength_bar.color = ft.Colors.ORANGE
            strength_label.value = "Weak"
            strength_label.color = ft.Colors.ORANGE 
        elif score <= 5:
            strength_bar.value = 0.60
            strength_bar.color = ft.Colors.YELLOW
            strength_label.value = "Moderate"
            strength_label.color = ft.Colors.YELLOW
        elif score <= 6:
            strength_bar.value = 0.80
            strength_bar.color = ft.Colors.GREEN_200
            strength_label.value = "Strong"
            strength_label.color = ft.Colors.GREEN_200
        else:
            strength_bar.value = 1.0
            strength_bar.color = ft.Colors.GREEN
            strength_label.value = "Very Strong"
            strength_label.color = ft.Colors.GREEN

    #!! separate ? + add to displaypage?
    async def copy_action():
        txt = display_pass_field.value
        await ft.Clipboard().set(txt)   #https://flet.dev/docs/services/clipboard/

    display_pass_field = ft.Text(weight=ft.FontWeight.BOLD, selectable=True)
    display_pass_card = ft.Card(
            visible=False,
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            content=ft.Container(
                padding=15,
                content=ft.Row(
                    controls=[display_pass_field,
                              ft.IconButton(icon=ft.Icons.COPY,
                                            on_click=copy_action)],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        )

    def save_data(e):
        response = encrypt_and_save(title_field.value, username_field.value, password_field.value)
        if response:
            page.show_dialog(ft.SnackBar(content=ft.Text("Logins Saved!")))
            title_field.value = ""
            username_field.value = ""
            password_field.value = ""
            page.update()
        else:
            page.show_dialog(ft.SnackBar(content=ft.Text("Error saving credentials")))

   
    def generate_action(e):
        display_pass_field.value = ""
        new_password = password_gen.generate(
            int(length_slider.value),
            upper_checkbox.value,
            nums_checkbox.value,
            symbols_checkbox.value)
        display_pass_field.value = new_password
        display_pass_card.visible = True
        page.update()




    title_field = ft.TextField(label="Service title", password=False)
    username_field = ft.TextField(label="Username", password=False)
    password_field = ft.TextField(label="Password", password=False, width=350, on_change=check_password)
    strength_bar = ft.ProgressBar(expand=True, value=0) #https://flet.dev/docs/controls/progressbar/
    strength_label = ft.Text(weight=ft.FontWeight.BOLD)
    ## generator
    upper_checkbox = ft.Checkbox(label="Upper", value=True)
    nums_checkbox = ft.Checkbox(label="Numbers", value=True)
    symbols_checkbox = ft.Checkbox(label="Symbols", value=True)
    length_slider = ft.Slider(min=10, max=64, value=16, divisions=54, label="{value} chars") #https://flet.dev/docs/controls/slider/
    


    return ft.View(
        route="/add",
        appbar=create_appbar(page),
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Add login credentials"),
                    title_field,
                    username_field,
                    ft.Column(
                        controls=[
                            password_field,
                            ft.Row(
                                controls=[strength_bar, strength_label], 
                                width=350,

                                spacing=5
                            )
                        ],
                        spacing=3
                    ),
                    ft.Button(content="Save", on_click=save_data),
                    ft.Divider(),
                
                ### generator
                    ft.Text("Generate Password", weight=ft.FontWeight.BOLD),
                    display_pass_card,
                    ft.Row([
                        length_slider,
                        upper_checkbox,
                        nums_checkbox,
                        symbols_checkbox
                    ]),
                    ft.Button(content="Generate", on_click=generate_action)
                ]
            )
        ]
    )