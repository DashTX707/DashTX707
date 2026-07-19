"""Color-key the terminal GIF's solid background out to transparency.

The generated GIF fills every frame with a solid background color. Rather
than trying to match GitHub's exact theme background (which varies by
light/dark mode), this strips that fill so the page's real background
shows through and the text appears to float directly on it.
"""

import sys

from PIL import Image, ImageSequence

BG_COLOR = (13, 17, 23)  # #0D1117
TOLERANCE = 30


def main() -> None:
    path = sys.argv[1]
    im = Image.open(path)

    rgba_frames = []
    durations = []
    for frame in ImageSequence.Iterator(im):
        rgba = frame.convert("RGBA")
        pixels = rgba.getdata()
        new_pixels = [
            (r, g, b, 0)
            if abs(r - BG_COLOR[0]) <= TOLERANCE
            and abs(g - BG_COLOR[1]) <= TOLERANCE
            and abs(b - BG_COLOR[2]) <= TOLERANCE
            else (r, g, b, 255)
            for r, g, b, a in pixels
        ]
        rgba.putdata(new_pixels)
        rgba_frames.append(rgba)
        durations.append(frame.info.get("duration", 100))

    palette_frames = []
    for rgba in rgba_frames:
        alpha = rgba.split()[-1]
        transparent_mask = Image.eval(alpha, lambda a: 255 if a == 0 else 0)
        p_frame = rgba.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
        p_frame.paste(255, transparent_mask)
        palette_frames.append(p_frame)

    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        transparency=255,
    )
    print(f"INFO: made background transparent in {path} ({len(palette_frames)} frames)")


if __name__ == "__main__":
    main()
