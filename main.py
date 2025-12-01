from tkinter import *
import tkintermapview

root = Tk()
root.title("Projekt systemu do zarządzania jednostkami policji i policjantami przypisanymi do danej jednostki")
root.geometry("2304x1536")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)

ramka_jednostki = Frame(root, padx=5, pady=5)
ramka_formularz_jednostki = Frame(root, padx=5, pady=5)
ramka_pracownicy = Frame(root, padx=5, pady=5)
ramka_formularz_pracownicy = Frame(root, padx=5, pady=5)
ramka_incydenty = Frame(root, padx=5, pady=5)
ramka_formularz_incydenty = Frame(root, padx=5, pady=5)
ramka_szczegoly_obiektu = Frame(root, padx=5, pady=5)
ramka_mapa = Frame(root)

ramka_jednostki.grid(row=0, column=0, sticky="nw")
ramka_formularz_jednostki.grid(row=0, column=1, sticky="nw")
ramka_pracownicy.grid(row=0, column=2, sticky="nw")
ramka_formularz_pracownicy.grid(row=0, column=3, sticky="nw")
ramka_incydenty.grid(row=0, column=4, sticky="nw")
ramka_formularz_incydenty.grid(row=0, column=5, sticky="nw")

ramka_szczegoly_obiektu.grid(row=1, column=0, columnspan=6, sticky="we", pady=10)
ramka_mapa.grid(row=2, column=0, columnspan=6)

# RAMKA LISTA JEDNOSTEK
label_lista_jednostek = Label(ramka_jednostki, text="Lista jednostek policji")
label_lista_jednostek.grid(row=0, column=0, columnspan=2)

list_box_lista_jednostek = Listbox(ramka_jednostki)
list_box_lista_jednostek.grid(row=1, column=0, columnspan=2)

buttom_dodaj_jednostke = Button(ramka_jednostki, text="Dodaj jednostkę")
buttom_dodaj_jednostke.grid(row=2, column=0)

buttom_usun_jednostke = Button(ramka_jednostki, text="Usuń jednostkę")
buttom_usun_jednostke.grid(row=2, column=1)

buttom_aktualizuj_jednostke = Button(ramka_jednostki, text="Aktualizuj jednostkę")
buttom_aktualizuj_jednostke.grid(row=2, column=2)

#RAMKA FORMULARZ JEDNOSTEK
label_formularz_jednostek = Label(ramka_formularz_jednostki, text="Formularz - jednostki: ")
label_formularz_jednostek.grid(row=0, column=0, columnspan=2)

label_nazwa_jednostki = Label(ramka_formularz_jednostki, text= "Nazwa: ")
label_nazwa_jednostki.grid(row=1, column=0, sticky=W)

label_ulica_jednostki = Label(ramka_formularz_jednostki, text="Ulica: ")
label_ulica_jednostki.grid(row=2, column=0, sticky=W)

label_miasto_jednostki = Label(ramka_formularz_jednostki, text="Miasto: ")
label_miasto_jednostki.grid(row=3, column=0, sticky=W)

entry_nazwa_jednostki = Entry(ramka_formularz_jednostki)
entry_nazwa_jednostki.grid(row=1, column=1)

entry_ulica_jednostki = Entry(ramka_formularz_jednostki)
entry_ulica_jednostki.grid(row=2, column=1)

entry_miasto_jednostki = Entry(ramka_formularz_jednostki)
entry_miasto_jednostki.grid(row=3, column=1)

button_dodaj_jednostke = Button(ramka_formularz_jednostki, text="Dodaj obiekt")
button_dodaj_jednostke.grid(row=4, column=0, columnspan=2)


#RAMKA LISTA PRACOWNIKÓW
label_lista_pracownikow = Label(ramka_pracownicy, text="Lista pracowników policji")
label_lista_pracownikow.grid(row=0, column=0, columnspan=2)

list_box_lista_pracownikow = Listbox(ramka_pracownicy)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=2)

buttom_dodaj_pracownika= Button(ramka_pracownicy, text="Dodaj pracownika")
buttom_dodaj_pracownika.grid(row=2, column=0)

buttom_usun_pracownika = Button(ramka_pracownicy, text="Usuń pracownika")
buttom_usun_pracownika.grid(row=2, column=1)

