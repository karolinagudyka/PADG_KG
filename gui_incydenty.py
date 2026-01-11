from tkinter import *
from tkinter import messagebox
from database import db_engine
from models import Incydenty




def add_incydent(incydenty_data:list, list_box, map_widget, marker_icon, entry_nazwa, entry_miejsce, entry_jednostka, db_engine = db_engine) -> None:
    cursor = db_engine.cursor()
    name: str = entry_nazwa.get()
    place: str = entry_miejsce.get()
    jednostka_name = entry_jednostka.get()

    cursor.execute("SELECT id FROM public.jednostki WHERE name = %s",(jednostka_name,))
    result = cursor.fetchone()

    unit_id = result[0]

    sql = "INSERT INTO public.incydenty(name, place, unit_id) VALUES (%s, %s, %s);"
    cursor.execute(sql, (name, place, unit_id))
    db_engine.commit()
    cursor.close()

    incydent_info(incydenty_data, list_box, map_widget, marker_icon)
    entry_nazwa.delete(0, END)
    entry_miejsce.delete(0, END)
    entry_jednostka.delete(0, END)
    entry_nazwa.focus()


def show_incydent_details(incydenty_data: list, list_box, root, label_font, default_font, entry_nazwa, entry_miejsce,  db_engine = db_engine) -> None:
    i = list_box.index(ACTIVE)
    if i < 0:
        return

    cursor = db_engine.cursor()
    sql = "SELECT name, place FROM public.incydenty WHERE name = %s"
    cursor.execute(sql, (incydenty_data[i].name,))
    data = cursor.fetchone()
    cursor.close()

    if not data:
        return

    detail_window = Toplevel(root)
    detail_window.title(f"Szczegóły incydentu: {data[0]}")
    detail_window.geometry("500x250")
    detail_window.configure(bg="#eddff7")

    Label(detail_window, text=f"Szczegóły incydentu", font=label_font, bg="#eddff7").pack(pady=10)

    info_frame = Frame(detail_window, bg="#eddff7", padx=20, pady=10)
    info_frame.pack(fill=BOTH, expand=True)

    Label(info_frame, text="Nazwa:", font=label_font, bg="#eddff7").grid(row=0, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[0], font=default_font, bg="#eddff7").grid(row=0, column=1, sticky=W, pady=5)

    Label(info_frame, text="Miejsce:", font=label_font, bg="#eddff7").grid(row=1, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[1], font=default_font, bg="#eddff7").grid(row=1, column=1, sticky=W, pady=5)

    Button(detail_window, text="Zamknij", command=detail_window.destroy, font=default_font).pack(pady=10)

    entry_nazwa.delete(0, END)
    entry_miejsce.delete(0, END)
    entry_nazwa.focus()

def incydent_info (incydenty_data:list, list_box, map_widget, marker_icon, db_engine = db_engine) -> None:
    for incydent in incydenty_data:
        if incydent.marker:
            incydent.marker.delete()
    incydenty_data.clear()

    list_box.delete(0, END)
    sql = "SELECT name, place FROM public.incydenty"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    failed_coords = []

    for idx, row in enumerate(db_data):
        incydent = Incydenty(name=row[0], place=row[1], map_widget=map_widget, marker_icon=marker_icon)
        incydenty_data.append(incydent)
        list_box.insert(idx, f"  {row[0]}")

        if not incydent.coords:
            failed_coords.append(row[0])

    if failed_coords:
        messagebox.showwarning(
            "Brak lokalizacji – incydenty","Nie udało się pobrać współrzędnych dla:\n\n" + "\n".join(failed_coords) + "\n\nTe incydenty nie będą widoczne na mapie.")

def delete_incydent(incydenty_data: list, list_box, map_widget, marker_icon) -> None:
    i = list_box.index(ACTIVE)
    name = incydenty_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.incydenty WHERE name = %s", (name,))
    db_engine.commit()
    cursor.close()

    incydent_info(incydenty_data, list_box, map_widget, marker_icon)

def edit_incydent(incydenty_data: list, list_box, map_widget, marker_icon, entry_nazwa, entry_miejsce, entry_jednostka, button_dodaj) -> None:
    i = list_box.index(ACTIVE)
    entry_nazwa.insert(0, incydenty_data[i].name)
    entry_miejsce.insert(0, incydenty_data[i].place)

    button_dodaj.config(text="Zapisz zmiany", command=lambda: update_incydent(incydenty_data, i, list_box, map_widget, marker_icon, entry_nazwa, entry_miejsce, button_dodaj, entry_jednostka))

def update_incydent(incydenty_data: list, i, list_box, map_widget, marker_icon, entry_nazwa, entry_miejsce, button_dodaj, entry_jednostka_incydentu) -> None:
    old_name = incydenty_data[i].name
    incydenty_data[i].name = entry_nazwa.get()
    incydenty_data[i].place = entry_miejsce.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.incydenty SET name = %s, place = %s WHERE name = %s"
    cursor.execute(sql, (incydenty_data[i].name, incydenty_data[i].place, old_name))
    db_engine.commit()
    cursor.close()

    incydenty_data[i].coords = incydenty_data[i].get_coordinates()
    incydenty_data[i].marker.set_position(incydenty_data[i].coords[0], incydenty_data[i].coords[1])
    incydenty_data[i].marker.set_text(incydenty_data[i].name)

    incydent_info(incydenty_data, list_box, map_widget, marker_icon)

    button_dodaj.config(text="Dodaj incydent", command=lambda: add_incydent(incydenty_data, list_box, map_widget, marker_icon, entry_nazwa, entry_miejsce, entry_jednostka_incydentu), bg = "#f7e9f3", fg="white",relief="flat", bd=0, highlightbackground="#ffffff", highlightcolor="#ffffff", highlightthickness=2, padx=10, pady=6, cursor="hand2")
    entry_nazwa.delete(0, END)
    entry_miejsce.delete(0, END)
    entry_jednostka_incydentu.delete(0, END)
    entry_nazwa.focus()


