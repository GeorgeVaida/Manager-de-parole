import flet as ft
from views.shared.navbar import create_appbar
from controllers.vault_controller import get_and_decrypt
from utils.dbconn import delete_entry

def DisplayView(page: ft.Page) -> ft.View:
    listview = ft.ListView(expand=True, spacing=10)
    
    async def delete(e):
        id = e.control.data

        if delete_entry(id):
            page.show_dialog(ft.SnackBar("Deleted successfuly"))
            await load_data()
        else:
            page.show_dialog(ft.SnackBar("Error deleting entry"))            

    async def load_data():
        view_bag = get_and_decrypt()
        
        listview.controls.clear()
        if not view_bag:
            listview.controls.append(ft.Text("You dont have stored logins"))
        
        for item in view_bag:
            listview.controls.append(
                ft.Card(
                    shadow_color=ft.Colors.ON_SURFACE_VARIANT,
                    content=ft.Container(
                        width=400,
                        padding=10,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Column(controls=[
                                    ft.Text(f"Title: {item.title}"),
                                    ft.Text(f"Username: {item.username}"),
                                    ft.Text(f"Password: {item.password}")
                                ]),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.ERROR,
                                    tooltip="Delete this login",
                                    data=item.id,
                                    on_click=delete)
                            ]
                        )
                    )
                )
            )
        page.update()

    page.run_task(load_data)
    return ft.View(
        route="/display",
        appbar=create_appbar(page),
        controls=[
            listview
        ]
    )