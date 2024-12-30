import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QComboBox, QFileDialog, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSettings


TRANSLATIONS = {
    "tr": {
        "window_title": "ShortAs | Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı",
        "about": "Hakkında",
        "alias_name": "Alias Adı",
        "command": "Komut",
        "description": "Açıklama",
        "add_alias": "Alias Ekle",
        "delete_alias": "Alias Sil",
        "search_placeholder": "Alias Ara",
        "export_aliases": "Alias'ları Dışa Aktar",
        "import_aliases": "Alias'ları İçe Aktar",
        "missing_field": "Eksik Alan",
        "missing_field_msg": "Alias adı ve komut gereklidir!",
        "error": "Hata",
        "select_alias_msg": "Lütfen silinecek bir alias seçin!",
        "confirm": "Onay",
        "confirm_delete": "Bu alias'ı silmek istediğinizden emin misiniz?",
        "success": "Başarılı",
        "import_success": "Alias'lar başarıyla içe aktarıldı!",
        "invalid_format": "Dosyada geçersiz alias tanımlamaları bulundu!",
        "file_error": "Dosya okuma hatası: {}",
        "language_label": "Dil:",
        "alias_name_label": "Alias Adı:",
        "command_label": "Komut:",
        "description_label": "Açıklama:",
        "description_placeholder": "Alias Açıklaması (Opsiyonel)",
        "app_subtitle": "Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı",
        "file_dialog_export": "Alias'ları Dışa Aktar",
        "file_dialog_import": "Alias'ları İçe Aktar",
        "all_files": "Tüm Dosyalar (*)",
        "alias_files": "Alias Dosyaları (*.aliases)",
        "imported_aliases_header": "\n# İçe aktarılan alias'lar\n",
        "about_text": """<h2 style='color: inherit;'>ShortAs</h2>
            <p>Bu uygulama, Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracıdır.</p>
            <p>Kullanıcının terminal alias'larını kolay ve güvenli şekilde yönetmesine yardımcı olur.</p>
            <p><b>Geliştirici:</b> ALG Yazılım Inc.©</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Yazılım</b> Pardus'a Göç'ü Destekler.</p>
            </br>
            <p><b>Sürüm:</b> 1.0</p>"""
    },
    "en": {
        "window_title": "ShortAs | Advanced Graphical User Interface Alias Management Tool",
        "about": "About",
        "alias_name": "Alias Name",
        "command": "Command",
        "description": "Description",
        "add_alias": "Add Alias",
        "delete_alias": "Delete Alias",
        "search_placeholder": "Search Alias",
        "export_aliases": "Export Aliases",
        "import_aliases": "Import Aliases",
        "missing_field": "Missing Field",
        "missing_field_msg": "Alias name and command are required!",
        "error": "Error",
        "select_alias_msg": "Please select an alias to delete!",
        "confirm": "Confirm",
        "confirm_delete": "Are you sure you want to delete this alias?",
        "success": "Success",
        "import_success": "Aliases imported successfully!",
        "invalid_format": "Invalid alias definitions found in file!",
        "file_error": "File reading error: {}",
        "language_label": "Language:",
        "alias_name_label": "Alias Name:",
        "command_label": "Command:",
        "description_label": "Description:",
        "description_placeholder": "Alias Description (Optional)",
        "app_subtitle": "Advanced Graphical User Interface Alias Management Tool",
        "file_dialog_export": "Export Aliases",
        "file_dialog_import": "Import Aliases",
        "all_files": "All Files (*)",
        "alias_files": "Alias Files (*.aliases)",
        "imported_aliases_header": "\n# Imported aliases\n",
        "about_text": """<h2 style='color: inherit;'>ShortAs</h2>
            <p>This application is an Advanced Graphical User Interface Alias Management Tool.</p>
            <p>It helps users manage their terminal aliases easily and securely.</p>
            <p><b>Developer:</b> ALG Software Inc.©</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Software</b> Supports Migration to Pardus.</p>
            </br>
            <p><b>Version:</b> 1.0</p>"""
    }
}


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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Dialog başlığı
        self.setWindowTitle(TRANSLATIONS[parent.current_language]["about"])
        self.setFixedSize(360, 360)
        
        # Layout
        layout = QVBoxLayout()
        
        # Uygulama hakkında bilgi
        about_label = QLabel(TRANSLATIONS[parent.current_language]["about_text"])
        about_label.setWordWrap(True)
        layout.addWidget(about_label)
        
        # Kapatma butonu
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # Karanlık tema uygula
        self.setStyleSheet("""
            QDialog { 
                background-color: #2e2e2e; 
                color: #ffffff; 
            }
            QLabel { 
                color: #ffffff; 
            }
            QPushButton { 
                background-color: #404040;
                border: 1px solid #505050;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)


class AliasManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Ayarları QSettings ile sakla
        self.settings = QSettings("ALGSoftware", "ShortAs")
        
        # Dil ayarını yükle
        self.current_language = self.settings.value("language", "tr")
        
        # UI elemanlarını oluştur
        self.init_ui()
        
        # Metinleri güncelle
        self.update_texts()

    def init_ui(self):
        """UI elemanlarını oluşturur."""
        # Uygulama simgesini ayarla
        if ICON_PATH:
            self.setWindowIcon(QIcon(ICON_PATH))

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
        self.subtitle_label = QLabel("Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı")
        self.subtitle_label.setFont(QFont("Courier", 13, QFont.Bold))
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle_label)

        # Karanlık tema uygula
        self.apply_dark_theme()

        # Alias giriş alanı
        entry_layout = QHBoxLayout()
        layout.addLayout(entry_layout)

        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Alias Adı")

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Komut")

        # Kısa açıklama alanı
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Alias Açıklaması (Opsiyonel)")

        # Etiketleri değişkenlerde sakla
        self.alias_name_label = QLabel()
        self.command_label = QLabel()
        self.description_label = QLabel()
        self.language_label = QLabel()
        
        entry_layout.addWidget(self.alias_name_label)
        entry_layout.addWidget(self.alias_input)
        entry_layout.addWidget(self.command_label)
        entry_layout.addWidget(self.command_input)
        entry_layout.addWidget(self.description_label)
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

        # Dil seçici
        language_layout = QHBoxLayout()
        language_layout.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Türkçe", "English"])
        self.language_combo.setCurrentText("Türkçe" if self.current_language == "tr" else "English")
        self.language_combo.currentTextChanged.connect(self.change_language)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)

        # Uygulama başlatıldığında mevcut alias'ları listele
        self.list_aliases()

    def apply_dark_theme(self):
        """Karanlık temayı uygular."""
        self.setStyleSheet("""
            QWidget { 
                background-color: #2e2e2e; 
                color: #ffffff; 
            }
            QPushButton { 
                background-color: #404040;
                border: 1px solid #505050;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #505050;
                border-radius: 3px;
                background-color: #404040;
                color: #ffffff;
            }
            QListWidget {
                background-color: #404040;
                border: 1px solid #505050;
                color: #ffffff;
            }
            QComboBox {
                background-color: #404040;
                border: 1px solid #505050;
                padding: 5px;
                border-radius: 3px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QLabel {
                color: #ffffff;
            }
        """)

    def show_about_dialog(self):
        """Hakkında dialogunu gösterir."""
        dialog = AboutDialog(self)  # self'i parent olarak geçiyoruz
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
        texts = TRANSLATIONS[self.current_language]
        alias_name = self.alias_input.text().strip()
        command = self.command_input.text().strip()
        description = self.description_input.text().strip()

        if not alias_name or not command:
            QMessageBox.warning(self, texts["missing_field"], 
                              texts["missing_field_msg"])
            return

        # Alias'ı dosyaya ekle
        with open(self.alias_file, "a") as file:
            file.write(f'alias {alias_name}="{command}"  # {description}\n')

        # Listeyi güncelle
        self.list_aliases()

        # Temizle
        self.alias_input.clear()
        self.command_input.clear()
        self.description_input.clear()

    def delete_alias(self):
        """Seçili alias'ı siler."""
        texts = TRANSLATIONS[self.current_language]
        selected_item = self.alias_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, texts["error"], 
                              texts["select_alias_msg"])
            return

        reply = QMessageBox.question(self, texts["confirm"], 
                                   texts["confirm_delete"],
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            alias_line = selected_item.text()
            with open(self.alias_file, "r") as file:
                lines = file.readlines()

            with open(self.alias_file, "w") as file:
                for line in lines:
                    if line.strip() != alias_line.strip():
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
        texts = TRANSLATIONS[self.current_language]
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            texts["file_dialog_export"],
            "", 
            f"{texts['alias_files']};;{texts['all_files']}", 
            options=options
        )
        if file_path:
            with open(file_path, "w") as file:
                with open(self.alias_file, "r") as alias_file:
                    file.write(alias_file.read())

    def import_aliases(self):
        """Alias'ları içe aktarır."""
        texts = TRANSLATIONS[self.current_language]
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            texts["file_dialog_import"],
            "", 
            f"{texts['alias_files']};;{texts['all_files']}", 
            options=options
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    imported_aliases = file.readlines()

                # Geçerli alias formatını kontrol et
                invalid_lines = []
                for line in imported_aliases:
                    if line.strip() and not line.strip().startswith('#'):
                        if not line.strip().startswith('alias '):
                            invalid_lines.append(line)

                if invalid_lines:
                    QMessageBox.warning(self, texts["error"], 
                                      texts["invalid_format"])
                    return

                with open(self.alias_file, "a") as file:
                    file.write(texts["imported_aliases_header"])
                    file.writelines(imported_aliases)

                self.list_aliases()
                QMessageBox.information(self, texts["success"], 
                                      texts["import_success"])
            except Exception as e:
                QMessageBox.critical(self, texts["error"], 
                                   texts["file_error"].format(str(e)))

    def change_language(self, language_text):
        """Dil değişikliğini uygular ve kaydeder."""
        self.current_language = "tr" if language_text == "Türkçe" else "en"
        self.settings.setValue("language", self.current_language)
        self.update_texts()
        
    def update_texts(self):
        """Tüm metinleri seçili dile göre günceller."""
        texts = TRANSLATIONS[self.current_language]
        
        # Pencere başlığı
        self.setWindowTitle(texts["window_title"])
        
        # Alt başlık
        self.subtitle_label.setText(texts["app_subtitle"])
        
        # Etiketler
        self.alias_name_label.setText(texts["alias_name_label"])
        self.command_label.setText(texts["command_label"])
        self.description_label.setText(texts["description_label"])
        self.language_label.setText(texts["language_label"])
        
        # Placeholder metinler
        self.alias_input.setPlaceholderText(texts["alias_name"])
        self.command_input.setPlaceholderText(texts["command"])
        self.description_input.setPlaceholderText(texts["description_placeholder"])
        self.search_input.setPlaceholderText(texts["search_placeholder"])
        
        # Buton metinleri
        for button in self.findChildren(QPushButton):
            if button.text() in ["Alias Ekle", "Add Alias"]:
                button.setText(texts["add_alias"])
            elif button.text() in ["Alias Sil", "Delete Alias"]:
                button.setText(texts["delete_alias"])
            elif button.text() in ["Alias'ları Dışa Aktar", "Export Aliases"]:
                button.setText(texts["export_aliases"])
            elif button.text() in ["Alias'ları İçe Aktar", "Import Aliases"]:
                button.setText(texts["import_aliases"])
            elif button.text() in ["Hakkında", "About"]:
                button.setText(texts["about"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    window = AliasManager()
    window.setWindowTitle("ShortAs | Gelişmiş Grafiksel Kullanıcı Arayüzlü Alias Yönetim Aracı")
    window.show()
    sys.exit(app.exec_())
