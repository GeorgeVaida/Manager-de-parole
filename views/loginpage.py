import flet as ft
from core import session
from controllers import auth_controller, TwoFactor_controller

def LoginView(page: ft.Page):
    password_field = ft.TextField(
        label="Password", 
        password=True, 
        can_reveal_password=True
    )
    input_field = ft.TextField(label="enter 6 digit code")


    def close_action(e):
        alert_dialog.open = False
        session.delete_key()
        page.update()
    
    async def verify_action(e):
        alert_dialog.open = False
        code = input_field.value
        response = TwoFactor_controller.get_and_verify(code)
        
        
        if response == True:
            await page.push_route("/display")
        else:
            session.delete_key()
            page.show_dialog(ft.SnackBar(f"Failed"))
        page.update()
    
    
    alert_dialog = ft.AlertDialog(
        title=ft.Text("Enter Google Authenticator code:"),
        content=ft.Column(
            input_field,
            tight=True
        ),
        actions=[
            ft.Button(content="Cancel", on_click=close_action),
            ft.Button(content="Verify", on_click=verify_action)
        ],
        open=False
    )

    async def login_click(e):
        
        response = auth_controller.auth(password_field.value.encode('utf-8'))
        
        if (response  == "SETUP_OK" or response == "LOGIN_OK"):
            await page.push_route("/display")
        elif response == "2FA":
            page.show_dialog(alert_dialog)
        else:
            page.show_dialog(ft.SnackBar(content=ft.Text("ERROR")))


    return ft.View(
        route="/login",
        controls=[
            ft.Text("Login", weight="bold"),
            password_field,
            ft.Button("Log In", on_click=login_click),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )