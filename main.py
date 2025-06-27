from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox
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
    def __init__(self, area_name, area_location, coordinates=None):
        self.area_name = area_name
        self.area_location = area_location
        self.coordinates = coordinates if coordinates else self.get_coordinates()

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


class Client:
    def __init__(self, client_name, client_surname, client_location,client_area, coordinates=None):
        self.client_name = client_name
        self.client_surname = client_surname
        self.client_location = client_location
        self.client_area=client_area
        self.coordinates = coordinates if coordinates else self.get_coordinates()

    def get_coordinates(self) -> list:
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.client_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd podczas pobierania współrzędnych: {e}")
            return [0.0, 0.0]







class Workers:
    def __init__(self, worker_name, worker_surname, worker_location,worker_area, coordinates=None):
        self.worker_name = worker_name
        self.worker_surname = worker_surname
        self.worker_location = worker_location
        self.worker_area = worker_area
        self.coordinates = coordinates if coordinates else self.get_coordinates()

    def get_coordinates(self) -> list:
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.worker_location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
            latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except Exception as e:
            print(f"Błąd podczas pobierania współrzędnych: {e}")
            return [0.0, 0.0]



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
ramka_mapa.grid(row=2, column=0,)

def dodaj_serwis():
    nazwa = entry_name_areas.get().strip()
    lokalizacja = entry_area_location.get().strip()
    if nazwa and lokalizacja:
        new_serwis = Areas(nazwa, lokalizacja)
        areas.append(new_serwis)
        data_areas.append((nazwa, lokalizacja))

        listbox_lista_kamer.insert(END, f"{len(data_areas)}. {nazwa} - {lokalizacja}")

        entry_name_areas.delete(0, END)
        entry_area_location.delete(0, END)

def dodaj_klienta():
    imie = entry_name_client.get().strip()
    nazwisko = entry_surname_client.get().strip()
    miejsce = entry_location_client.get().strip()
    teren=entry_name_areas.get().strip()

    if imie and nazwisko and miejsce and teren:
        nowy_klient = Client(imie, nazwisko, miejsce, teren)
        clients.append(nowy_klient)

        data_clients.append((imie, nazwisko, miejsce, teren))
        listbox_lista_klientow.insert(END, f"{len(data_clients)}. {imie} {nazwisko} {teren}")

        entry_name_client.delete(0, END)
        entry_surname_client.delete(0, END)
        entry_location_client.delete(0, END)

def dodaj_pracownik():
    imie = entry_name_workers.get().strip()
    nazwisko = entry_surname_workers.get().strip()
    miejsce = entry_location_workers.get().strip()
    teren=entry_name_areas.get().strip()

    if imie and nazwisko and miejsce and teren:
        nowy_pracownik = Workers(imie, nazwisko, miejsce, teren)
        workers.append(nowy_pracownik)

        # Dodaj do danych i listboxa
        data_workers.append((imie, nazwisko,miejsce, teren))
        listbox_lista_pracownikow.insert(END, f"{len(data_workers)}. {imie} {nazwisko}")

        # Wyczyść formularz
        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)
        entry_location_workers.delete(0, END)

def remove_areas():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        areas.pop(i)
        data_areas.pop(i)

        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, lokalizacja) in enumerate(data_areas, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa} - {lokalizacja}")

def edit_areas():
    selection = listbox_lista_kamer.curselection()
    if selection:
        i = selection[0]
        name, location = data_areas[i]

        entry_name_areas.delete(0, END)
        entry_name_areas.insert(0, name)

        entry_area_location.delete(0, END)
        entry_area_location.insert(0, location)

        edytowany_index.set(i)
        edytowany_typ.set("serwis")

        button_dodaj_obiekt.config(text="Zapisz", command=update_areas)

def update_areas():
    i = edytowany_index.get()
    new_name = entry_name_areas.get().strip()
    new_location = entry_area_location.get().strip()

    if new_name and new_location:
        data_areas[i] = (new_name, new_location)
        areas[i].area_name = new_name
        areas[i].area_location = new_location
        areas[i].coordinates = areas[i].get_coordinates()

        # Odświeżenie listy
        listbox_lista_kamer.delete(0, END)
        for idx, (nazwa, lokalizacja) in enumerate(data_areas, start=1):
            listbox_lista_kamer.insert(END, f"{idx}. {nazwa} - {lokalizacja}")

        # Reset formularza
        entry_name_areas.delete(0, END)
        entry_area_location.delete(0, END)

        button_dodaj_obiekt.config(text="Zapisz dane", command=zapisz_obiekt)






