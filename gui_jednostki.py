from tkinter import *
from tkinter import messagebox
import webbrowser
from database import db_engine
from models import Jednostki



def add_jednostki(jednostki_data:list, list_box, map_widget, marker_icon, entry_nazwa, entry_miasto, entry_ulica, db_engine = db_engine) -> None:
    cursor = db_engine.cursor()
    name:str = entry_nazwa.get()
    city:str = entry_miasto.get()
    street:str = entry_ulica.get()

    sql = "INSERT INTO public.jednostki(name, city, street) VALUES (%s, %s, %s);"
    cursor.execute(sql, (name, city, street))
    db_engine.commit()
    cursor.close()

    jednostki_info(jednostki_data, list_box, map_widget, marker_icon)
    entry_nazwa.delete(0, END)
    entry_miasto.delete(0, END)
    entry_ulica.delete(0, END)
    entry_nazwa.focus()

def jednostki_info (jednostki_data:list, list_box, map_widget, marker_icon, db_engine=db_engine) -> None:
    for jednostka in jednostki_data:
        if jednostka.marker:
            jednostka.marker.delete()
    jednostki_data.clear()

    list_box.delete(0, END)
    sql = "SELECT name, city, street FROM public.jednostki"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    failed_coords = []
    for idx, row in enumerate(db_data):
        jednostka = Jednostki(name=row[0], city=row[1], street=row[2], map_widget=map_widget, marker_icon=marker_icon)
        jednostki_data.append(jednostka)
        list_box.insert(idx, f"  {row[0]}")

        if not jednostka.coords:
            failed_coords.append(row[0])

    if failed_coords:
        messagebox.showwarning("Brak lokalizacji – jednostki", "Nie udało się pobrać współrzędnych dla:\n\n" + "\n".join(failed_coords) + "\n\nTe jednostki nie będą widoczne na mapie.")

def delete_jednostka(jednostki_data: list, list_box, map_widget, marker_icon) -> None:
    i = list_box.index(ACTIVE)
    name = jednostki_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.jednostki WHERE name = %s", (name,))
    db_engine.commit()
    cursor.close()

    jednostki_info(jednostki_data, list_box, map_widget, marker_icon)

def edit_jednostki(jednostki_data: list, list_box, entry_nazwa, entry_miasto, entry_ulica, button_dodaj, map_widget, marker_icon) -> None:
    i = list_box.index(ACTIVE)
    entry_nazwa.insert(0, jednostki_data[i].name)
    entry_miasto.insert(0, jednostki_data[i].city)
    entry_ulica.insert(0, jednostki_data[i].street)

    button_dodaj.config(text="Zapisz zmiany", command=lambda: update_jednostki(jednostki_data, i, entry_nazwa, entry_miasto, entry_ulica, button_dodaj, list_box, map_widget, marker_icon))

def update_jednostki(jednostki_data: list, i, entry_nazwa, entry_miasto, entry_ulica, button_dodaj, list_box, map_widget, marker_icon) -> None:
    old_name = jednostki_data[i].name
    jednostki_data[i].name = entry_nazwa.get()
    jednostki_data[i].city = entry_miasto.get()
    jednostki_data[i].street = entry_ulica.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.jednostki SET name = %s, city = %s, street = %s WHERE name = %s"
    cursor.execute(sql, (jednostki_data[i].name, jednostki_data[i].city, jednostki_data[i].street, old_name))
    db_engine.commit()
    cursor.close()

    jednostki_data[i].coords = jednostki_data[i].get_coordinates()
    jednostki_data[i].marker.set_position(jednostki_data[i].coords[0], jednostki_data[i].coords[1])
    jednostki_data[i].marker.set_text(jednostki_data[i].name)

    jednostki_info(jednostki_data, list_box, map_widget, marker_icon)

    button_dodaj.config(text="Dodaj jednostkę", command=lambda: add_jednostki(jednostki_data, list_box, map_widget, marker_icon, entry_nazwa, entry_miasto, entry_ulica))
    entry_nazwa.delete(0, END)
    entry_miasto.delete(0, END)
    entry_ulica.delete(0, END)
    entry_nazwa.focus()


