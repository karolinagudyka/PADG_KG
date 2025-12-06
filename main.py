from tkinter import *
from tkinter import font
import psycopg2
import tkintermapview
import webbrowser

db_engine = psycopg2.connect(
    user="postgres",
    database="jednostki_policji",
    password="postgres",
    port="5432",
    host="localhost"
)

jednostki: list = []
pracownicy: list = []
incydenty: list = []

class Jednostki:
    def __init__(self, name: str, city: str, street = str):
        self.name = name
        self.city = city
        self.street = street
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

def add_jednostki(jednostki_data:list, db_engine = db_engine)->None:
    cursor = db_engine.cursor()
    name:str = entry_nazwa_jednostki.get()
    city:str = entry_miasto_jednostki.get()
    street:str = entry_ulica_jednostki.get()

    sql = "INSERT INTO public.jednostki(name, city, street) VALUES (%s, %s, %s);"
    cursor.execute(sql, (name, city, street))
    db_engine.commit()
    cursor.close()

    jednostki_info(jednostki_data)
    entry_nazwa_jednostki.delete(0, END)
    entry_miasto_jednostki.delete(0, END)
    entry_ulica_jednostki.delete(0, END)
    entry_nazwa_jednostki.focus()

def jednostki_info (jednostki_data:list, db_engine=db_engine):
    for jednostka in jednostki_data:
        jednostka.marker.delete()
    jednostki_data.clear()

    list_box_lista_jednostek.delete(0, END)
    sql = "SELECT name, city, street FROM public.jednostki"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    for idx,row in enumerate(db_data):
        jednostki_data.append(Jednostki(name=row[0], city=row[1], street=row[2]))
        list_box_lista_jednostek.insert(idx, f"{row[0]}")


def delete_jednostka(jednostki_data: list):
    i = list_box_lista_jednostek.index(ACTIVE)
    name = jednostki_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.jednostki WHERE name = %s", (name,))
    db_engine.commit()
    cursor.close()

    jednostki_info(jednostki_data)

def edit_jednostki(jednostki_data: list):
    i = list_box_lista_jednostek.index(ACTIVE)
    entry_nazwa_jednostki.insert(0, jednostki_data[i].name)
    entry_miasto_jednostki.insert(0, jednostki_data[i].city)
    entry_ulica_jednostki.insert(0, jednostki_data[i].street)

    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: update_jednostki(jednostki_data, i))

def update_jednostki(jednostki_data: list, i):
    old_name = jednostki_data[i].name
    jednostki_data[i].name = entry_nazwa_jednostki.get()
    jednostki_data[i].city = entry_miasto_jednostki.get()
    jednostki_data[i].street = entry_ulica_jednostki.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.jednostki SET name = %s, city = %s, street = %s WHERE name = %s"
    cursor.execute(sql, (jednostki_data[i].name, jednostki_data[i].city, jednostki_data[i].street, old_name))
    db_engine.commit()
    cursor.close()

    jednostki_data[i].coords = jednostki_data[i].get_coordinates()
    jednostki_data[i].marker.set_position(jednostki_data[i].coords[0], jednostki_data[i].coords[1])
    jednostki_data[i].marker.set_text(jednostki_data[i].name)

    jednostki_info(jednostki_data)

    button_dodaj_jednostke.config(text="Dodaj jednostkę", command=lambda: add_jednostki(jednostki))
    entry_nazwa_jednostki.delete(0, END)
    entry_miasto_jednostki.delete(0, END)
    entry_ulica_jednostki.delete(0, END)
    entry_nazwa_jednostki.focus()


class Pracownicy:
    def __init__(self, name: str, surname: str, city = str):
        self.name = name
        self.surname = surname
        self.city = city
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

def add_pracownik(pracownicy_data:list, db_engine = db_engine)->None:
    cursor = db_engine.cursor()
    name:str = entry_imie_pracownika.get()
    surname:str = entry_nazwisko_pracownika.get()
    city:str = entry_miasto_pracownika.get()

    sql = "INSERT INTO public.pracownicy(name, surname, city) VALUES (%s, %s, %s);"
    cursor.execute(sql, (name, surname, city))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data)
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_miasto_pracownika.delete(0, END)
    entry_imie_pracownika.focus()


def pracownik_info (pracownicy_data:list, db_engine = db_engine)->None:
    for pracownik in pracownicy_data:
        pracownik.marker.delete()
    pracownicy_data.clear()

    list_box_lista_pracownikow.delete(0, END)
    sql = "SELECT name, surname, city FROM public.pracownicy"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    for idx,row in enumerate(db_data):
        pracownicy_data.append(Pracownicy(name=row[0], surname=row[1], city=row[2]))
        list_box_lista_pracownikow.insert(idx, f"{row[0]} {row[1]}" )