# ramka_lista_kamer
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista obiektów wypoczynkowych")
label_lista_obiektow.grid(row=0, column=0,columnspan=2)
listbox_lista_kamer = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_kamer.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text='Dodaj obiekt', command=dodaj_serwis)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_areas)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_areas)
button_edytuj_obiekt.grid(row=2, column=2)

def remove_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]

        # Usuń z listy danych i obiektów
        del data_workers[i]
        del workers[i]


        listbox_lista_pracownikow.delete(i)
        for idx, (imie, nazwisko) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko}")


def edit_worker():
    selection = listbox_lista_pracownikow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko, miejsce, teren = data_workers[i]

        entry_name_workers.delete(0, END)
        entry_name_workers.insert(0, imie)

        entry_surname_workers.delete(0, END)
        entry_surname_workers.insert(0, nazwisko)

        entry_location_workers.delete(0, END)
        entry_location_workers.insert(0, miejsce)

        entry_name_areas.delete(0, END)
        entry_name_areas.insert(0, teren)

        edytowany_index.set(i)
        edytowany_typ.set("worker")

        button_dodaj_obiekt.config(text="Zapisz", command=update_worker)

def update_worker():
    i = edytowany_index.get()
    new_imie = entry_name_workers.get().strip()
    new_nazwisko = entry_surname_workers.get().strip()
    new_miejsce = entry_location_workers.get().strip()
    new_teren = entry_name_areas.get().strip()

    if new_imie and new_nazwisko and new_miejsce and new_teren:
        data_workers[i] = (new_imie, new_nazwisko, new_miejsce, new_teren)
        workers[i].worker_name = new_imie
        workers[i].worker_surname = new_nazwisko
        workers[i].worker_location = new_miejsce
        workers[i].worker_area = new_teren

        listbox_lista_pracownikow.delete(0, END)
        for idx, (imie, nazwisko, miejsce, teren) in enumerate(data_workers, start=1):
            listbox_lista_pracownikow.insert(END, f"{idx}. {imie} {nazwisko} ({teren})")

        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)
        entry_location_workers.delete(0, END)
        entry_name_areas.delete(0, END)

        button_dodaj_obiekt.config(text="Zapisz dane", command=zapisz_obiekt)


#ramka_lista_PRACOWNIKÓW
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_obiektow_klient.grid(row=0, column=3,columnspan=2)
listbox_lista_pracownikow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_pracownikow.grid(row=1, column=3, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Dodaj pracownika', command=dodaj_pracownik)
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=3)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_worker)
button_usun_obiekt_klient.grid(row=2, column=4)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_worker)
button_edytuj_obiekt_klient.grid(row=2, column=5)

def remove_client():
    selection = listbox_lista_klientow.curselection()
    if selection:
        i = selection[0]

        # Usuń z listy danych i obiektów
        del data_clients[i]
        del clients[i]

        i=selection[0]
        listbox_lista_klientow.delete(i)
        for idx, (imie, nazwisko) in enumerate(data_clients, start=1):
            listbox_lista_klientow.insert(END, f"{idx}. {imie} {nazwisko}")

def edit_client():
    selection = listbox_lista_klientow.curselection()
    if selection:
        i = selection[0]
        imie, nazwisko, miejsce, teren = data_clients[i]

        entry_name_client.delete(0, END)
        entry_name_client.insert(0, imie)

        entry_surname_client.delete(0, END)
        entry_surname_client.insert(0, nazwisko)

        entry_location_client.delete(0, END)
        entry_location_client.insert(0, miejsce)

        entry_name_areas.delete(0, END)
        entry_name_areas.insert(0, teren)

        edytowany_index.set(i)
        edytowany_typ.set("client")

        button_dodaj_obiekt.config(text="Zapisz", command=update_client)

def update_client():
    i = edytowany_index.get()
    new_imie = entry_name_client.get().strip()
    new_nazwisko = entry_surname_client.get().strip()
    new_miejsce = entry_location_client.get().strip()
    new_teren = entry_name_areas.get().strip()

    if new_imie and new_nazwisko and new_miejsce and new_teren:
        data_clients[i] = (new_imie, new_nazwisko, new_miejsce, new_teren)
        clients[i].client_name = new_imie
        clients[i].client_surname = new_nazwisko
        clients[i].client_location = new_miejsce
        clients[i].client_area = new_teren

        listbox_lista_klientow.delete(0, END)
        for idx, (imie, nazwisko, miejsce, teren) in enumerate(data_clients, start=1):
            listbox_lista_klientow.insert(END, f"{idx}. {imie} {nazwisko} ({teren})")

        entry_name_client.delete(0, END)
        entry_surname_client.delete(0, END)
        entry_location_client.delete(0, END)
        # Możemy też zostawić teren w polu, jeśli chcesz
        entry_name_areas.delete(0, END)

        button_dodaj_obiekt.config(text="Zapisz dane", command=zapisz_obiekt)


