# 🌙 DuskBeacon

An RGB lamp that automatically turns on at night, but only if I'm actually home. It uses ping in order to detect my phone.

---

## ⚙️ How It Works

* **Time check** — Using the `astral` library, the script calculates today's dusk and dawn times for Timisoara (based on actual sun position, not a fixed clock time), so the "night window" shifts automatically with the seasons.
* **Presence check** — During the night window, it pings both the dorm router and my phone's local IP. If both respond, I'm considered "home and connected to the home network."
* **Lamp control** — If present, it turns the RGB lamp on dim (via Home Assistant's API) and periodically re-checks the lamp's state, so turning it off manually stops the script's monitoring loop early instead of fighting the manual override.
* **Auto-off** — If nobody turns it off manually, the lamp shuts off automatically after a set duration.
* Once daytime is reached, the script exits.

> [!TIP]
> If you want to use this, you need to set a static IP for your phone in your router's settings.

---

## 🧰 Tech Stack

| Component / Tool | Purpose |
| :--- | :--- |
| **Python 3** (`requests`, `astral`, `ping3`) | Script logic, time calculation, and networking |
| **Home Assistant** | Self-hosted on a Pi for lamp control |

---

## ⚠️ Known Limitations

* If my phone's Wi-Fi is activated, the lamp can turn on even if I'm just passing by the dorm. It doesn't distinguish "phone connected to WiFi" from "phone actually in the room."

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white)
