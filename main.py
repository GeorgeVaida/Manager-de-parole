import flet as ft
from utils.dbconn import init_db
from views.loginpage import LoginView
from views.displaypage import DisplayView
from views.addpage import AddView
from views.TwoFactorPage import TwoFactorView

async def main(page: ft.Page):
    page.title = "Password manager"
    init_db()

    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/display":
            page.views.append(DisplayView(page))
        elif page.route == "/add":
            page.views.append(AddView(page))
        elif page.route == "/setup_2FA":
            page.views.append(TwoFactorView(page))
        page.update()


    page.on_route_change = route_change
    await page.push_route("/login")


if __name__ == "__main__":
    ft.run(main)