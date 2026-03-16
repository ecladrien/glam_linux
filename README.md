# GLAM v6 (Linux Ubuntu)

Application de supervision avec interface PySide6 : pages Accueil, Plans, Mesures, Caméra, QLC et Setup.

Ce README est orienté **déploiement Ubuntu** avec bonnes pratiques (venv, service `systemd`, variables d'environnement, logs, sécurité minimale).

## 1) Prérequis

- Ubuntu 22.04+ (desktop recommandé pour l'interface graphique)
- Compte utilisateur non-root avec `sudo`
- Python 3.10+ recommandé
- Accès matériel optionnel : caméra RTSP/ONVIF, ESP32 WROOM

> GLAM est une application GUI. Pour un démarrage automatique, ciblez une session graphique active (`graphical.target`).

## 2) Structure utile

- Code applicatif : `src/`
- Configuration : `data/config.json`
- Données mesures : `data/measurements.csv`
- Logs applicatifs : `logs/glam.log`
- Kit de déploiement Ubuntu : `deploy/ubuntu/`

## 3) Déploiement rapide Ubuntu

Depuis la racine du projet :

```bash
chmod +x deploy/ubuntu/install.sh deploy/ubuntu/run_glam.sh
./deploy/ubuntu/install.sh
```

Ce script :
- installe les dépendances système requises pour PySide6/OpenCV,
- crée le virtualenv `.venv`,
- installe les dépendances Python de `requirements.txt`,
- prépare `logs/` et `data/`,
- ajoute l'utilisateur au groupe `dialout` (ESP32/USB série).

Si `dialout` a été ajouté, reconnectez votre session.

## 4) Configuration runtime (secrets)

Ne stockez pas les secrets dans `data/config.json`.

```bash
cp deploy/ubuntu/glam.env.example deploy/ubuntu/glam.env
nano deploy/ubuntu/glam.env
```

Variables principales :
- `RTSP_PASSWORD` : mot de passe caméra (lu par `src/config/manager.py`)
- `QT_QPA_PLATFORM` (optionnel) : backend Qt (`xcb` par défaut)

## 5) Lancement manuel

```bash
./deploy/ubuntu/run_glam.sh
```

## 6) Démarrage automatique avec systemd

### Installer le service

```bash
cp deploy/ubuntu/glam.service /tmp/glam.service
sed -i "s|__USER__|$USER|g" /tmp/glam.service
sed -i "s|__PROJECT_DIR__|$(pwd)|g" /tmp/glam.service
sudo cp /tmp/glam.service /etc/systemd/system/glam.service
sudo systemctl daemon-reload
sudo systemctl enable glam.service
sudo systemctl start glam.service
```

### Vérifier

```bash
systemctl status glam.service
journalctl -u glam.service -f
```

### Arrêter / redémarrer

```bash
sudo systemctl restart glam.service
sudo systemctl stop glam.service
```

## 7) Bonnes pratiques d'exploitation

- Exécuter GLAM avec un utilisateur dédié (non-root)
- Garder les secrets dans `deploy/ubuntu/glam.env` (non versionné)
- Sauvegarder régulièrement `data/config.json` et `data/measurements.csv`
- Vérifier les permissions d'accès série (`dialout`) et caméra
- Surveiller `logs/glam.log` et `journalctl` pour le diagnostic

## 8) Mise à jour applicative

```bash
git pull
./deploy/ubuntu/install.sh
sudo systemctl restart glam.service
```

## 9) Tests

```bash
source .venv/bin/activate
pytest -q
```

## 10) Dépannage rapide

- Erreur Qt/X11 (`xcb`) : vérifier la session graphique et `DISPLAY=:0`
- Caméra non détectée : valider IP/réseau/ports RTSP-ONVIF
- ESP32 indisponible : vérifier port (`/dev/ttyACM0` ou `/dev/ttyUSB0`), groupe `dialout`, et le firmware série ESP32
- Pas de démarrage service : consulter `journalctl -u glam.service -n 200`