def zapisz_obiekt():
    # Pobierz wartości z pól formularza
    name_area = entry_name_areas.get().strip()
    location_area = entry_area_location.get().strip()

    name_worker = entry_name_workers.get().strip()
    surname_worker = entry_surname_workers.get().strip()
    location_worker = entry_location_workers.get().strip()

    name_client = entry_name_client.get().strip()
    surname_client = entry_surname_client.get().strip()
    location_client = entry_location_client.get().strip()

    # Sprawdź, jaki typ danych chcemy zapisać (wykorzystując zmienną edytowany_typ)
    typ = edytowany_typ.get()

    if typ == "serwis":
        if not (name_area and location_area):
            return
        new_object = Areas(name_area, location_area)
        areas.append(new_object)
        data_areas.append((name_area, location_area))
        listbox_lista_kamer.insert(END, f"{len(data_areas)}. {name_area} - {location_area}")

        # Wyczyść pola formularza
        entry_name_areas.delete(0, END)
        entry_area_location.delete(0, END)

    elif typ == "worker":
        if not (name_worker and surname_worker and location_worker):
            return
        new_object = Workers(name_worker, surname_worker, location_worker, location_worker)
        workers.append(new_object)
        data_workers.append((name_worker, surname_worker, location_worker, location_worker))
        listbox_lista_pracownikow.insert(END, f"{len(data_workers)}. {name_worker} {surname_worker}")

        entry_name_workers.delete(0, END)
        entry_surname_workers.delete(0, END)
        entry_location_workers.delete(0, END)

    elif typ == "client":
        if not (name_client and surname_client and location_client):
            return
        new_object = Client(name_client, surname_client, location_client, location_client)
        clients.append(new_object)
        data_clients.append((name_client, surname_client, location_client, location_client))
        listbox_lista_klientow.insert(END, f"{len(data_clients)}. {name_client} {surname_client}")

        entry_name_client.delete(0, END)
        entry_surname_client.delete(0, END)
        entry_location_client.delete(0, END)

    else:
        # Domyślnie dodajemy obiekt typu Areas (serwis) jeśli typ nie został określony
        if not (name_area and location_area):
            return
        new_object = Areas(name_area, location_area)
        areas.append(new_object)
        data_areas.append((name_area, location_area))
        listbox_lista_kamer.insert(END, f"{len(data_areas)}. {name_area} - {location_area}")
        entry_name_areas.delete(0, END)
        entry_area_location.delete(0, END)

    # Dodaj marker na mapie
    if hasattr(new_object, "coordinates"):
        latitude, longitude = new_object.coordinates
        map_widget.set_marker(latitude, longitude, text=name_area if typ == "serwis" else
                                                f"{name_worker} {surname_worker}" if typ == "worker" else
                                                f"{name_client} {surname_client}")

    # Resetuj zmienne edytowany_typ i edytowany_index
    edytowany_typ.set("")
    edytowany_index.set(-1)

    # Przywróć przycisk do domyślnego stanu
    button_dodaj_obiekt.config(text="Zapisz dane", command=zapisz_obiekt)
def pokaz_mapę_terenów():
    map_widget.delete_all_marker()
    for area in areas:
        lat, lon = area.coordinates
        map_widget.set_marker(lat, lon, text=f"Teren: {area.area_name}")

def pokaz_mapę_pracowników():
    map_widget.delete_all_marker()
    for worker in workers:
        lat, lon = worker.coordinates
        map_widget.set_marker(lat, lon, text=f"Pracownik: {worker.worker_name} {worker.worker_surname}")

def pokaz_mapę_użytkowników_wybranego_terenu():
    selection = listbox_lista_kamer.curselection()
    if not selection:
        messagebox.showwarning("Uwaga", "Wybierz teren z listy")
        return
    i = selection[0]
    wybrany_teren = areas[i]
    map_widget.delete_all_marker()

    for client in clients:
        if client.client_area == wybrany_teren.area_name and hasattr(client, "coordinates") and client.coordinates:
            lat, lon = client.coordinates
            map_widget.set_marker(lat, lon, text=f"Klient: {client.client_name} {client.client_surname}")

