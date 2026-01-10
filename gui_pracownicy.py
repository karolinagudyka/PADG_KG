from tkinter import *
from tkinter import messagebox
import webbrowser
from database import db_engine
from models import Pracownicy

def add_pracownik(pracownicy_data:list, list_box, map_widget, marker_icon, entry_imie, entry_nazwisko, entry_miasto, entry_jednostka, db_engine = db_engine)->None:
    cursor = db_engine.cursor()
    name:str = entry_imie.get()
    surname:str = entry_nazwisko.get()
    city:str = entry_miasto.get()
    jednostka_name = entry_jednostka.get()

    # pobranie ID jednostki
    cursor.execute("SELECT id FROM public.jednostki WHERE name = %s",(jednostka_name,))
    result = cursor.fetchone()

    unit_id = result[0]

    sql = "INSERT INTO public.pracownicy(name, surname, city, unit_id) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql, (name, surname, city, unit_id))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data, list_box, map_widget, marker_icon)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miasto.delete(0, END)
    entry_jednostka.delete(0, END)
    entry_imie.focus()


def pracownik_info (pracownicy_data:list, list_box, map_widget, marker_icon, db_engine = db_engine)->None:
    for pracownik in pracownicy_data:
        if pracownik.marker:
            pracownik.marker.delete()
    pracownicy_data.clear()

    list_box.delete(0, END)
    sql = "SELECT name, surname, city FROM public.pracownicy"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    failed_coords = []

    for idx, row in enumerate(db_data):
        pracownik = Pracownicy(name=row[0], surname=row[1], city=row[2], map_widget=map_widget, marker_icon=marker_icon)
        pracownicy_data.append(pracownik)
        list_box.insert(idx, f"  {row[0]} {row[1]}")

        if not pracownik.coords:
            failed_coords.append(f"{row[0]} {row[1]}")

    if failed_coords:
        messagebox.showwarning("Brak lokalizacji – pracownicy","Nie udało się pobrać współrzędnych dla:\n\n" + "\n".join(failed_coords) + "\n\nCi pracownicy nie będą widoczni na mapie.")


def delete_pracownik(pracownicy_data: list, list_box, map_widget, marker_icon):
    i = list_box.index(ACTIVE)
    name = pracownicy_data[i].name
    surname = pracownicy_data[i].surname

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.pracownicy WHERE name = %s AND surname = %s", (name, surname))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data, list_box, map_widget, marker_icon)

def edit_pracownik(pracownicy_data: list, list_box, map_widget, marker_icon, entry_imie, entry_nazwisko, entry_miasto, entry_jednostka, button_dodaj):
    i = list_box.index(ACTIVE)
    entry_imie.insert(0, pracownicy_data[i].name)
    entry_nazwisko.insert(0, pracownicy_data[i].surname)
    entry_miasto.insert(0, pracownicy_data[i].city)

    button_dodaj.config(text="Zapisz zmiany", command=lambda: update_pracownik(pracownicy_data, i, list_box, map_widget, marker_icon,
        entry_imie, entry_nazwisko, entry_miasto,
        entry_jednostka, button_dodaj))

def update_pracownik(pracownicy_data: list, i, list_box, map_widget, marker_icon, entry_imie, entry_nazwisko, entry_miasto, entry_jednostka, button_dodaj):
    old_name = pracownicy_data[i].name
    old_surname = pracownicy_data[i].surname
    new_name = entry_imie.get()
    new_surname = entry_nazwisko.get()
    new_city = entry_miasto.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.pracownicy SET name = %s, surname = %s, city = %s WHERE name = %s AND surname = %s"
    cursor.execute(sql, (new_name, new_surname, new_city, old_name, old_surname))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data, list_box, map_widget, marker_icon)

    button_dodaj.config(text="Dodaj pracownika", command=lambda: add_pracownik(pracownicy_data, list_box, map_widget, marker_icon,
        entry_imie, entry_nazwisko, entry_miasto, entry_jednostka))
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miasto.delete(0, END)
    entry_jednostka.delete(0, END)
    entry_imie.focus()


def show_pracownik_details(pracownik_data: list, list_box, root, label_font, default_font, entry_imie, entry_nazwisko, entry_miasto):
    i = list_box.index(ACTIVE)
    if i < 0:
        return

    cursor = db_engine.cursor()
    sql = "SELECT name, surname, city FROM public.pracownicy WHERE name = %s AND surname = %s"
    cursor.execute(sql, (pracownik_data[i].name, pracownik_data[i].surname))
    data = cursor.fetchone()
    cursor.close()
    if not data:
        return

    detail_window = Toplevel(root)
    detail_window.title(f"Szczegóły pracownika: {data[0]}")
    detail_window.geometry("500x250")
    detail_window.configure(bg="#eddff7")

    Label(detail_window, text=f"Szczegóły incydentu", font=label_font, bg="#eddff7").pack(pady=10)

    info_frame = Frame(detail_window, bg="#eddff7", padx=20, pady=10)
    info_frame.pack(fill=BOTH, expand=True)

    Label(info_frame, text="Imię:", font=label_font, bg="#eddff7").grid(row=0, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[0], font=default_font, bg="#eddff7").grid(row=0, column=1, sticky=W, pady=5)

    Label(info_frame, text="Nazwisko:", font=label_font, bg="#eddff7").grid(row=1, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[1], font=default_font, bg="#eddff7").grid(row=1, column=1, sticky=W, pady=5)

    Label(info_frame, text="Miasto:", font=label_font, bg="#eddff7").grid(row=2, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[2], font=default_font, bg="#eddff7").grid(row=2, column=1, sticky=W, pady=5)

    Button(detail_window, text="Zamknij", command=detail_window.destroy, font=default_font).pack(pady=10)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miasto.delete(0, END)
    entry_imie.focus()

