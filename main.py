from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

areas: list =[]
clients:list=[]
workers:list=[]
data_areas =[]
data_workers=[]
data_clients =[]
area_markers = []

class Areas:
    def __init__(self, area_name, area_location):
        self.area_name = area_name
        self.area_location = area_location

    def get_coordinates(self) -> list:
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.area_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd podczas pobierania współrzędnych: {e}")
            return [0.0, 0.0]


class client:
    def __init__(self, client_name, client_surname, client_id):
        self.client_name = client_name
        self.client_surname = client_surname
        self.client_id = client_id



class Workers:
    def __init__(self, worker_name, worker_surname, worker_id):
        self.worker_name = worker_name
        self.worker_surname = worker_surname
        self.worker_id = worker_id



root = Tk()
root.geometry("1200x760")
root.title("Ramka")


ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0,columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

def dodaj_wszystko():
    text_location = entry_area_location.get().strip()
    text_areas = entry_name_areas.get().strip()
    text_id = entry_name_id.get().strip()
    text_workers = entry_name_workers.get().strip()
    text_workers_surname = entry_surname_workers.get().strip()
    text_clientnical = entry_name_client.get().strip()
    text_client_surname = entry_surname_client.get().strip()

    ar = areas(text_areas, text_location)
    areas.append(ar)

    coordinates = ar.get_coordinates()
    if coordinates != [0.0, 0.0]:
        marker = map_widget.set_marker(coordinates[0], coordinates[1], text=text_areas)
        area_markers.append(marker)
    else:
        area_markers.append(None)
    pozycja = listbox_lista_kamer.size() + 1
    wiersz = f"{pozycja}. {text_areas} ({text_id})"
    listbox_lista_kamer.insert(END, wiersz)
    data_areas.append((text_areas, text_id))
    entry_name_areas.delete(0, END)
    entry_name_id.delete(0, END)
    entry_area_location.delete(0, END)

    worker = Workers(text_workers, text_workers_surname, "-")
    workers.append(worker)
    pozycja = listbox_lista_pracownikow.size() + 1
    wiersz = f"{pozycja}. {text_workers} {text_workers_surname}"
    listbox_lista_pracownikow.insert(END, wiersz)
    data_workers.append((text_workers, text_workers_surname))
    entry_name_workers.delete(0, END)
    entry_surname_workers.delete(0, END)

    client_obj = client(text_clientnical, text_client_surname, "-")
    clients.append(client_obj)
    pozycja = listbox_lista_klientow.size() + 1
    wiersz = f"{pozycja}. {text_clientnical} {text_client_surname}"
    listbox_lista_klientow.insert(END, wiersz)
    data_clients.append((text_clientnical, text_client_surname))
    entry_name_client.delete(0, END)
    entry_surname_client.delete(0, END)
def remove_areas():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]

        marker = area_markers.pop(i)
        if marker:
            marker.delete()

        data_areas.pop(i)
        areas.pop(i)

        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, id_) in enumerate(data_areas, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa}  {id_}")

def edit_areas():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        name, id_ = data_areas[i]
        location = areas[i].area_location

        entry_name_areas.delete(0, END)
        entry_name_areas.insert(0, name)

        entry_name_id.delete(0, END)
        entry_name_id.insert(0, id_)

        entry_area_location.delete(0, END)
        entry_area_location.insert(0, location)

        edytowany_index.set(i)
        button_dodaj_obiekt.config(text="Zapisz", command=update_areas)