def delete_pracownik(pracownicy_data: list):
    i = list_box_lista_pracownikow.index(ACTIVE)
    name = pracownicy_data[i].name
    surname = pracownicy_data[i].surname

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.pracownicy WHERE name = %s AND surname = %s", (name, surname))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data)

def edit_pracownik(pracownicy_data: list):
    i = list_box_lista_pracownikow.index(ACTIVE)
    entry_imie_pracownika.insert(0, pracownicy_data[i].name)
    entry_nazwisko_pracownika.insert(0, pracownicy_data[i].surname)
    entry_miasto_pracownika.insert(0, pracownicy_data[i].city)

    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_pracownik(pracownicy_data, i))

def update_pracownik(pracownicy_data: list, i):
    old_name = pracownicy_data[i].name
    old_surname = pracownicy_data[i].surname
    new_name = entry_imie_pracownika.get()
    new_surname = entry_nazwisko_pracownika.get()
    new_city = entry_miasto_pracownika.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.pracownicy SET name = %s, surname = %s, city = %s WHERE name = %s AND surname = %s"
    cursor.execute(sql, (new_name, new_surname, new_city, old_name, old_surname))
    db_engine.commit()
    cursor.close()

    pracownik_info(pracownicy_data)

    button_dodaj_pracownika.config(text="Dodaj pracownika", command=lambda: add_pracownik(pracownicy))
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_miasto_pracownika.delete(0, END)
    entry_imie_pracownika.focus()


def show_pracownik_details(pracownik_data: list):
    i = list_box_lista_pracownikow.index(ACTIVE)
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

    Label(info_frame, text="Imię:", font=("Times New Roman", 11, "bold"), bg="#eddff7").grid(row=0, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[0], font=default_font, bg="#eddff7").grid(row=0, column=1, sticky=W, pady=5)

    Label(info_frame, text="Nazwisko:", font=("Times New Roman", 11, "bold"), bg="#eddff7").grid(row=1, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[1], font=default_font, bg="#eddff7").grid(row=1, column=1, sticky=W, pady=5)

    Label(info_frame, text="Miasto:", font=("Times New Roman", 11, "bold"), bg="#eddff7").grid(row=2, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[2], font=default_font, bg="#eddff7").grid(row=2, column=1, sticky=W, pady=5)

    Button(detail_window, text="Zamknij", command=detail_window.destroy, font=default_font).pack(pady=10)

    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_miasto_pracownika.delete(0, END)
    entry_imie_pracownika.focus()



class Incydenty:
    def __init__(self, name: str, place: str):
        self.name = name
        self.place = place
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.place}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

def add_incydent(incydenty_data:list, db_engine = db_engine)->None:
    cursor = db_engine.cursor()
    name: str = entry_nazwa_incydentu.get()
    place: str = entry_miejsce_incydentu.get()

    sql = "INSERT INTO public.incydenty(name, place) VALUES (%s, %s);"
    cursor.execute(sql, (name, place))
    db_engine.commit()
    cursor.close()

    incydent_info(incydenty_data)
    entry_nazwa_incydentu.delete(0, END)
    entry_miejsce_incydentu.delete(0, END)
    entry_nazwa_incydentu.focus()


def show_incydent_details(incydenty_data: list):
    i = list_box_lista_incydentow.index(ACTIVE)
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
    detail_window.configure(bg="#f0c2e3")

    Label(detail_window, text=f"Szczegóły incydentu", font=label_font, bg="#f0c2e3").pack(pady=10)

    info_frame = Frame(detail_window, bg="#f0c2e3", padx=20, pady=10)
    info_frame.pack(fill=BOTH, expand=True)

    Label(info_frame, text="Nazwa:", font=("Times New Roman", 11, "bold"), bg="#f0c2e3").grid(row=0, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[0], font=default_font, bg="#f0c2e3").grid(row=0, column=1, sticky=W, pady=5)

    Label(info_frame, text="Miejsce:", font=("Times New Roman", 11, "bold"), bg="#f0c2e3").grid(row=1, column=0, sticky=W, pady=5)
    Label(info_frame, text=data[1], font=default_font, bg="#f0c2e3").grid(row=1, column=1, sticky=W, pady=5)

    Button(detail_window, text="Zamknij", command=detail_window.destroy, font=default_font).pack(pady=10)

    entry_nazwa_incydentu.delete(0, END)
    entry_miejsce_incydentu.delete(0, END)
    entry_nazwa_incydentu.focus()

