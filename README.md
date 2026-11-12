# 🗺️ niri-minimap

An ultra-minimalist **scrollable column strip minimap** for the **[niri](https://github.com/YaLTeR/niri)** Wayland compositor.

When working with 4, 6, or 10 columns along Niri's infinite horizontal strip, `niri-minimap` lets you see at a glance where you are positioned, which adjacent columns are currently visible in your viewport, and where your custom-named windows live along the strip.

```text
┌──────────────────────────────────┐
│        niri-window-label         │
│       ◇  ▫  ▣  ▪  ▫   3/5        │
└──────────────────────────────────┘
```

### Symbol Legend (Option A)

| Symbol | Meaning |
| :--- | :--- |
| `▣` *(Blue)* | Currently focused column |
| `◈` *(Gold)* | Currently focused column with a custom name from `niri-window-label` |
| `▪` *(Light)* | Unfocused column currently visible inside the monitor viewport |
| `▫` *(Dim)* | Off-screen column (to the left or right of the current viewport) |
| `◇` *(Gold)* | Off-screen column containing a custom-named window (`Super + N`) |

---

## 🔗 Two Modes of Operation

### 1. Connected to [`niri-window-label`](https://github.com/alfredoramirez985/niri-window-label) *(Automatic)*
If `niri-minimap` is installed in `~/.local/bin/niri-minimap`, `niri-window-label` automatically detects it and embeds the minimap strip directly inside its floating window pill whenever a workspace has **2 or more columns** (hiding it when there is only 1 window to keep zero visual noise).

### 2. Standalone Mode
You can also use `niri-minimap` completely on its own without `niri-window-label`:
- **Overlay Daemon:** `niri-minimap daemon`
- **Waybar / CLI output:** `niri-minimap status` (prints `◇  ▫  ▣  ▪  ▫   3/5`)

---

## 🚀 Installation

```bash
git clone https://github.com/alfredoramirez985/niri-minimap.git
cd niri-minimap
mkdir -p ~/.local/bin
cp niri-minimap ~/.local/bin/niri-minimap
chmod +x ~/.local/bin/niri-minimap
```

---

## 🧪 Running Tests

```bash
python3 -m unittest discover -s tests -v
```
