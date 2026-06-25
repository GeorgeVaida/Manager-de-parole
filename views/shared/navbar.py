import flet as ft
from core import session
def create_appbar(page: ft.Page) -> ft.AppBar:

    async def push2fa():
        return await page.push_route("/setup_2FA")
    
    async def logout(e):

        session.delete_key()
        
        if session.KEY is None:
            await page.push_route("/login")
        else:
            print("error deleting the key")

    
    return ft.AppBar(
        title=ft.Text("Password manager"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(
                icon=ft.Icons.ADD,
                tooltip="Add logins",
                on_click=lambda e: page.run_task(page.push_route, "/add")
            ),
            ft.IconButton(
                icon=ft.Icons.HOME, 
                tooltip="My Passwords",
                on_click=lambda e: page.run_task(page.push_route, "/display")
            ),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content="2FA", icon=ft.Icons.SECURITY, on_click= push2fa),
                    ft.PopupMenuItem(),
                    ft.PopupMenuItem(content="Log Out", icon=ft.Icons.LOGOUT, on_click=logout),
                ]
            ),
        ],
    )