def incydent_info (incydenty_data:list, db_engine = db_engine)->None:
    for incydent in incydenty_data:
        incydent.marker.delete()
    incydenty_data.clear()

    list_box_lista_incydentow.delete(0, END)
    sql = "SELECT name, place FROM public.incydenty"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    db_data = cursor.fetchall()
    cursor.close()

    for idx, row in enumerate(db_data):
        incydenty_data.append(Incydenty(name=row[0], place=row[1]))
        list_box_lista_incydentow.insert(idx, f"{row[0]}")

def delete_incydent(incydenty_data: list):
    i = list_box_lista_incydentow.index(ACTIVE)
    name = incydenty_data[i].name

    cursor = db_engine.cursor()
    cursor.execute("DELETE FROM public.incydenty WHERE name = %s", (name,))
    db_engine.commit()
    cursor.close()

    incydent_info(incydenty_data)

def edit_incydent(incydenty_data: list):
    i = list_box_lista_incydentow.index(ACTIVE)
    entry_nazwa_incydentu.insert(0, incydenty_data[i].name)
    entry_miejsce_incydentu.insert(0, incydenty_data[i].place)

    button_dodaj_incydent.config(text="Zapisz zmiany", command=lambda: update_incydent(incydenty_data, i))

def update_incydent(incydenty_data: list, i):
    old_name = incydenty_data[i].name
    incydenty_data[i].name = entry_nazwa_incydentu.get()
    incydenty_data[i].place = entry_miejsce_incydentu.get()

    cursor = db_engine.cursor()
    sql = "UPDATE public.incydenty SET name = %s, place = %s WHERE name = %s"
    cursor.execute(sql, (incydenty_data[i].name, incydenty_data[i].place, old_name))
    db_engine.commit()
    cursor.close()

    incydenty_data[i].coords = incydenty_data[i].get_coordinates()
    incydenty_data[i].marker.set_position(incydenty_data[i].coords[0], incydenty_data[i].coords[1])
    incydenty_data[i].marker.set_text(incydenty_data[i].name)

    incydent_info(incydenty_data)

    button_dodaj_incydent.config(text="Dodaj incydent", command=lambda: add_incydent(incydenty))
    entry_nazwa_incydentu.delete(0, END)
    entry_miejsce_incydentu.delete(0, END)
    entry_nazwa_incydentu.focus()




root = Tk()
root.title("Projekt systemu do zarządzania jednostkami policji i policjantami przypisanymi do danej jednostki")
root.geometry("1300x900")

default_font = font.Font(family="Times New Roman", size=10)
label_font = font.Font(family="Times New Roman", size=12, weight="bold")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)

ramka_jednostki = Frame(root, padx=5, pady=5, bg="#f2d0d7")
ramka_formularz_jednostki = Frame(root, padx=5, pady=5, bg="#f2d0d7")
ramka_pracownicy = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_formularz_pracownicy = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_incydenty = Frame(root, padx=5, pady=5, bg="#f0c2e3")
ramka_formularz_incydenty = Frame(root, padx=5, pady=5, bg="#f0c2e3")
ramka_szczegoly_obiektu = Frame(root, padx=5, pady=5, bg="#f7e9f3")
ramka_mapa = Frame(root)

ramka_jednostki.grid(row=0, column=0, sticky="nsew")
ramka_formularz_jednostki.grid(row=0, column=1, sticky="nsew")
ramka_pracownicy.grid(row=0, column=2, sticky="nsew")
ramka_formularz_pracownicy.grid(row=0, column=3, sticky="nsew")
ramka_incydenty.grid(row=0, column=4, sticky="nsew")
ramka_formularz_incydenty.grid(row=0, column=5, sticky="nsew")

ramka_szczegoly_obiektu.grid(row=1, column=0, columnspan=6, sticky="ew", pady=10)
ramka_mapa.grid(row=2, column=0, columnspan=6, sticky="nsew")

# RAMKA LISTA JEDNOSTEK
label_lista_jednostek = Label(ramka_jednostki, text="Lista jednostek policji", font=label_font, bg="#f2d0d7")
label_lista_jednostek.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_jednostek = Listbox(ramka_jednostki, font=default_font)
list_box_lista_jednostek.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_szczegoly_jednostki = Button(ramka_jednostki, text="Wyświetl szczegóły", font=default_font)
buttom_szczegoly_jednostki.grid(row=2, column=0, sticky="ew")

buttom_usun_jednostke = Button(ramka_jednostki, text="Usuń", font=default_font, command=lambda: delete_jednostka(jednostki))
buttom_usun_jednostke.grid(row=2, column=1, sticky="ew")

