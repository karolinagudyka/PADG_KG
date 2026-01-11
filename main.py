import tkintermapview
from gui_jednostki import *
from gui_pracownicy import *
from gui_incydenty import *
from tkinter import font, PhotoImage

jednostki: list = []
pracownicy: list = []
incydenty: list = []

root = Tk()
root.title("Projekt systemu do zarządzania jednostkami policji i policjantami przypisanymi do danej jednostki")
root.geometry("1500x900")

default_font = font.Font(family="Century Gothic", size=10)
label_font = font.Font(family="Century Gothic", size=12, weight="bold")

marker_icon_default_jednostki = PhotoImage(file="assets/jednostki.png")
marker_icon_default_pracownicy = PhotoImage(file="assets/pracownicy.png")
marker_icon_default_incydenty = PhotoImage(file="assets/incydenty.png")
marker_icon_highlighted = PhotoImage(file="assets/highlighted.png")
map_icon = PhotoImage(file="assets/map.png")
jednostka_icon = PhotoImage(file="assets/jednostka.png")
pracownik_icon = PhotoImage(file="assets/pracownik.png")
incydent_icon = PhotoImage(file="assets/incydent.png")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)

ramka_jednostki = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_formularz_jednostki = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_pracownicy = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_formularz_pracownicy = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_incydenty = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_formularz_incydenty = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_naglowek_mapy = Frame(root, padx=5, pady=5, bg="#eddff7")
ramka_mapa = Frame(root)

ramka_jednostki.grid(row=0, column=0, sticky="nsew")
ramka_formularz_jednostki.grid(row=0, column=1, sticky="nsew")
ramka_pracownicy.grid(row=0, column=2, sticky="nsew")
ramka_formularz_pracownicy.grid(row=0, column=3, sticky="nsew")
ramka_incydenty.grid(row=0, column=4, sticky="nsew")
ramka_formularz_incydenty.grid(row=0, column=5, sticky="nsew")

ramka_naglowek_mapy.grid(row=1, column=0, columnspan=6, sticky="ew", pady=10)
ramka_mapa.grid(row=2, column=0, columnspan=6, sticky="nsew")

# RAMKA LISTA JEDNOSTEK
label_lista_jednostek = Label(ramka_jednostki, text="Lista jednostek policji", image=jednostka_icon, compound=LEFT,
                              font=label_font, bg="#eddff7")
label_lista_jednostek.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_jednostek = Listbox(ramka_jednostki, font=default_font)
list_box_lista_jednostek.grid(row=1, column=0, columnspan=3, sticky="nsew")

button_szczegoly_jednostki = Button(ramka_jednostki, text="Wyświetl szczegóły", font=default_font,
                                    command=lambda: show_jednostka_details(jednostki, list_box_lista_jednostek, root,
                                    label_font, default_font, entry_nazwa_jednostki, entry_miasto_jednostki,
                                    entry_ulica_jednostki), bg="#d8a7e6", fg="white", bd=0,

                                    padx=10, pady=6, cursor="hand2")
button_szczegoly_jednostki.grid(row=2, column=0, sticky="ew", padx=4, pady=4)

button_usun_jednostke = Button(ramka_jednostki, text="Usuń", font=default_font,
                                command=lambda: delete_jednostka(jednostki, list_box_lista_jednostek, map_widget,
                                marker_icon_default_jednostki), bg="#d8a7e6", fg="white", bd=0, padx=10,
                                pady=6, cursor="hand2")
button_usun_jednostke.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

button_aktualizuj_jednostke = Button(ramka_jednostki, text="Aktualizuj", font=default_font,
                                    command=lambda: edit_jednostki(jednostki, list_box_lista_jednostek,
                                    entry_nazwa_jednostki, entry_miasto_jednostki, entry_ulica_jednostki,
                                    button_dodaj_jednostke, map_widget, marker_icon_default_jednostki), bg="#d8a7e6",
                                    fg="white", bd=0, padx=10, pady=6, cursor="hand2")
button_aktualizuj_jednostke.grid(row=2, column=2, sticky="ew", padx=4, pady=4)

ramka_jednostki.columnconfigure(0, weight=1)
ramka_jednostki.columnconfigure(1, weight=1)
ramka_jednostki.columnconfigure(2, weight=1)
ramka_jednostki.rowconfigure(1, weight=1)

