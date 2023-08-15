import tkinter as tk
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

class NWSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShowLow's NWS Product Puller ver. alpha 0.0")

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        self.warning_button = tk.Button(self.menu_frame, text="NWS Products", command=self.show_warnings)
        self.warning_button.pack(pady=10)

        self.afd_button = tk.Button(self.menu_frame, text="NWS AFD's", command=self.show_afds)
        self.afd_button.pack(pady=10)

        self.radio_button = tk.Button(self.menu_frame, text="ShowLowfinity Weather Radio", command=self.show_radio)
        self.radio_button.pack(pady=10)

        self.warning_index = 0
        self.warnings = []

    def get_nws_warnings(self):
        base_url = 'https://api.weather.gov/alerts/active'
        url = f'{base_url}?status=actual&message_type=alert'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['features']

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return []

    def show_warnings(self):
        try:
            self.warnings = self.get_nws_warnings()
            self.warning_index = 0
            self.show_warning()
        except requests.exceptions.RequestException as e:
            print("Error occurred while fetching NWS warnings:", e)

    def show_warning(self):
        try:
            if self.warnings:
                warning = self.warnings[self.warning_index]
                properties = warning['properties']
                event = properties['event']
                headline = properties['headline']
                description = properties['description']
                instruction = properties.get('instruction', 'N/A')

                self.clear_frame(self.menu_frame)

                warning_label = tk.Label(self.menu_frame, text=f"Event: {event}\nHeadline: {headline}\nDescription: {description}\nPrecautionary/Prepardness: {instruction}", justify='left')
                warning_label.pack(pady=10)

                next_button = tk.Button(self.menu_frame, text="Next", command=self.next_warning)
                next_button.pack(side=tk.LEFT, padx=10)

                prev_button = tk.Button(self.menu_frame, text="Previous", command=self.prev_warning)
                prev_button.pack(side=tk.LEFT, padx=10)

                back_button = tk.Button(self.menu_frame, text="Back to Menu", command=self.show_menu)
                back_button.pack(side=tk.RIGHT, padx=10)
        except IndexError:
            print("No warnings available.")

    def next_warning(self):
        self.warning_index = (self.warning_index + 1) % len(self.warnings)
        self.show_warning()

    def prev_warning(self):
        self.warning_index = (self.warning_index - 1) % len(self.warnings)
        self.show_warning()

    def show_afds(self):
        try:
            self.clear_frame(self.menu_frame)
            self.afd_text = tk.Text(self.menu_frame, wrap=tk.WORD)
            self.afd_text.pack(fill=tk.BOTH, expand=True)

            back_button = tk.Button(self.menu_frame, text="Back to Menu", command=self.show_menu)
            back_button.pack(pady=10)

            self.fetch_and_display_afd()
        except Exception as e:
            print("An error occurred:", e)

    def fetch_and_display_afd(self):
        try:
            url = "https://forecast.weather.gov/product.php?site=NWS&issuedby=PSR&product=AFD&format=TXT&version=1&glossary=0"
            response = requests.get(url)
            response.raise_for_status()
            afd_data = response.text
            self.afd_text.config(state=tk.NORMAL)
            self.afd_text.delete("1.0", tk.END)
            self.afd_text.insert(tk.END, afd_data)
            self.afd_text.config(state=tk.DISABLED)
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching AFD: {e}")

    def show_radio(self):
        try:
            top = tk.Toplevel()
            top.title("ShowLowfinity Weather Radio")

            username_label = tk.Label(top, text="Staff Username:")
            username_label.pack()

            self.username_entry = tk.Entry(top)
            self.username_entry.pack()

            password_label = tk.Label(top, text="Password:")
            password_label.pack()

            self.password_entry = tk.Entry(top, show="*")
            self.password_entry.pack()

            login_button = tk.Button(top, text="Login", command=self.login)
            login_button.pack(pady=10)
        except Exception as e:
            print("An error occurred:", e)

    def login(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()

            if username == "ShowLowfinity" and password == "WSLFRadio(NRY!)": # Not fully ready yet, hence why its not secure, It just takes you to a cap page
                self.fetch_and_display_radio_warnings()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            print("An error occurred:", e)

    def fetch_and_display_radio_warnings(self):
        try:
            url = "https://alerts.weather.gov/cap/wwaatmget.php?x=AZC013&y=0"
            response = requests.get(url)
            response.raise_for_status()
            data = response.text
            self.clear_frame(self.menu_frame)

            warning_label = tk.Label(self.menu_frame, text=data, justify='left')
            warning_label.pack(pady=10)

            back_button = tk.Button(self.menu_frame, text="Back to Menu", command=self.show_menu)
            back_button.pack(side=tk.RIGHT, padx=10)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching warnings: {e}")

    def show_menu(self):
        try:
            self.clear_frame(self.menu_frame)

            self.warning_button = tk.Button(self.menu_frame, text="NWS Products", command=self.show_warnings)
            self.warning_button.pack(pady=10)

            self.afd_button = tk.Button(self.menu_frame, text="NWS AFD's", command=self.show_afds)
            self.afd_button.pack(pady=10)

            self.radio_button = tk.Button(self.menu_frame, text="ShowLowfinity Weather Radio", command=self.show_radio)
            self.radio_button.pack(pady=10)
        except Exception as e:
            print("An error occurred:", e)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def extract_afd_text(self, html_text):
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            content = soup.find('pre', class_='glossaryProduct').get_text()
            return content
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    try:
        app = NWSApp()
        app.root.mainloop()
    except Exception as e:
        print("An error occurred:", e)