buttom_aktualizuj_jednostke = Button(ramka_jednostki, text="Aktualizuj", font=default_font, command=lambda: edit_jednostki(jednostki))
buttom_aktualizuj_jednostke.grid(row=2, column=2, sticky="ew")

ramka_jednostki.columnconfigure(0, weight=1)
ramka_jednostki.columnconfigure(1, weight=1)
ramka_jednostki.columnconfigure(2, weight=1)
ramka_jednostki.rowconfigure(1, weight=1)

#RAMKA FORMULARZ JEDNOSTEK
label_formularz_jednostek = Label(ramka_formularz_jednostki, text="Formularz - jednostki: ", font=label_font, bg="#f2d0d7")
label_formularz_jednostek.grid(row=0, column=0, columnspan=2, sticky="ew")

label_nazwa_jednostki = Label(ramka_formularz_jednostki, text= "Nazwa: ", font=default_font, bg="#f2d0d7")
label_nazwa_jednostki.grid(row=1, column=0, sticky=W)

label_ulica_jednostki = Label(ramka_formularz_jednostki, text="Ulica: ", font=default_font, bg="#f2d0d7")
label_ulica_jednostki.grid(row=2, column=0, sticky=W)

label_miasto_jednostki = Label(ramka_formularz_jednostki, text="Miasto: ", font=default_font, bg="#f2d0d7")
label_miasto_jednostki.grid(row=3, column=0, sticky=W)

entry_nazwa_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_nazwa_jednostki.grid(row=1, column=1, sticky="ew")

entry_ulica_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_ulica_jednostki.grid(row=2, column=1, sticky="ew")

entry_miasto_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_miasto_jednostki.grid(row=3, column=1, sticky="ew")

button_dodaj_jednostke = Button(ramka_formularz_jednostki, text="Dodaj jednostkę", font=default_font, command=lambda: add_jednostki(jednostki))
button_dodaj_jednostke.grid(row=4, column=0, columnspan=2, sticky="ew")

ramka_formularz_jednostki.columnconfigure(1, weight=1)


#RAMKA LISTA PRACOWNIKÓW
label_lista_pracownikow = Label(ramka_pracownicy, text="Lista pracowników policji", font=label_font, bg="#eddff7")
label_lista_pracownikow.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_pracownikow = Listbox(ramka_pracownicy, font=default_font)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_szczegoly_pracownika= Button(ramka_pracownicy, text="Wyświetl szczegóły", font=default_font, command=lambda: show_pracownik_details(pracownicy))
buttom_szczegoly_pracownika.grid(row=2, column=0, sticky="ew")

buttom_usun_pracownika = Button(ramka_pracownicy, text="Usuń", font=default_font, command=lambda: delete_pracownik(pracownicy))
buttom_usun_pracownika.grid(row=2, column=1, sticky="ew")

buttom_aktualizuj_pracownika = Button(ramka_pracownicy, text="Aktualizuj", font=default_font, command=lambda: edit_pracownik(pracownicy))
buttom_aktualizuj_pracownika.grid(row=2, column=2, sticky="ew")

ramka_pracownicy.columnconfigure(0, weight=1)
ramka_pracownicy.columnconfigure(1, weight=1)
ramka_pracownicy.columnconfigure(2, weight=1)
ramka_pracownicy.rowconfigure(1, weight=1)

#RAMKA FORMULARZ PRACOWNIKÓW
label_formularz_pracownicy = Label(ramka_formularz_pracownicy, text="Formularz - pracownicy: ", font=label_font, bg="#eddff7")
label_formularz_pracownicy.grid(row=0, column=0, columnspan=2, sticky="ew")

label_imie_pracownika = Label(ramka_formularz_pracownicy, text= "Imię: ", font=default_font, bg="#eddff7")
label_imie_pracownika.grid(row=1, column=0, sticky=W)

label_nazwisko_pracownika = Label(ramka_formularz_pracownicy, text="Nazwisko: ", font=default_font, bg="#eddff7")
label_nazwisko_pracownika.grid(row=2, column=0, sticky=W)

label_miasto_pracownika = Label(ramka_formularz_pracownicy, text="Miasto: ", font=default_font, bg="#eddff7")
label_miasto_pracownika.grid(row=3, column=0, sticky=W)

entry_imie_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_imie_pracownika.grid(row=1, column=1, sticky="ew")

entry_nazwisko_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_nazwisko_pracownika.grid(row=2, column=1, sticky="ew")

entry_miasto_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_miasto_pracownika.grid(row=3, column=1, sticky="ew")

