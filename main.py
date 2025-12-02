from tkinter import *
from tkinter import font
import psycopg2
import tkintermapview

db_engine = psycopg2.connect(
    user="postgres",
    database="postgres",
    password="postgres",
    port="5432",
    host="localhost"
)

jednostki: list = []

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

def add_jednostki(jednostki_data:list)->None:
    name:str = entry_nazwa_jednostki.get()
    city:str = entry_miasto_jednostki.get()
    street:str = entry_ulica_jednostki.get()
    jednostki_data.append(Jednostki(name=name, city=city, street=street))
    print(jednostki_data)
    jednostki_info(jednostki_data)
    entry_nazwa_jednostki.delete(0, END)
    entry_miasto_jednostki.delete(0, END)
    entry_ulica_jednostki.delete(0, END)
    entry_nazwa_jednostki.focus()

def jednostki_info (jednostki_data:list):
    list_box_lista_jednostek.delete(0, END)
    for idx,jednostki in enumerate(jednostki_data):
        list_box_lista_jednostek.insert(idx, f"{jednostki.name}" )

def delete_jednostka(jednostki_data: list):
    i = list_box_lista_jednostek.index(ACTIVE)
    jednostki_data[i].marker.delete()
    jednostki_data.pop(i)
    jednostki_info(jednostki_data)

def edit_jednostki(jednostki_data: list):
    i = list_box_lista_jednostek.index(ACTIVE)
    entry_nazwa_jednostki.insert(0, jednostki_data[i].name)
    entry_miasto_jednostki.insert(0, jednostki_data[i].city)
    entry_ulica_jednostki.insert(0, jednostki_data[i].street)

    button_dodaj_jednostke.config(text="Zapisz zmiany", command=lambda: update_jednostki(jednostki_data, i))

def update_jednostki(jednostki_data: list, i):
    jednostki_data[i].name = entry_nazwa_jednostki.get()
    jednostki_data[i].city = entry_miasto_jednostki.get()
    jednostki_data[i].street = entry_ulica_jednostki.get()

    jednostki_data[i].coords = jednostki_data[i].get_coordinates()
    jednostki_data[i].marker.set_position(jednostki_data[i].coords[0], jednostki_data[i].coords[1])
    jednostki_data[i].marker.set_text(jednostki_data[i].name)

    jednostki_info(jednostki_data)

    button_dodaj_jednostke.config(text="Dodaj jednostkę", command=lambda: add_jednostki(jednostki))
    entry_nazwa_jednostki.delete(0, END)
    entry_miasto_jednostki.delete(0, END)
    entry_ulica_jednostki.delete(0, END)
    entry_nazwa_jednostki.focus()



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

buttom_szczegoly_pracownika= Button(ramka_pracownicy, text="Wyświetl szczegóły", font=default_font)
buttom_szczegoly_pracownika.grid(row=2, column=0, sticky="ew")

buttom_usun_pracownika = Button(ramka_pracownicy, text="Usuń", font=default_font)
buttom_usun_pracownika.grid(row=2, column=1, sticky="ew")

buttom_aktualizuj_pracownika = Button(ramka_pracownicy, text="Aktualizuj", font=default_font)
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

button_dodaj_pracownika = Button(ramka_formularz_pracownicy, text="Dodaj obiekt", font=default_font)
button_dodaj_pracownika.grid(row=4, column=0, columnspan=2, sticky="ew")

ramka_formularz_pracownicy.columnconfigure(1, weight=1)


#RAMKA LISTA INCYDENTÓW
label_lista_incydentow = Label(ramka_incydenty, text="Lista incydentów", font=label_font, bg="#f0c2e3")
label_lista_incydentow.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_incydentow = Listbox(ramka_incydenty, font=default_font)
list_box_lista_incydentow.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_szczegoly_incydentu= Button(ramka_incydenty, text="Wyświetl szczegóły", font=default_font)
buttom_szczegoly_incydentu.grid(row=2, column=0, sticky="ew")

buttom_usun_incydent = Button(ramka_incydenty, text="Usuń", font=default_font)
buttom_usun_incydent.grid(row=2, column=1, sticky="ew")

buttom_aktualizuj_incydent = Button(ramka_incydenty, text="Aktualizuj", font=default_font)
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

# label_nazwisko_pracownika = Label(ramka_formularz_jednostki, text="Nazwisko: ")
# label_nazwisko_pracownika.grid(row=2, column=0, sticky=W)
#
# label_miasto_pracownika = Label(ramka_formularz_jednostki, text="Miasto: ")
# label_miasto_pracownika.grid(row=3, column=0, sticky=W)

entry_nazwa_incydentu = Entry(ramka_formularz_incydenty, font=default_font)
entry_nazwa_incydentu.grid(row=1, column=1, sticky="ew")

# entry_nazwisko_pracownika = Entry(ramka_formularz_jednostki)
# entry_nazwisko_pracownika.grid(row=2, column=1)
#
# entry_miasto_pracownika = Entry(ramka_formularz_jednostki)
# entry_miasto_pracownika.grid(row=3, column=1)

button_dodaj_pracownika = Button(ramka_formularz_incydenty, text="Dodaj obiekt", font=default_font)
button_dodaj_pracownika.grid(row=2, column=0, columnspan=2, sticky="ew")
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

root.mainloop()