def show_jednostka_details(jednostki_data: list, list_box, root, label_font, default_font, entry_nazwa, entry_miasto, entry_ulica) -> None:
    i = list_box.curselection()
    if not i:
        return
    i = i[0]

    cursor = db_engine.cursor()
    sql = "SELECT name, city, street, website_url, description FROM public.jednostki WHERE name = %s"
    cursor.execute(sql, (jednostki_data[i].name,))
    data = cursor.fetchone()
    cursor.close()
    if not data:
        return

    detail_window = Toplevel(root)
    detail_window.title(f"Szczegóły jednostki: {data[0]}")
    detail_window.geometry("800x450")
    detail_window.configure(bg="#eddff7")

    Label(detail_window, text=f"Szczegóły jednostki", font=label_font, bg="#eddff7").pack(pady=10)

    info_frame = Frame(detail_window, bg="#eddff7", padx=20, pady=10)
    info_frame.pack(fill=BOTH, expand=True)

    Label(info_frame, text="Nazwa:", font=label_font, bg="#eddff7").grid(row=0, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[0], font=default_font, bg="#eddff7").grid(row=0, column=1, sticky=W, pady=5)

    Label(info_frame, text="Miasto:", font=label_font, bg="#eddff7").grid(row=1, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[1], font=default_font, bg="#eddff7").grid(row=1, column=1, sticky=W, pady=5)

    Label(info_frame, text="Ulica:", font=label_font, bg="#eddff7").grid(row=2, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[2], font=default_font, bg="#eddff7").grid(row=2, column=1, sticky=W, pady=5)

    Label(info_frame, text="Strona internetowa:", font=label_font, bg="#eddff7").grid(row=3, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[3], font=default_font, bg="#eddff7").grid(row=3, column=1, sticky=W, pady=5)
    link_label = Label(info_frame, text=data[3], font=default_font, fg="blue", cursor="hand2", bg="#eddff7")
    link_label.grid(row=3, column=1, sticky=W)

    link_label.bind("<Button-1>", lambda e: webbrowser.open(data[3]))

    Label(info_frame, text="Opis:", font=label_font,  bg="#eddff7").grid(row=4, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[4], font=default_font, bg="#eddff7").grid(row=4, column=1, sticky=W, pady=5)

    Button(detail_window, text="Zamknij", command=detail_window.destroy, font=default_font, bg="#c9a9e6", fg="white").pack(pady=10)


    entry_nazwa.delete(0, END)
    entry_ulica.delete(0, END)
    entry_miasto.delete(0, END)
    entry_nazwa.focus()

def filtr_pracownicy_by_jednostka(jednostki_data: list, list_box_jednostek, pracownicy, list_box_pracownicy, marker_icon_highlighted, marker_icon_default_pracownicy) -> None:
    i = list_box_jednostek.curselection()
    if not i:
        return
    i = i[0]
    jednostka_name = jednostki_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("SELECT id FROM public.jednostki WHERE name = %s", (jednostka_name,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return

    unit_id = result[0]

    cursor.execute("SELECT name, surname FROM public.pracownicy WHERE unit_id = %s", (unit_id,))
    wybrani_pracownicy = cursor.fetchall()
    cursor.close()

    list_box_pracownicy.selection_clear(0, END)

    for pracownik in pracownicy:
        if pracownik.marker:
            pracownik.marker.change_icon(marker_icon_default_pracownicy)

    for assigned in wybrani_pracownicy:
        for idx, pracownik in enumerate(pracownicy):
            if pracownik.name == assigned[0] and pracownik.surname == assigned[1] and pracownik.marker:
                pracownik.marker.change_icon(marker_icon_highlighted)
                list_box_pracownicy.selection_set(idx)
                list_box_pracownicy.see(idx)

def filtr_incydenty_by_jednostka(jednostki_data: list, list_box_jednostek, incydenty, list_box_incydenty, marker_icon_highlighted, marker_icon_default_incydenty) -> None:
    i = list_box_jednostek.curselection()
    if not i:
        return
    i = i[0]
    jednostka_name = jednostki_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("SELECT id FROM public.jednostki WHERE name = %s", (jednostka_name,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return

    unit_id = result[0]

    cursor.execute("SELECT name FROM public.incydenty WHERE unit_id = %s", (unit_id,))
    wybrane_incydenty = cursor.fetchall()
    cursor.close()

    list_box_incydenty.selection_clear(0, END)

    for incydent in incydenty:
        if incydent.marker:
            incydent.marker.change_icon(marker_icon_default_incydenty)

    for assigned in wybrane_incydenty:
        for idx, incydent in enumerate(incydenty):
            if incydent.name == assigned[0] and incydent.marker:
                incydent.marker.change_icon(marker_icon_highlighted)
                list_box_incydenty.selection_set(idx)
                list_box_incydenty.see(idx)

def clear_highlights(pracownicy, incydenty, list_box_pracownicy, list_box_incydenty, marker_icon_default_pracownicy, marker_icon_default_incydenty) -> None:
    list_box_pracownicy.selection_clear(0, END)
    list_box_incydenty.selection_clear(0, END)
    for pracownik in pracownicy:
        if pracownik.marker:
            pracownik.marker.change_icon(marker_icon_default_pracownicy)
    for incydent in incydenty:
        if incydent.marker:
            incydent.marker.change_icon(marker_icon_default_incydenty)