def update_areas():
    i = edytowany_index.get()
    new_name = entry_name_areas.get().strip()
    new_id = entry_name_id.get().strip()
    new_location = entry_area_location.get().strip()

    if new_name and new_location:
        # Aktualizacja danych tekstowych
        data_areas[i] = (new_name, new_id)
        areas[i].area_name = new_name
        areas[i].area_location = new_location

        # Usunięcie starego markera
        old_marker = area_markers[i]
        if old_marker:
            old_marker.delete()

        # Nowe współrzędne
        coordinates = areas[i].get_coordinates()
        if coordinates != [0.0, 0.0]:
            new_marker = map_widget.set_marker(coordinates[0], coordinates[1], text=new_name)
            area_markers[i] = new_marker
        else:
            print("Nie udało się pobrać współrzędnych nowej lokalizacji.")
            area_markers[i] = None

        # Odświeżenie listy kamer
        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, id_) in enumerate(data_areas, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa}  {id_}")

        # Reset formularza
        entry_name_areas.delete(0, END)
        entry_name_id.delete(0, END)
        entry_area_location.delete(0, END)
        button_dodaj_obiekt.config(text="Zapisz", command=dodaj_wszystko)


def show_areas():

    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        name, id_ = data_areas[i]
        label_szczegoly_area_name_wartosc.config(text=name)
        label_szczegoly_area_id_wartosc.config(text=id_)


# ramka_lista_kamer
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista obiektów wypoczynkowych")
label_lista_obiektow.grid(row=0, column=0,columnspan=2)
listbox_lista_kamer = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_kamer.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_areas)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_areas)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_areas)
button_edytuj_obiekt.grid(row=2, column=2)

def remove_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        data_workers.pop(i)
        listbox_lista_pracownikow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko}")

def edit_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko = data_workers[i]

        entry_name_workers.delete(0, END)
        entry_name_workers.insert(0, imie)

        entry_surname_workers.delete(0, END)
        entry_surname_workers.insert(0, nazwisko)

        edytowany_index.set(i)
        edytowany_typ.set("pracownik")

        button_dodaj_obiekt.config(text="Zapisz", command=update_worker)

def update_worker():
    i = edytowany_index.get()
    new_imie = entry_name_workers.get()
    new_nazwisko = entry_surname_workers.get()

    if new_imie.strip():
        data_workers[i] = (new_imie, new_nazwisko)

        listbox_lista_pracownikow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko}")

        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)

        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

def show_workers():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        name, surname = data_workers[i]
        label_szczegoly_worker_name_wartosc.config(text=name)
        label_szczegoly_worker_surname_wartosc.config(text=surname)

#ramka_lista_PRACOWNIKÓW
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_obiektow_klient.grid(row=0, column=3,columnspan=2)
listbox_lista_pracownikow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_pracownikow.grid(row=1, column=3, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_workers)
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=3)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_worker)
button_usun_obiekt_klient.grid(row=2, column=4)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_worker)
button_edytuj_obiekt_klient.grid(row=2, column=5)

def remove_client():
    selection = listbox_lista_klientow.curselection()
    if selection:
        i = selection[0]
        data_clients.pop(i)
        listbox_lista_klientow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_clients, start=1):
            listbox_lista_klientow.insert(END, f"{idx}. {imie} {nazwisko}")

def edit_client():
    selection = listbox_lista_klientow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko = data_clients[i]

        entry_name_client.delete(0, END)
        entry_name_client.insert(0, imie)

        entry_surname_client.delete(0, END)
        entry_surname_client.insert(0, nazwisko)

        edytowany_index.set(i)
        edytowany_typ.set("konserwator")

        button_dodaj_obiekt.config(text="Zapisz", command=update_client)

def update_client():
    i = edytowany_index.get()
    new_imie = entry_name_client.get()
    new_nazwisko = entry_surname_client.get()

    if new_imie.strip():
        data_clients[i] = (new_imie, new_nazwisko)

        listbox_lista_klientow.delete(0, END)
        for idx, (imie, nazwisko) in enumerate(data_clients, start=1):
            listbox_lista_klientow.insert(END, f"{idx}. {imie} {nazwisko}")

        entry_name_client.delete(0, END)
        entry_surname_client.delete(0, END)

        button_dodaj_obiekt.config(text="Dodaj", command=dodaj_wszystko)

def show_clients():
    selection = listbox_lista_klientow.curselection()
    if selection:
        i = selection[0]
        name, surname = data_clients[i]
        label_szczegoly_client_name_wartosc.config(text=name)
        label_szczegoly_client_surname_wartosc.config(text=surname)

