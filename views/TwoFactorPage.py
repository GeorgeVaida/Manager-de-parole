import flet as ft
from controllers import TwoFactor_controller
from views.shared.navbar import create_appbar

def TwoFactorView(page: ft.Page):
    secret = {"value": None}
    qr_img = ft.Image(width=200, height=200, src=None)
    input_field = ft.TextField(label="enter 6 digit code")
    
    
    def close_action(e):
        alert_dialog.open = False
        page.update()
    
    def verify_action(e):
        code = input_field.value
        response = TwoFactor_controller.confirm_and_save(secret["value"], code)

        alert_dialog.open = False
        page.update()
        if response[0] == True:
            page.views.pop()
            page.views.append(TwoFactorView(page))
            page.update()
        else:
            alert_dialog.open = False
            page.update()
            page.show_dialog(ft.SnackBar(f"Failed : {response[1]}"))
            page.update()

    alert_dialog = ft.AlertDialog(
        title=ft.Text("Scan with Google Authenticator"),
        content=ft.Column(
            controls=[qr_img, input_field],
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        actions=[
            ft.Button(content="Cancel", on_click=close_action),
            ft.Button(content="Verify", on_click=verify_action)
        ],
        open=False
    )

    def setup_2fa(e):
        
        bag = TwoFactor_controller.generate_2fa()
        secret["value"] = bag["secret"]
        qr_img.src = bag["qr_image"]
        
        input_field.value = ""

        page.show_dialog(alert_dialog)

    def disable_2FA(e):
        response = TwoFactor_controller.disable()
        if response:
            page.views.pop()
            page.views.append(TwoFactorView(page))
            page.update()
            page.show_dialog(ft.SnackBar("2FA disabled successfully"))
        else:
            page.show_dialog(ft.SnackBar("Error"))
            page.update()



    is_enabled = TwoFactor_controller.is_enabled()
    if is_enabled:
        page_content = ft.Column(
            controls=[
                ft.Text("Two-Factor Authentication", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("2FA is enabled", color=ft.Colors.GREEN),
                ft.Button("Disable 2FA", on_click=disable_2FA, icon=ft.Icons.DANGEROUS, bgcolor=ft.Colors.RED)
            ]
        )
    else:
        page_content = ft.Column(
            controls=[
                ft.Text("Two-Factor Authentication", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Google authenticator", size=20, weight=ft.FontWeight.W_600),
                ft.Button(
                    content="Setup 2FA", 
                    icon=ft.Icons.QR_CODE_SCANNER,
                    on_click=setup_2fa
                )
            ]
        )

    return ft.View(
        route="/setup_2FA",
        appbar=create_appbar(page),
        controls=[
            ft.Container(
                padding=20,
                content=page_content
            )
        ]
    )
