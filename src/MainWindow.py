import flet as ft


class MainWindow():
    def __init__(self, loadedData):
        self._loadedData = loadedData

    def __main(self, page: ft.Page):
        page.title = "Flet counter example"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

        def minus_click(e):
            txt_number.value = str(int(txt_number.value) - 1)
            page.update()

        def plus_click(e):
            txt_number.value = str(int(txt_number.value) + 1)
            page.update()

        page.add(
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        ## try listview
        list_view = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        list_view.controls.clear()
        list_view.controls = self.__create_table_rows(self._loadedData)
        page.add(list_view)

    def __create_table_rows(self, data) -> list[ft.Row]:
        result = list[ft.Row]()
        for item in sorted(data, key=lambda _: _.scope, reverse=True):
            row = ft.Row([
                # ft.IconButton(icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED, icon_size=20),
                ft.TextField(value=item.scope, border=ft.InputBorder.NONE),
                ft.Text(self.__format_seconds_to_hours(item.working_seconds)),
                ft.Text(self.__format_seconds_to_hours(item.overtime_seconds)),
            ])
            result.append(row)
        return result

    @staticmethod
    def __format_seconds_to_hours(data: int) -> str:
        return '{:.2f}'.format(data / 60 / 60)

    def run_window(self):
        ft.app(target=self.__main)
