# CertumSigner

CertumSigner ist ein Windows-Tool zum automatisierten Signieren von Dateien und Ordnern über **Certum SimplySign** + Microsoft **SignTool.exe**.

Die Anwendung ermöglicht:
- Batch-Signierung ganzer Ordner
- Integrierte GUI (Windows)
- Automatische Zeitstempelserver-Integration
- Logging & Fehleranalyse

## 🚀 Features
- Nutzung von SimplySign über die Mobil-App + Cloud-Zertifikat
- Vollautomatische Signiervorgänge
- Unterstützt Dateien und ganze Verzeichnisbäume
- Einfache Bedienung per GUI

---

## 📦 Installation

### Voraussetzungen
- Windows 10/11
- Certum SimplySign App + aktives Zertifikat
- SignTool.exe (in Windows SDK enthalten)
- Python 3.10+ (falls Quellcode verwendet wird)

---

## ▶️ Verwendung

### EXE-Version

1. CertumSigner.exe aus dem Ordner `dist/` starten.
2. Datei oder Ordner auswählen.
3. Signieren klicken.

### Python-Version

```bash
pip install -r requirements.txt
python src/certum_signer.py
```

---

## 📚 Dokumentation

Weitere Details:

- `docs/usage.md`
- `docs/troubleshooting.md`
- `docs/faq.md`

---

## 🔨 Entwicklung / Beitrag

Siehe `CONTRIBUTING.md`

---

## 📜 Lizenz

Dieses Projekt steht unter GPL-3.0.