# RAMKA FORMULARZ JEDNOSTEK
label_formularz_jednostek = Label(ramka_formularz_jednostki, text="Formularz - jednostki: ", font=label_font,
                                  bg="#eddff7")
label_formularz_jednostek.grid(row=0, column=0, columnspan=2, sticky="ew")

label_nazwa_jednostki = Label(ramka_formularz_jednostki, text="Nazwa: ", font=default_font, bg="#eddff7")
label_nazwa_jednostki.grid(row=1, column=0, sticky=W)

label_ulica_jednostki = Label(ramka_formularz_jednostki, text="Ulica: ", font=default_font, bg="#eddff7")
label_ulica_jednostki.grid(row=2, column=0, sticky=W)

label_miasto_jednostki = Label(ramka_formularz_jednostki, text="Miasto: ", font=default_font, bg="#eddff7")
label_miasto_jednostki.grid(row=3, column=0, sticky=W)

entry_nazwa_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_nazwa_jednostki.grid(row=1, column=1, sticky="ew")

entry_ulica_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_ulica_jednostki.grid(row=2, column=1, sticky="ew")

entry_miasto_jednostki = Entry(ramka_formularz_jednostki, font=default_font)
entry_miasto_jednostki.grid(row=3, column=1, sticky="ew")

button_dodaj_jednostke = Button(ramka_formularz_jednostki, text="Dodaj jednostkę", font=default_font,
                                command=lambda: add_jednostki(jednostki, list_box_lista_jednostek, map_widget,
                                marker_icon_default_jednostki, entry_nazwa_jednostki,entry_miasto_jednostki,
                                entry_ulica_jednostki), bg="#d8a7e6", fg="white", bd=0,
                                padx=10, pady=6, cursor="hand2")
