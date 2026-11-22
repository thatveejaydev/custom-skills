#!/usr/bin/env python3
"""Merge a sharp background plate and its zoomed-out version into one expanded background.

  expand_background.py PLATE EXPANDED OUTPUT

The output is up to 1.5x the frame in both directions, with the frame exactly centered: 1620x2880 for a
9:16 frame, 2880x1620 for 16:9. The middle keeps the plate's detail. OUTPUT is the only file written.
Needs only numpy and Pillow, which Codex's bundled Python includes.
"""
import pathlib
import sys

sys.dont_write_bytecode = True
try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("expand_background.py needs Pillow and numpy:  pip install pillow numpy")

GROW, MIN_GROW = 1.5, 1.25


def blur(a, sigma):
    """Fast Gaussian-like blur of any radius: three box passes on each axis."""
    r = max(1, round(sigma))
    out = a.astype(np.float32)
    for axis in (0, 1):
        v = np.moveaxis(out, axis, 0)
        for _ in range(3):
            padded = np.concatenate([np.repeat(v[:1], r + 1, 0), v, np.repeat(v[-1:], r, 0)])
            total = np.cumsum(padded, 0, dtype=np.float64)
            v = ((total[2 * r + 1:] - total[:-2 * r - 1]) / (2 * r + 1)).astype(np.float32)
        out = np.moveaxis(v, 0, axis)
    return out


def resize(a, size):
    return np.asarray(Image.fromarray(a).resize(size, Image.BILINEAR))


def gray(rgb):
    return rgb.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)


def edges(rgb):
    dy, dx = np.gradient(gray(rgb))
    return blur(np.log1p(4 * np.hypot(dx, dy)), 1)