buttom_aktualizuj_pracownika = Button(ramka_pracownicy, text="Aktualizuj pracownika")
buttom_aktualizuj_pracownika.grid(row=2, column=2)

#RAMKA FORMULARZ PRACOWNIKÓW
label_formularz_pracownicy = Label(ramka_formularz_pracownicy, text="Formularz - pracownicy: ")
label_formularz_pracownicy.grid(row=0, column=0, columnspan=2)

label_imie_pracownika = Label(ramka_formularz_pracownicy, text= "Imię: ")
label_imie_pracownika.grid(row=1, column=0, sticky=W)

label_nazwisko_pracownika = Label(ramka_formularz_pracownicy, text="Nazwisko: ")
label_nazwisko_pracownika.grid(row=2, column=0, sticky=W)

label_miasto_pracownika = Label(ramka_formularz_pracownicy, text="Miasto: ")
label_miasto_pracownika.grid(row=3, column=0, sticky=W)

entry_imie_pracownika = Entry(ramka_formularz_pracownicy)
entry_imie_pracownika.grid(row=1, column=1)

entry_nazwisko_pracownika = Entry(ramka_formularz_pracownicy)
entry_nazwisko_pracownika.grid(row=2, column=1)

entry_miasto_pracownika = Entry(ramka_formularz_pracownicy)
entry_miasto_pracownika.grid(row=3, column=1)

button_dodaj_pracownika = Button(ramka_formularz_pracownicy, text="Dodaj obiekt")
button_dodaj_pracownika.grid(row=4, column=0, columnspan=2)


#RAMKA LISTA INCYDERNTÓW
label_lista_incydentow = Label(ramka_incydenty, text="Lista incydentów")
label_lista_incydentow.grid(row=0, column=0, columnspan=2)

list_box_lista_incydentow = Listbox(ramka_incydenty)
list_box_lista_incydentow.grid(row=1, column=0, columnspan=2)

buttom_dodaj_incydent= Button(ramka_incydenty, text="Dodaj incydent")
buttom_dodaj_incydent.grid(row=2, column=0)

buttom_usun_incydent = Button(ramka_incydenty, text="Usuń incydent")
buttom_usun_incydent.grid(row=2, column=1)

buttom_aktualizuj_incydent = Button(ramka_incydenty, text="Aktualizuj incydent")
buttom_aktualizuj_incydent.grid(row=2, column=2)

#RAMKA FORMULARZ INCYDENTÓW
label_formularz_incydentów = Label(ramka_formularz_incydenty, text="Formularz - pracownicy: ")
label_formularz_incydentów.grid(row=0, column=0, columnspan=2)

label_nazwa_incydentu = Label(ramka_formularz_incydenty, text= "Nazwa: ")
label_nazwa_incydentu.grid(row=1, column=0, sticky=W)

# label_nazwisko_pracownika = Label(ramka_formularz_jednostki, text="Nazwisko: ")
# label_nazwisko_pracownika.grid(row=2, column=0, sticky=W)
#
# label_miasto_pracownika = Label(ramka_formularz_jednostki, text="Miasto: ")
# label_miasto_pracownika.grid(row=3, column=0, sticky=W)

entry_nazwa_incydentu = Entry(ramka_formularz_incydenty)
entry_nazwa_incydentu.grid(row=1, column=1)

# entry_nazwisko_pracownika = Entry(ramka_formularz_jednostki)
# entry_nazwisko_pracownika.grid(row=2, column=1)
#
# entry_miasto_pracownika = Entry(ramka_formularz_jednostki)
# entry_miasto_pracownika.grid(row=3, column=1)

button_dodaj_pracownika = Button(ramka_formularz_incydenty, text="Dodaj obiekt")
button_dodaj_pracownika.grid(row=2, column=0, columnspan=2)


# RAMKA SZCZEGÓŁY OBIEKTU
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu: ")
label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)

label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Imie: ")
label_imie_szczegoly_obiektu.grid(row=1, column=0)

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)

label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Lokalizacja: ")
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=2)

label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=3)

label_posty_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Posty: ")
label_posty_szczegoly_obiektu.grid(row=1, column=4)

label_posty_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_posty_szczegoly_obiektu_wartosc.grid(row=1, column=5)


# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1025, height=600, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0)


root.mainloop()