#ramka_lista_konserwatorów
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista klientów")
label_lista_obiektow_klient.grid(row=0, column=6,columnspan=2)
listbox_lista_klientow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_klientow.grid(row=1, column=6, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_clients)
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=6)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_client)
button_usun_obiekt_klient.grid(row=2, column=7)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_client)
button_edytuj_obiekt_klient.grid(row=2,column=8)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_area_coords = Label(ramka_formularz, text="Nazwa miejscowości:")
label_area_coords.grid(row=1, column=0, sticky=W)
label_area_name = Label(ramka_formularz, text="Nazwa obiektu wypoczynkowego:")
label_area_name.grid(row=2, column=0, sticky=W)
label_id=Label(ramka_formularz, text="Telefon kontaktowy")
label_id.grid(row=3, column=0)
label_name_workers=Label(ramka_formularz, text="Imie pracownika:")
label_name_workers.grid(row=4, column=0)
label_surname_workers=Label(ramka_formularz, text="Nazwisko Pracownika:")
label_surname_workers.grid(row=5, column=0)
label_name_client=Label(ramka_formularz, text="Imie klienta:")
label_name_client.grid(row=6, column=0)
label_surname_client=Label(ramka_formularz, text="Nazwisko klienta:")
label_surname_client.grid(row=7, column=0)
button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", command=dodaj_wszystko)
button_dodaj_obiekt.grid(row=8, column=0, columnspan=2)

entry_area_location = Entry(ramka_formularz)
entry_area_location.grid(row=1, column=1)

entry_name_areas = Entry(ramka_formularz)
entry_name_areas.grid(row=2, column=1)

entry_name_id = Entry(ramka_formularz)
entry_name_id.grid(row=3, column=1)

entry_name_workers = Entry(ramka_formularz)
entry_name_workers.grid(row=4, column=1)

entry_surname_workers = Entry(ramka_formularz)
entry_surname_workers.grid(row=5, column=1)

entry_name_client = Entry(ramka_formularz)
entry_name_client.grid(row=6, column=1)

entry_surname_client = Entry(ramka_formularz)
entry_surname_client.grid(row=7, column=1)


edytowany_typ = StringVar(value="")
edytowany_index = IntVar(value=-1)


label_szczegoly_area_name = Label(ramka_szczegoly_obiektow, text="Nazwa obiektu:")
label_szczegoly_area_name.grid(row=0, column=0)
label_szczegoly_area_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_area_name_wartosc.grid(row=0, column=1)

label_szczegoly_area_id = Label(ramka_szczegoly_obiektow, text="Telefon kontaktowy:")
label_szczegoly_area_id.grid(row=0, column=2)
label_szczegoly_area_id_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_area_id_wartosc.grid(row=0, column=3)

label_szczegoly_worker_name = Label(ramka_szczegoly_obiektow, text="Imię pracownika:")
label_szczegoly_worker_name.grid(row=0, column=4)
label_szczegoly_worker_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_worker_name_wartosc.grid(row=0, column=5)

label_szczegoly_worker_surname = Label(ramka_szczegoly_obiektow, text="Nazwisko pracownika:")
label_szczegoly_worker_surname.grid(row=0, column=6)
label_szczegoly_worker_surname_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_worker_surname_wartosc.grid(row=0, column=7)

label_szczegoly_client_name = Label(ramka_szczegoly_obiektow, text="Imie klienta:")
label_szczegoly_client_name.grid(row=0, column=8)
label_szczegoly_client_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_client_name_wartosc.grid(row=0, column=9)

label_szczegoly_client_surname = Label(ramka_szczegoly_obiektow, text="Nazwisko klienta:")
label_szczegoly_client_surname.grid(row=0, column=10)
label_szczegoly_client_surname_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_client_surname_wartosc.grid(row=0, column=11)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=6)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)



root.mainloop()