def warp(rgb, m, size):
    """Sample rgb at m applied to every pixel of an image of the given size, repeating the border outward."""
    pad = max(rgb.shape[:2]) // 4
    padded = np.pad(rgb, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    a, b, c, d, e, f = np.asarray(m, float).ravel()
    return np.asarray(Image.fromarray(padded).transform(
        size, Image.AFFINE, (a, b, c + pad, d, e, f + pad), Image.BICUBIC))


def sample(a, x, y):
    """Bilinear lookup of a at float coordinates."""
    h, w = a.shape[:2]
    x, y = np.clip(x, 0, w - 1.001), np.clip(y, 0, h - 1.001)
    ix, iy = x.astype(np.int32), y.astype(np.int32)
    fx, fy = x - ix, y - iy
    if a.ndim == 3:
        fx, fy = fx[..., None], fy[..., None]
    top = a[iy, ix] * (1 - fx) + a[iy, ix + 1] * fx
    low = a[iy + 1, ix] * (1 - fx) + a[iy + 1, ix + 1] * fx
    return (top * (1 - fy) + low * fy).astype(np.float32)


def locate(plate, wide):
    """Return the transform from plate pixels to expanded-image pixels."""
    k = 360 / max(wide.shape[:2])
    target = edges(resize(wide, (round(wide.shape[1] * k), round(wide.shape[0] * k))))
    H, W = target.shape
    target -= target.mean()
    spectrum = np.fft.rfft2(target)
    total, squares = [np.pad(v.astype(np.float64).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
                      for v in (target, target ** 2)]

    def match(w, h):
        t = edges(resize(plate, (w, h)))
        t -= t.mean()
        found = np.fft.irfft2(spectrum * np.conj(np.fft.rfft2(t, (H, W))), (H, W))[:H - h + 1, :W - w + 1]

        def window(s):
            return s[h:, w:] - s[:-h, w:] - s[h:, :-w] + s[:-h, :-w]

        spread = np.maximum(window(squares) - window(total) ** 2 / (w * h), 1e-3)
        scores = found / np.sqrt(spread * float((t ** 2).sum()) + 1e-6)
        y, x = np.unravel_index(scores.argmax(), scores.shape)
        return float(scores[y, x]), w, h, int(x), int(y)

    best = (-1.0, 0, 0, 0, 0)
    for w in range(round(0.40 * W), W + 1, 2):
        h = round(w * plate.shape[0] / plate.shape[1])
        if h > H:
            break
        best = max(best, match(w, h))
    # Models sometimes squash the picture to fit another shape, so then let width and height vary separately.
    if best[1]:
        for _ in range(2):
            _, w0, h0, _, _ = best
            for h in range(round(0.8 * h0), min(H, round(1.25 * h0)) + 1, 3):
                best = max(best, match(w0, h))
            _, w0, h0, _, _ = best
            for w in range(round(0.8 * w0), min(W, round(1.25 * w0)) + 1, 3):
                best = max(best, match(w, h0))
        _, w0, h0, _, _ = best
        for w in range(max(8, w0 - 3), min(W, w0 + 3) + 1):
            for h in range(max(8, h0 - 3), min(H, h0 + 3) + 1):
                best = max(best, match(w, h))
    score, w, h, x, y = best
    if score < 0.35:
        sys.exit("FAIL the expanded image does not contain the plate; regenerate the expanded image")
    sx, sy = wide.shape[1] / W, wide.shape[0] / H
    return np.array([[w * sx / plate.shape[1], 0, x * sx], [0, h * sy / plate.shape[0], y * sy]])


def flow(plate, other):
    """Offsets (dx, dy) so that other sampled at p + offset lines up with plate at p."""
    h, w = plate.shape[:2]
    fx = fy = np.zeros((2, 2), np.float32)
    for level in (8, 4, 2):
        size = (w // level, h // level)
        a, b = [gray(resize(i, size)) for i in (plate, other)]
        a, b = [v - blur(v, 6) for v in (a, b)]  # ignore differences in color and light
        fx, fy = resize(fx, size) * (size[0] / fx.shape[1]), resize(fy, size) * (size[1] / fy.shape[0])
        x, y = np.meshgrid(np.arange(size[0], dtype=np.float32), np.arange(size[1], dtype=np.float32))
        for _ in range(5):
            moved = sample(b, x + fx, y + fy)
            gy, gx = np.gradient((a + moved) / 2)
            err = moved - a
            xx, yy, xy, xe, ye = [blur(v, 4) for v in (gx * gx, gy * gy, gx * gy, gx * err, gy * err)]
            xx, yy = xx + 2, yy + 2
            det = xx * yy - xy * xy
            fx = fx - np.clip((yy * xe - xy * ye) / det, -1.5, 1.5)
            fy = fy - np.clip((xx * ye - xy * xe) / det, -1.5, 1.5)
            fx, fy = blur(fx, 2), blur(fy, 2)
    return np.dstack([resize(fx, (w, h)) * (w / size[0]), resize(fy, (w, h)) * (h / size[1])])


def refine(m, plate, wide):
    """Tighten the match using the flow left over after the coarse one."""
    h, w = plate.shape[:2]
    for _ in range(2):
        offset = flow(plate, warp(wide, m, (w, h)))[8::16, 8::16]
        ys, xs = np.mgrid[8:h:16, 8:w:16]
        here = np.c_[xs.ravel(), ys.ravel(), np.ones(xs.size)]
        there = np.c_[here[:, :2] + offset.reshape(-1, 2), np.ones(xs.size)] @ m.T
        keep = np.ones(xs.size, bool)
        for _ in range(4):
            fit = np.linalg.lstsq(here[keep], there[keep], rcond=None)[0]
            miss = np.linalg.norm(here @ fit - there, axis=1)
            keep = miss <= np.percentile(miss, 80)
        m = fit.T
    return m


def agreement(m, plate, wide):
    """How well the linework inside the frame agrees: about 1 for the same scene, under 0.3 for another."""
    h, w = plate.shape[:2]
    size = (w // 4, h // 4)
    a, b = [edges(resize(i, size)) for i in (plate, warp(wide, m, (w, h)))]
    return float(np.corrcoef(a.ravel(), b.ravel())[0, 1])


def room(m, plate, wide):
    """Largest centered enlargement of the plate that the expanded image can fill."""
    h, w = plate.shape[:2]
    slack = 0.008 * max(wide.shape[:2])
    limit = np.array([wide.shape[1], wide.shape[0]]) + slack
    for grow in np.arange(GROW, 0.999, -0.005):
        x, y = w * (grow - 1) / 2, h * (grow - 1) / 2
        corners = np.array([[-x, -y, 1], [w + x, -y, 1], [-x, h + y, 1], [w + x, h + y, 1]]) @ m.T
        if (corners >= -slack).all() and (corners <= limit).all():
            return float(grow)
    return 1.0


def merge(plate, wide, m, grow):
    h, w = plate.shape[:2]
    px, py = round(w * (grow - 1) / 2), round(h * (grow - 1) / 2)
    size = (w + 2 * px, h + 2 * py)
    shifted = m.copy()
    shifted[:, 2] -= m[:, :2] @ np.array([px, py], float)
    base = warp(wide, shifted, size)

    x, y = np.meshgrid(np.arange(size[0], dtype=np.float32), np.arange(size[1], dtype=np.float32))
    away = np.hypot(np.maximum(np.maximum(px - x, x - (px + w - 1)), 0),
                    np.maximum(np.maximum(py - y, y - (py + h - 1)), 0))
    fade = np.exp(-away / (0.15 * w))[..., None]

    def spread(field):
        """Carry a correction measured inside the frame outward, fading with distance."""
        full = blur(np.pad(field, ((py, py), (px, px), (0, 0)), mode="edge"), 0.015 * w)
        full[py:py + h, px:px + w] = field
        return full * fade

    # The two generations never agree exactly, so bend the surround until its lines meet the plate's.
    bend = spread(np.clip(flow(plate, base[py:py + h, px:px + w]), -0.03 * w, 0.03 * w))
    base = sample(base, x + bend[..., 0], y + bend[..., 1])

    # Then match its color and light to the plate's.
    diff = blur(plate.astype(np.float32) - base[py:py + h, px:px + w], 0.025 * w)
    base += spread(np.clip(diff, -35, 35))

    band = max(4, 0.025 * w)
    inside = np.minimum.reduce([x - px, px + w - 1 - x, y - py, py + h - 1 - y])
    a = np.clip(inside / band, 0, 1)[py:py + h, px:px + w, None]
    base[py:py + h, px:px + w] = plate * a + base[py:py + h, px:px + w] * (1 - a)
    return np.clip(base, 0, 255).astype(np.uint8)


def refuse_skill_folder(path):
    path = path.resolve()
    if any((folder / "SKILL.md").is_file() for folder in (path, *path.parents)):
        sys.exit(f"FAIL {path} is inside a skill folder; save in the project, or ask the user where to save")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    plate, wide = (np.asarray(Image.open(p).convert("RGB")) for p in sys.argv[1:3])
    out = pathlib.Path(sys.argv[3])
    refuse_skill_folder(out)
    m = refine(locate(plate, wide), plate, wide)
    if not agreement(m, plate, wide) >= 0.55:
        sys.exit("FAIL the expanded image changed or lost the plate; regenerate the expanded image")
    grow = room(m, plate, wide)
    if grow < MIN_GROW:
        sys.exit(f"FAIL only {grow:.2f}x of centered space; regenerate the expanded image, zoomed out further "
                 "with the original in the middle")

    result = merge(plate, wide, m, grow)
    h, w = plate.shape[:2]
    frame = (w, h)
    for standard in ((1080, 1920), (1920, 1080)):
        if abs((w / h) / (standard[0] / standard[1]) - 1) < 0.03:
            frame = standard
    scale = max(frame[0] / w, frame[1] / h)
    size = (round(result.shape[1] * scale), round(result.shape[0] * scale))
    if grow >= GROW - 0.02 and frame != (w, h):
        size = (round(frame[0] * grow), round(frame[1] * grow))
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result).resize(size, Image.LANCZOS).save(out)
    print(f"ok   {out.name}: {size[0]}x{size[1]}, frame {frame[0]}x{frame[1]} centered, {grow:.2f}x space")
    if grow < GROW - 0.02:
        print("WARN less than the 1.5x requested; regenerate the expanded image if more room is needed")


if __name__ == "__main__":
    main()