button_dodaj_jednostke.grid(row=4, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

button_wyswietl_pracownikow = Button(ramka_formularz_jednostki, text="Wyświetl pracowników", font=default_font,
                                    command=lambda: filtr_pracownicy_by_jednostka(jednostki, list_box_lista_jednostek,
                                    pracownicy, list_box_lista_pracownikow, marker_icon_highlighted,
                                    marker_icon_default_pracownicy), bg="#e0a1bf", fg="white", bd=0,
                                    padx=10, pady=6, cursor="hand2")
button_wyswietl_pracownikow.grid(row=6, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

button_wyswietl_incydenty = Button(ramka_formularz_jednostki, text="Wyświetl incydenty", font=default_font,
                                   command=lambda: filtr_incydenty_by_jednostka(jednostki, list_box_lista_jednostek,
                                    incydenty, list_box_lista_incydentow, marker_icon_highlighted,
                                    marker_icon_default_incydenty), bg="#e0a1bf", fg="white", bd=0,
                                   padx=10, pady=6, cursor="hand2")
button_wyswietl_incydenty.grid(row=7, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

button_wyczysc_zaznaczenia = Button(ramka_formularz_jednostki, text="Wyczyść zaznaczenia", font=default_font,
                                    command=lambda: clear_highlights(pracownicy, incydenty, list_box_lista_pracownikow,
                                    list_box_lista_incydentow, marker_icon_default_pracownicy,
                                    marker_icon_default_incydenty), bg="#e8b6cf", fg="white", bd=0,
                                    padx=10, pady=4, cursor="hand2")
button_wyczysc_zaznaczenia.grid(row=8, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

ramka_formularz_jednostki.columnconfigure(1, weight=1)

# RAMKA LISTA PRACOWNIKÓW
label_lista_pracownikow = Label(ramka_pracownicy, text="Lista pracowników policji", image=pracownik_icon, compound=LEFT,
                                font=label_font, bg="#eddff7")
label_lista_pracownikow.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_pracownikow = Listbox(ramka_pracownicy, font=default_font)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=3, sticky="nsew")

button_szczegoly_pracownika = Button(ramka_pracownicy, text="Wyświetl szczegóły", font=default_font,
                                    command=lambda: show_pracownik_details(pracownicy, list_box_lista_pracownikow,
                                    root, label_font, default_font, entry_imie_pracownika, entry_nazwisko_pracownika,
                                    entry_miasto_pracownika), bg="#d8a7e6", fg="white", bd=0, padx=10, pady=6,
                                    cursor="hand2")
button_szczegoly_pracownika.grid(row=2, column=0, sticky="ew", padx=4, pady=4)

button_usun_pracownika = Button(ramka_pracownicy, text="Usuń", font=default_font,
                                command=lambda: delete_pracownik(pracownicy, list_box_lista_pracownikow, map_widget,
                                marker_icon_default_pracownicy), bg="#d8a7e6", fg="white", bd=0, padx=10,
                                pady=6, cursor="hand2")
button_usun_pracownika.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

button_aktualizuj_pracownika = Button(ramka_pracownicy, text="Aktualizuj", font=default_font,
                                    command=lambda: edit_pracownik(pracownicy, list_box_lista_pracownikow, map_widget,
                                    marker_icon_default_pracownicy, entry_imie_pracownika, entry_nazwisko_pracownika,
                                    entry_miasto_pracownika, entry_jednostka_pracownika, button_dodaj_pracownika),
                                    bg="#d8a7e6", fg="white", bd=0, padx=10, pady=6, cursor="hand2")
button_aktualizuj_pracownika.grid(row=2, column=2, sticky="ew", padx=4, pady=4)

ramka_pracownicy.columnconfigure(0, weight=1)
ramka_pracownicy.columnconfigure(1, weight=1)
ramka_pracownicy.columnconfigure(2, weight=1)
ramka_pracownicy.rowconfigure(1, weight=1)

# RAMKA FORMULARZ PRACOWNIKÓW
label_formularz_pracownicy = Label(ramka_formularz_pracownicy, text="Formularz - pracownicy: ", font=label_font,
                                   bg="#eddff7")
label_formularz_pracownicy.grid(row=0, column=0, columnspan=2, sticky="ew")

label_imie_pracownika = Label(ramka_formularz_pracownicy, text="Imię: ", font=default_font, bg="#eddff7")
label_imie_pracownika.grid(row=1, column=0, sticky=W)

label_nazwisko_pracownika = Label(ramka_formularz_pracownicy, text="Nazwisko: ", font=default_font, bg="#eddff7")
label_nazwisko_pracownika.grid(row=2, column=0, sticky=W)

label_miasto_pracownika = Label(ramka_formularz_pracownicy, text="Miasto: ", font=default_font, bg="#eddff7")
label_miasto_pracownika.grid(row=3, column=0, sticky=W)

label_jednostka_pracownika = Label(ramka_formularz_pracownicy, text="Jednostka policji: ", font=default_font,
                                   bg="#eddff7")
label_jednostka_pracownika.grid(row=4, column=0, sticky=W)

entry_imie_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_imie_pracownika.grid(row=1, column=1, sticky="ew")

entry_nazwisko_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_nazwisko_pracownika.grid(row=2, column=1, sticky="ew")

entry_miasto_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_miasto_pracownika.grid(row=3, column=1, sticky="ew")

entry_jednostka_pracownika = Entry(ramka_formularz_pracownicy, font=default_font)
entry_jednostka_pracownika.grid(row=4, column=1, sticky="ew")

button_dodaj_pracownika = Button(ramka_formularz_pracownicy, text="Dodaj pracownika", font=default_font,
                                command=lambda: add_pracownik(pracownicy, list_box_lista_pracownikow, map_widget,
                                marker_icon_default_pracownicy, entry_imie_pracownika, entry_nazwisko_pracownika,
                                entry_miasto_pracownika, entry_jednostka_pracownika), bg="#d8a7e6", fg="white",
                                bd=0, padx=10, pady=6, cursor="hand2")
button_dodaj_pracownika.grid(row=5, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

ramka_formularz_pracownicy.columnconfigure(1, weight=1)

# RAMKA LISTA INCYDENTÓW
label_lista_incydentow = Label(ramka_incydenty, text="Lista incydentów", image=incydent_icon, compound=LEFT,
                               font=label_font, bg="#eddff7")
label_lista_incydentow.grid(row=0, column=0, columnspan=3, sticky="ew")

list_box_lista_incydentow = Listbox(ramka_incydenty, font=default_font)
list_box_lista_incydentow.grid(row=1, column=0, columnspan=3, sticky="nsew")

button_szczegoly_incydentu = Button(ramka_incydenty, text="Wyświetl szczegóły", font=default_font,
                                    command=lambda: show_incydent_details(incydenty, list_box_lista_incydentow, root,
                                    label_font, default_font, entry_nazwa_incydentu, entry_miejsce_incydentu),
                                    bg="#d8a7e6", fg="white", bd=0, padx=10, pady=6, cursor="hand2")
button_szczegoly_incydentu.grid(row=2, column=0, sticky="ew", padx=4, pady=4)

button_usun_incydent = Button(ramka_incydenty, text="Usuń", font=default_font,
                              command=lambda: delete_incydent(incydenty, list_box_lista_incydentow, map_widget,
                              marker_icon_default_incydenty), bg="#d8a7e6", fg="white", bd=0, padx=10,
                              pady=6, cursor="hand2")
button_usun_incydent.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

button_aktualizuj_incydent = Button(ramka_incydenty, text="Aktualizuj", font=default_font,
                                    command=lambda: edit_incydent(incydenty, list_box_lista_incydentow, map_widget,
                                    marker_icon_default_incydenty, entry_nazwa_incydentu, entry_miejsce_incydentu,
                                    entry_jednostka_incydentu, button_dodaj_incydent), bg="#d8a7e6", fg="white", bd=0,
                                    padx=10, pady=6, cursor="hand2")
button_aktualizuj_incydent.grid(row=2, column=2, sticky="ew", padx=4, pady=4)

ramka_incydenty.columnconfigure(0, weight=1)
ramka_incydenty.columnconfigure(1, weight=1)
ramka_incydenty.columnconfigure(2, weight=1)
ramka_incydenty.rowconfigure(1, weight=1)

# RAMKA FORMULARZ INCYDENTÓW
label_formularz_incydentow = Label(ramka_formularz_incydenty, text="Formularz - incydenty: ", font=label_font,
                                   bg="#eddff7")
label_formularz_incydentow.grid(row=0, column=0, columnspan=2, sticky="ew")

label_nazwa_incydentu = Label(ramka_formularz_incydenty, text="Nazwa: ", font=default_font, bg="#eddff7")
label_nazwa_incydentu.grid(row=1, column=0, sticky=W)

label_miejsce_incydentu = Label(ramka_formularz_incydenty, text="Miejsce: ", font=default_font, bg="#eddff7")
label_miejsce_incydentu.grid(row=2, column=0, sticky=W)

label_jednostka_incydentu = Label(ramka_formularz_incydenty, text="Jednostka policji: ",font=default_font,bg="#eddff7")
label_jednostka_incydentu.grid(row=3, column=0, sticky=W)

entry_nazwa_incydentu = Entry(ramka_formularz_incydenty, font=default_font)
entry_nazwa_incydentu.grid(row=1, column=1, sticky="ew")

entry_miejsce_incydentu = Entry(ramka_formularz_incydenty, font=default_font)
entry_miejsce_incydentu.grid(row=2, column=1, sticky="ew")

entry_jednostka_incydentu = Entry(ramka_formularz_incydenty, font=default_font)
entry_jednostka_incydentu.grid(row=3, column=1, sticky="ew")

button_dodaj_incydent = Button(ramka_formularz_incydenty, text="Dodaj incydent", font=default_font,
                               command=lambda: add_incydent(incydenty, list_box_lista_incydentow, map_widget,
                               marker_icon_default_incydenty, entry_nazwa_incydentu, entry_miejsce_incydentu,
                               entry_jednostka_incydentu,), bg="#d8a7e6", fg="white", bd=0, padx=10, pady=6,
                               cursor="hand2")
button_dodaj_incydent.grid(row=4, column=0, columnspan=2, sticky="ew", padx=4, pady=4)
ramka_formularz_incydenty.columnconfigure(1, weight=1)

# RAMKA NAGŁÓWEK MAPY
label_naglowek_mapy = Label(ramka_naglowek_mapy, text="Mapa", image=map_icon, compound=LEFT, font=label_font,
                            bg="#f7e9f3", fg="#4b0082", padx=10, pady=5)
label_naglowek_mapy.grid(row=0, column=0, columnspan=6, sticky="ew")
ramka_naglowek_mapy.config(bg="#ffffff", highlightbackground="#f7e9f3", highlightthickness=2, padx=5, pady=5)

for i in range(6):
    ramka_naglowek_mapy.columnconfigure(i, weight=1)

# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1025, height=600, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

ramka_mapa.columnconfigure(0, weight=1)
ramka_mapa.rowconfigure(0, weight=1)

jednostki_info(jednostki,list_box_lista_jednostek,map_widget,marker_icon_default_jednostki)
pracownik_info(pracownicy,list_box_lista_pracownikow, map_widget, marker_icon_default_pracownicy)
incydent_info(incydenty,list_box_lista_incydentow, map_widget, marker_icon_default_incydenty)

root.mainloop()
