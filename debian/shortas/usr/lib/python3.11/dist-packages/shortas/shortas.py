import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox, QFileDialog, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSettings


def get_logo_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "shortaslo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/shortaslo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/shortaslo.png"
    elif os.path.exists("shortaslo.png"):
        return "shortaslo.png"
    return None


def get_icon_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "shortaslo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/shortaslo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/shortaslo.png"
    return None


LOGO_PATH = get_logo_path()
ICON_PATH = get_icon_path()


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog başlığı
        self.setWindowTitle("Hakkında")
        self.setFixedSize(360, 360)

        # Layout
        layout = QVBoxLayout()

        # Uygulama hakkında bilgi
        about_label = QLabel("""<h2>ShortAs</h2>
            <p>Bu uygulama, Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracıdır.</p>
            <p>Kullanıcının terminal alias'larını kolay ve güvenli şekilde yönetmesine yardımcı olur..</p>
            <p><b>Geliştirici:</b> ALG Yazılım Inc.©</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Yazılım</b> Pardus'a Göç'ü Destekler.</p>
            </br>
            <p><b>Sürüm:</b> 1.0</p>
        """)
        about_label.setWordWrap(True)  # WordWrap özelliği eklendi
        layout.addWidget(about_label) 

        # Kapatma butonu
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Temayı uygula
        self.apply_theme()

    def apply_theme(self):
        """Dialog'un temasını uygular."""
        if self.is_dark_mode():
            self.setStyleSheet("QDialog { background-color: #2e2e2e; color: white; }")
        else:
            self.setStyleSheet("QDialog { background-color: white; color: black; }")

    def is_dark_mode(self):
        """Linux'ta sistem temasının karanlık modda olup olmadığını kontrol eder (GNOME, KDE, XFCE)."""
        desktop_env = os.getenv("XDG_CURRENT_DESKTOP", "").lower()

        if desktop_env in ["gnome", "kde"]:
            return os.getenv("GTK_THEME", "").lower().find("dark") != -1
        elif desktop_env == "xfce":
            current_theme = os.popen("xfconf-query -c xsettings -p /Net/ThemeName").read().strip().lower()
            return "dark" in current_theme
        return False


class AliasManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Uygulama simgesini ayarla
        if ICON_PATH:
            self.setWindowIcon(QIcon(ICON_PATH))  # QPixmap yerine QIcon kullanıldı

        # Ayarları QSettings ile sakla
        self.settings = QSettings("ALGSoftware", "ShortAs")

        # Alias dosyasını kontrol et ve oluştur
        self.alias_file = os.path.expanduser("~/.bash_aliases")
        if not os.path.exists(self.alias_file):
            open(self.alias_file, "w").close()

        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Logo ekle
        if LOGO_PATH:
            logo_pixmap = QPixmap(LOGO_PATH)
            logo_label = QLabel()
            logo_label.setPixmap(logo_pixmap.scaled(200, 100, Qt.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        # Başlık etiketi
        title_label = QLabel("ShortAs")
        title_label.setFont(QFont("Courier", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Başlık etiketi
        title_label = QLabel("Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı")
        title_label.setFont(QFont("Courier", 13, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tema seçici
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Sistem Teması", "Aydınlık Tema", "Karanlık Tema"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)

        # Alias giriş alanı
        entry_layout = QHBoxLayout()
        layout.addLayout(entry_layout)

        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Alias Adı")
        entry_layout.addWidget(QLabel("Alias Adı:"))
        entry_layout.addWidget(self.alias_input)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Komut")
        entry_layout.addWidget(QLabel("Komut:"))
        entry_layout.addWidget(self.command_input)

        # Kısa açıklama alanı
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Alias Açıklaması (Opsiyonel)")
        entry_layout.addWidget(QLabel("Açıklama:"))
        entry_layout.addWidget(self.description_input)

        # Alias ekleme butonu
        add_button = QPushButton("Alias Ekle")
        add_button.clicked.connect(self.add_alias)
        layout.addWidget(add_button)

        # Alias silme butonu
        delete_button = QPushButton("Alias Sil")
        delete_button.clicked.connect(self.delete_alias)
        layout.addWidget(delete_button)

        # Alias listesi
        self.alias_list = QListWidget()
        layout.addWidget(self.alias_list)

        # Alias arama alanı
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Alias Ara")
        self.search_input.textChanged.connect(self.search_alias)
        layout.addWidget(self.search_input)

        # Alias dışa aktarma butonu
        export_button = QPushButton("Alias'ları Dışa Aktar")
        export_button.clicked.connect(self.export_aliases)
        layout.addWidget(export_button)

        # Alias içe aktarma butonu
        import_button = QPushButton("Alias'ları İçe Aktar")
        import_button.clicked.connect(self.import_aliases)
        layout.addWidget(import_button)

        # Hakkında butonu
        about_button = QPushButton("Hakkında")
        about_button.clicked.connect(self.show_about_dialog)
        layout.addWidget(about_button)

        # Başlangıçta temayı ayarla
        self.init_theme()

        # Uygulama başlatıldığında mevcut alias'ları listele
        self.list_aliases()

    def init_theme(self):
        """Uygulamanın başlangıçta temasını ayarlar."""
        saved_theme = self.settings.value("theme", "Sistem Teması")
        index = self.theme_combo.findText(saved_theme)
        if index != -1:
            self.theme_combo.setCurrentIndex(index)
        else:
            self.theme_combo.setCurrentIndex(0)

        self.apply_theme(saved_theme)

    def change_theme(self):
        """Tema seçildiğinde bu temayı uygular ve kaydeder."""
        selected_theme = self.theme_combo.currentText()
        self.settings.setValue("theme", selected_theme)
        self.apply_theme(selected_theme)

    def apply_theme(self, theme):
        """Seçilen temaya göre stil uygulaması."""
        if theme == "Aydınlık Tema":
            self.setStyleSheet("")
        elif theme == "Karanlık Tema":
            self.setStyleSheet("QWidget { background-color: #2e2e2e; color: white; }")
        elif theme == "Sistem Teması":
            self.setStyleSheet("")


    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec_()

    def list_aliases(self):
        """Alias dosyasını oku ve listeyi güncelle."""
        self.alias_list.clear()
        with open(self.alias_file, "r") as file:
            aliases = file.readlines()

        for alias in aliases:
            self.alias_list.addItem(alias.strip())

    def add_alias(self):
        """Yeni alias ekler."""
        alias_name = self.alias_input.text().strip()
        command = self.command_input.text().strip()
        description = self.description_input.text().strip()

        if not alias_name or not command:
            QMessageBox.warning(self, "Eksik Alan", "Alias adı ve komut gereklidir!")
            return

        # Alias'ı dosyaya ekle
        with open(self.alias_file, "a") as file:
            file.write(f"alias {alias_name}='{command}'  # {description}\n")

        # Listeyi güncelle
        self.list_aliases()

        # Temizle
        self.alias_input.clear()
        self.command_input.clear()
        self.description_input.clear()

    def delete_alias(self):
        """Seçili alias'ı siler."""
        selected_item = self.alias_list.currentItem()
        if selected_item:
            alias = selected_item.text().split(" ")[0].replace("alias", "").strip()
            with open(self.alias_file, "r") as file:
                lines = file.readlines()

            with open(self.alias_file, "w") as file:
                for line in lines:
                    if alias not in line:
                        file.write(line)

            self.list_aliases()

    def search_alias(self):
        """Alias'lar içinde arama yapar."""
        search_text = self.search_input.text().lower()
        for row in range(self.alias_list.count()):
            item = self.alias_list.item(row)
            item.setHidden(search_text not in item.text().lower())

    def export_aliases(self):
        """Alias'ları dışa aktarır."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Alias'ları Dışa Aktar", "", "Tüm Dosyalar (*)", options=options)
        if file_path:
            with open(file_path, "w") as file:
                with open(self.alias_file, "r") as alias_file:
                    file.write(alias_file.read())

    def import_aliases(self):
        """Alias'ları içe aktarır."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Alias'ları İçe Aktar", "", "Tüm Dosyalar (*)", options=options)
        if file_path:
            with open(file_path, "r") as file:
                imported_aliases = file.readlines()

            with open(self.alias_file, "a") as file:
                file.writelines(imported_aliases)

            self.list_aliases()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AliasManager()
    window.setWindowTitle("ShortAs | Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı")
    window.show()
    sys.exit(app.exec_())