def pokaz_mapę_pracowników_wybranego_terenu():
    selection = listbox_lista_kamer.curselection()
    if not selection:
        messagebox.showwarning("Uwaga", "Wybierz teren z listy")
        return
    i = selection[0]
    wybrany_teren = areas[i]
    map_widget.delete_all_marker()

    for worker in workers:
        if worker.worker_area == wybrany_teren.area_name and hasattr(worker, "coordinates") and worker.coordinates:
            lat, lon = worker.coordinates
            map_widget.set_marker(lat, lon, text=f"Pracownik: {worker.worker_name} {worker.worker_surname}")


# ramka_lista_klientow
label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista klientów")
label_lista_obiektow_klient.grid(row=0, column=6,columnspan=2)
listbox_lista_klientow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_klientow.grid(row=1, column=6, columnspan=3)
button_pokaz_szczegoly_obiektu_klient = Button(ramka_lista_obiektow, text='Dodaj klienta', command=dodaj_klienta)
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=6)
button_usun_obiekt_klient = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_client)
button_usun_obiekt_klient.grid(row=2, column=7)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_client)
button_edytuj_obiekt_klient.grid(row=2,column=8)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_area_coords = Label(ramka_formularz, text="Lokalizacja obiektu wypoczynkowego:")
label_area_coords.grid(row=1, column=0, sticky=W)
label_area_name = Label(ramka_formularz, text="Nazwa obiektu wypoczynkowego:")
label_area_name.grid(row=2, column=0, sticky=W)
label_name_workers=Label(ramka_formularz, text="Imie pracownika:")
label_name_workers.grid(row=3, column=0)
label_surname_workers=Label(ramka_formularz, text="Nazwisko Pracownika:")
label_surname_workers.grid(row=4, column=0)
label_worker_coords=Label(ramka_formularz,text='MIejsce zamieszkania pracownika:')
label_worker_coords.grid(row=5, column=0)
label_name_client=Label(ramka_formularz, text="Imie klienta:")
label_name_client.grid(row=6, column=0)
label_surname_client=Label(ramka_formularz, text="Nazwisko klienta:")
label_surname_client.grid(row=7, column=0)
label_client_coords=Label(ramka_formularz,text='MIejsce zamieszkania klienta:')
label_client_coords.grid(row=8, column=0)
button_dodaj_obiekt=Button(ramka_formularz, text='Zapisz dane', command=zapisz_obiekt)
button_dodaj_obiekt.grid(row=9, column=0, columnspan=2)

entry_area_location = Entry(ramka_formularz)
entry_area_location.grid(row=1, column=1)

entry_name_areas = Entry(ramka_formularz)
entry_name_areas.grid(row=2, column=1)

entry_name_workers = Entry(ramka_formularz)
entry_name_workers.grid(row=3, column=1)

entry_surname_workers = Entry(ramka_formularz)
entry_surname_workers.grid(row=4, column=1)

entry_location_workers=Entry(ramka_formularz)
entry_location_workers.grid(row=5, column=1)

entry_name_client = Entry(ramka_formularz)
entry_name_client.grid(row=6, column=1)

entry_surname_client = Entry(ramka_formularz)
entry_surname_client.grid(row=7, column=1)

entry_location_client = Entry(ramka_formularz)
entry_location_client.grid(row=8, column=1)


edytowany_typ = StringVar(value="")
edytowany_index = IntVar(value=-1)


button_show_all_areas = Button(ramka_lista_obiektow, text="Pokaż wszystkie tereny", command=pokaz_mapę_terenów)
button_show_all_areas.grid(row=3, column=0)

button_show_all_workers = Button(ramka_lista_obiektow, text="Pokaż wszystkich pracowników", command=pokaz_mapę_pracowników)
button_show_all_workers.grid(row=3, column=3)

button_show_clients_in_area = Button(ramka_lista_obiektow, text="Klienci wybranego terenu", command=pokaz_mapę_użytkowników_wybranego_terenu)
button_show_clients_in_area.grid(row=4, column=0)

button_show_workers_in_area = Button(ramka_lista_obiektow, text="Pracownicy wybranego terenu", command=pokaz_mapę_pracowników_wybranego_terenu)
button_show_workers_in_area.grid(row=4, column=3)



# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=900, height=500)
map_widget.grid(row=0, column=0,sticky=W)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)

root.mainloop()