button_dodaj_pracownika = Button(ramka_formularz_pracownicy, text="Dodaj pracownika", font=default_font, command=lambda: add_pracownik(pracownicy))
button_dodaj_pracownika.grid(row=4, column=0, columnspan=2, sticky="ew")

ramka_formularz_pracownicy.columnconfigure(1, weight=1)


#RAMKA LISTA INCYDENTÓW
label_lista_incydentow = Label(ramka_incydenty, text="Lista incydentów", font=label_font, bg="#f0c2e3")
label_lista_incydentow.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_incydentow = Listbox(ramka_incydenty, font=default_font)
list_box_lista_incydentow.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_szczegoly_incydentu= Button(ramka_incydenty, text="Wyświetl szczegóły", font=default_font, command=lambda: show_incydent_details(incydenty))
buttom_szczegoly_incydentu.grid(row=2, column=0, sticky="ew")

buttom_usun_incydent = Button(ramka_incydenty, text="Usuń", font=default_font, command=lambda: delete_incydent(incydenty))
buttom_usun_incydent.grid(row=2, column=1, sticky="ew")

buttom_aktualizuj_incydent = Button(ramka_incydenty, text="Aktualizuj", font=default_font, command=lambda: edit_incydent(incydenty))
buttom_aktualizuj_incydent.grid(row=2, column=2, sticky="ew")

ramka_incydenty.columnconfigure(0, weight=1)
ramka_incydenty.columnconfigure(1, weight=1)
ramka_incydenty.columnconfigure(2, weight=1)
ramka_incydenty.rowconfigure(1, weight=1)

#RAMKA FORMULARZ INCYDENTÓW
label_formularz_incydentow = Label(ramka_formularz_incydenty, text="Formularz - incydenty: ", font=label_font, bg="#f0c2e3")
label_formularz_incydentow.grid(row=0, column=0, columnspan=2, sticky="ew")

label_nazwa_incydentu = Label(ramka_formularz_incydenty, text= "Nazwa: ", font=default_font, bg="#f0c2e3")
label_nazwa_incydentu.grid(row=1, column=0, sticky=W)

label_miejsce_incydentu = Label(ramka_formularz_incydenty, text="Miejsce: ", font=default_font, bg="#f0c2e3")
label_miejsce_incydentu.grid(row=2, column=0, sticky=W)

entry_nazwa_incydentu = Entry(ramka_formularz_incydenty, font=default_font)
entry_nazwa_incydentu.grid(row=1, column=1, sticky="ew")

entry_miejsce_incydentu = Entry(ramka_formularz_incydenty)
entry_miejsce_incydentu.grid(row=2, column=1, sticky="ew")
#
# entry_miasto_pracownika = Entry(ramka_formularz_jednostki)
# entry_miasto_pracownika.grid(row=3, column=1)

button_dodaj_incydent = Button(ramka_formularz_incydenty, text="Dodaj incydent", font=default_font, command=lambda: add_incydent(incydenty))
button_dodaj_incydent.grid(row=3, column=0, columnspan=2, sticky="ew")
ramka_formularz_incydenty.columnconfigure(1, weight=1)

# RAMKA SZCZEGÓŁY OBIEKTU
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu: ", font=label_font, bg="#f7e9f3")
label_szczegoly_obiektu.grid(row=0, column=0, columnspan=6, sticky="ew")

# label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Imie: ", font=default_font, bg="#f7e9f3")
# label_imie_szczegoly_obiektu.grid(row=1, column=0, sticky="ew")
#
# label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", font=default_font, bg="#f7e9f3")
# label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1, sticky="ew")
#
# label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Lokalizacja: ", font=default_font, bg="#f7e9f3")
# label_lokalizacja_szczegoly_obiektu.grid(row=1, column=2, sticky="ew")
#
# label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", font=default_font, bg="#f7e9f3")
# label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=3, sticky="ew")
#
# label_posty_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Posty: ", font=default_font, bg="#f7e9f3")
# label_posty_szczegoly_obiektu.grid(row=1, column=4, sticky="ew")
#
# label_posty_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", font=default_font, bg="#f7e9f3")
# label_posty_szczegoly_obiektu_wartosc.grid(row=1, column=5, sticky="ew")

for i in range(6):
    ramka_szczegoly_obiektu.columnconfigure(i, weight=1)

# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1025, height=600, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

ramka_mapa.columnconfigure(0, weight=1)
ramka_mapa.rowconfigure(0, weight=1)

jednostki_info(jednostki)
pracownik_info(pracownicy)
incydent_info(incydenty)

root.mainloop()