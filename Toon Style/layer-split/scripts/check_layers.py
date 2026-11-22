#!/usr/bin/env python3
"""Make sure every layer in a raw folder is transparent.

  check_layers.py RAW

background.png and layers that are already transparent are left untouched. A layer on a flat green,
magenta or cyan background is made transparent in place. No other files are created.
"""
import pathlib
import sys

sys.dont_write_bytecode = True
try:
    import numpy as np
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("check_layers.py needs Pillow and numpy:  pip install pillow numpy")

KEYS = {"green": (0, 255, 0), "magenta": (255, 0, 255), "cyan": (0, 255, 255)}


def channels(key):
    """(channels that are high in the key, channels that are low)."""
    high = [i for i, v in enumerate(KEYS[key]) if v]
    return high, [i for i in range(3) if i not in high]


def dominance(rgb, key):
    high, low = channels(key)
    return rgb[..., high].min(-1) - rgb[..., low].max(-1)


def cut_out(im):
    """Return (RGBA, method, warnings) at the original size. Raises ValueError when there is nothing safe to cut."""
    im = im.convert("RGBA")
    data = np.asarray(im).astype(np.float32)
    rgb, alpha = data[..., :3].copy(), data[..., 3].copy()
    warn = []

    if (alpha < 10).mean() > 0.005:
        method = "native alpha"
        visible = alpha > 20
        if visible.any() and (alpha[visible] < 235).mean() > 0.25:
            warn.append("much of the subject is see-through; regenerate it as fully opaque")
    else:
        edge = np.concatenate([rgb[:4].reshape(-1, 3), rgb[-4:].reshape(-1, 3),
                               rgb[:, :4].reshape(-1, 3), rgb[:, -4:].reshape(-1, 3)])
        bg = np.median(edge, axis=0)
        key = max(KEYS, key=lambda k: dominance(bg, k))
        strength = float(dominance(bg, key))
        if strength < 90 or (np.linalg.norm(edge - bg, axis=-1) < 70).mean() < 0.55:
            raise ValueError("no transparency and no flat key background (a drawn checkerboard does not count)")
        method = f"{key} key"

        # Only the background and a narrow band next to it are altered, so similar colors inside the art survive.
        dom = dominance(rgb, key)
        back = (np.linalg.norm(rgb - bg, axis=-1) < 70) & (dom > 0.6 * strength)
        near = np.asarray(Image.fromarray(back.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(7))) > 0
        band = near & ~back
        alpha[back] = 0
        a = np.clip(1 - np.maximum(dom[band] - 0.08 * strength, 0) / (0.92 * strength), 0, 1)
        alpha[band] = a * 255

        c = rgb[band]
        c = np.clip((c - (1 - a[:, None]) * bg) / np.maximum(a[:, None], 0.2), 0, 255)
        spill = np.maximum(dominance(c, key), 0)
        for i in channels(key)[0]:
            c[:, i] -= spill
        rgb[band] = c

    alpha[alpha < 12] = 0
    solid = Image.fromarray(((alpha > 20) * 255).astype(np.uint8))
    # A median pass stops stray specks from counting as the subject touching the edge.
    box = solid.filter(ImageFilter.MedianFilter(5)).getbbox() or solid.getbbox()
    if not box:
        raise ValueError("nothing was left after removing the background")
    left, top, right, bottom = box
    if left <= 1 or top <= 1 or right >= im.width - 1 or bottom >= im.height - 1:
        warn.append("subject touches the image edge and may be cropped; regenerate with margin all around")
    out = Image.fromarray(np.dstack([rgb, alpha]).clip(0, 255).astype(np.uint8))
    return out, method, warn


def refuse_skill_folder(path):
    path = path.resolve()
    if any((folder / "SKILL.md").is_file() for folder in (path, *path.parents)):
        sys.exit(f"FAIL {path} is inside a skill folder; save in the project, or ask the user where to save")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = pathlib.Path(sys.argv[1])
    refuse_skill_folder(raw)
    if not raw.is_dir():
        sys.exit(f"{raw} is not a folder")
    failed = False
    if not (raw / "background.png").exists():
        print("FAIL background.png is missing")
        failed = True
    for path in sorted(raw.iterdir()):
        if path.name == "background.png" or not path.is_file():
            continue
        if path.suffix.lower() != ".png":
            print(f"FAIL {path.name}: layers must be saved as PNG")
            failed = True
            continue
        try:
            with Image.open(path) as im:
                out, method, warnings = cut_out(im)
        except (OSError, ValueError) as e:
            print(f"FAIL {path.name}: {e}")
            failed = True
            continue
        if method != "native alpha":
            out.save(path)
        print(f"ok   {path.name}: {method}")
        for w in warnings:
            print(f"WARN {path.name}: {w}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
