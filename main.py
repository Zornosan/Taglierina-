from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock

class ContaMetriApp(App):
    def build(self):
        # Variabili
        self.metri = 0
        self.velocita = 10  # velocità iniziale in metri/minuto
        self.metri_fermata = 0
        self.differenza = 0
        self.contando = False
        self.active_input = "metri_iniziali"  # Campo attivo predefinito
        self.clear_on_next_input = False  # Flag per cancellare il valore esistente al primo input

        # Layout principale
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input per i metri iniziali
        layout.add_widget(Label(text="Metri Inizio:"))
        self.input_metri_iniziali = Label(text="0", color=(1, 1, 0, 1))  # Colore evidenziato iniziale
        layout.add_widget(self.input_metri_iniziali)

        # Input per la velocità iniziale
        layout.add_widget(Label(text="Velocità Iniziale (m/min):"))
        self.input_velocita = Label(text="10", color=(1, 1, 1, 1))  # Colore normale
        layout.add_widget(self.input_velocita)

        # Cursore per regolare la velocità
        layout.add_widget(Label(text="Cursore Velocità"))
        self.slider_velocita = Slider(min=0, max=800, value=self.velocita)
        self.slider_velocita.bind(value=self.on_slider_value_change)
        layout.add_widget(self.slider_velocita)

        # Input per i metri di fermata
        layout.add_widget(Label(text="Metri di Fermata:"))
        self.input_metri_fermata = Label(text="0", color=(1, 1, 1, 1))  # Colore normale
        layout.add_widget(self.input_metri_fermata)

        # Differenza tra Metri Percorsi e Metri di Fermata
        self.label_differenza = Label(text="Differenza: 0.0")
        layout.add_widget(self.label_differenza)

        # Pulsanti Avvio, Stop, Reset, Play/Start e Tab
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.button_avvio = Button(text="Avvio")
        self.button_avvio.bind(on_press=self.start_counting)
        button_layout.add_widget(self.button_avvio)
        
        self.button_stop = Button(text="Stop")
        self.button_stop.bind(on_press=self.stop_counting)
        button_layout.add_widget(self.button_stop)
        
        self.button_reset = Button(text="Reset")
        self.button_reset.bind(on_press=self.reset)
        button_layout.add_widget(self.button_reset)
        
        # Pulsante Play/Start per mettere in pausa e riprendere il conteggio
        self.button_play_start = Button(text="Play")
        self.button_play_start.bind(on_press=self.toggle_counting)
        button_layout.add_widget(self.button_play_start)
        
        # Pulsante Tab per cambiare il campo attivo
        self.button_tab = Button(text="Tab")
        self.button_tab.bind(on_press=self.switch_active_input)
        button_layout.add_widget(self.button_tab)
        
        layout.add_widget(button_layout)

        # Label per mostrare i metri percorsi, con testo più grande
        self.label_metri = Label(text="Metri Percorsi: 0.0", font_size=32, bold=True)
        layout.add_widget(self.label_metri)

        # Tastiera numerica simulata
        keyboard_layout = GridLayout(cols=3, size_hint_y=None, height=200)
        for i in range(1, 10):
            button = Button(text=str(i), font_size=24)
            button.bind(on_press=self.on_keyboard_press)
            keyboard_layout.add_widget(button)
        
        button_zero = Button(text="0", font_size=24)
        button_zero.bind(on_press=self.on_keyboard_press)
        keyboard_layout.add_widget(button_zero)

        button_clear = Button(text="C", font_size=24)
        button_clear.bind(on_press=self.on_clear_press)
        keyboard_layout.add_widget(button_clear)

        layout.add_widget(keyboard_layout)

        return layout

    def switch_active_input(self, instance):
        # Cambia il campo attivo in sequenza tra metri_iniziali, velocita, e metri_fermata
        # Ripristina i colori
        self.input_metri_iniziali.color = (1, 1, 1, 1)
        self.input_velocita.color = (1, 1, 1, 1)
        self.input_metri_fermata.color = (1, 1, 1, 1)

        # Cambia il campo attivo e applica il colore evidenziato
        if self.active_input == "metri_iniziali":
            self.active_input = "velocita"
            self.input_velocita.color = (1, 1, 0, 1)  # Colore evidenziato giallo
        elif self.active_input == "velocita":
            self.active_input = "metri_fermata"
            self.input_metri_fermata.color = (1, 1, 0, 1)  # Colore evidenziato giallo
        else:
            self.active_input = "metri_iniziali"
            self.input_metri_iniziali.color = (1, 1, 0, 1)  # Colore evidenziato giallo

        # Imposta il flag per cancellare al prossimo input
        self.clear_on_next_input = True

    def on_keyboard_press(self, instance):
        # Cancella il testo se il flag è attivo
        if self.clear_on_next_input:
            if self.active_input == "metri_iniziali":
                self.input_metri_iniziali.text = ""
            elif self.active_input == "velocita":
                self.input_velocita.text = ""
            elif self.active_input == "metri_fermata":
                self.input_metri_fermata.text = ""
            self.clear_on_next_input = False  # Resetta il flag dopo la cancellazione

        # Aggiunge il numero al campo attivo
        if self.active_input == "metri_iniziali":
            current_text = self.input_metri_iniziali.text
            self.input_metri_iniziali.text = current_text + instance.text
        elif self.active_input == "velocita":
            current_text = self.input_velocita.text
            self.input_velocita.text = current_text + instance.text
            # Aggiorna la velocità e il cursore quando viene modificata tramite tastiera
            self.update_speed(float(self.input_velocita.text))
        elif self.active_input == "metri_fermata":
            current_text = self.input_metri_fermata.text
            self.input_metri_fermata.text = current_text + instance.text

    def on_clear_press(self, instance):
        # Cancella il campo attivo
        if self.active_input == "metri_iniziali":
            self.input_metri_iniziali.text = ""
        elif self.active_input == "velocita":
            self.input_velocita.text = ""
        elif self.active_input == "metri_fermata":
            self.input_metri_fermata.text = ""

    def on_slider_value_change(self, instance, value):
        self.update_speed(value)

    def update_speed(self, value):
        self.velocita = value
        self.input_velocita.text = str(int(value))
        self.slider_velocita.value = value

    def start_counting(self, instance):
        # Solo la prima volta, avvia il conteggio dai metri di partenza
        if not self.contando:
            self.metri = float(self.input_metri_iniziali.text) if self.input_metri_iniziali.text else 0
            self.metri_fermata = float(self.input_metri_fermata.text) if self.input_metri_fermata.text else 0
            self.velocita = float(self.input_velocita.text) if self.input_velocita.text else 10
            self.update_speed(self.velocita)  # Sincronizza velocità e cursore

            self.contando = True
            Clock.schedule_interval(self.update_meters, 0.1)
            self.button_play_start.text = "Pause"  # Imposta il testo su "Pause"

    def toggle_counting(self, instance):
        # Alterna tra play e pausa
        if self.contando:
            self.contando = False
            Clock.unschedule(self.update_meters)
            self.button_play_start.text = "Play"  # Cambia il testo a "Play" quando è in pausa
        else:
            self.contando = True
            Clock.schedule_interval(self.update_meters, 0.1)
            self.button_play_start.text = "Pause"  # Cambia il testo a "Pause" quando è in esecuzione

    def stop_counting(self, instance):
        # Ferma il conteggio completamente
        if self.contando:
            self.contando = False
            Clock.unschedule(self.update_meters)
            self.button_play_start.text = "Play"  # Resetta il testo a "Play" per il prossimo avvio

    def reset(self, instance):
        # Resetta tutte le variabili
        self.metri = 0
        self.velocita = 10
        self.metri_fermata = 0
        self.differenza = 0
        self.input_metri_iniziali.text = "0"
        self.input_velocita.text = "10"
        self.input_metri_fermata.text = "0"
        self.label_metri.text = "Metri Percorsi: 0.0"
        self.label_differenza.text = "Differenza: 0.0"
        self.slider_velocita.value = 10  # Reset del cursore alla velocità iniziale
        self.update_speed(10)  # Sincronizza velocità e cursore
        self.button_play_start.text = "Play"  # Resetta il testo a "Play"
        self.contando = False
        Clock.unschedule(self.update_meters)

    def update_meters(self, dt):
        if self.contando:
            # Calcola i metri da aggiungere ogni 0.1 secondi
            metri_da_aggiungere = (self.velocita / 60) * 0.1
            self.metri += metri_da_aggiungere
            # Aggiorna la visualizzazione dei metri percorsi e della differenza
            self.label_metri.text = f"Metri Percorsi: {self.metri:.1f}"
            self.differenza = self.metri - self.metri_fermata
            self.label_differenza.text = f"Differenza: {self.differenza:.1f}"

if __name__ == "__main__":
    ContaMetriApp().run()