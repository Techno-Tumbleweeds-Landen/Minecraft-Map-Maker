"""
from PIL import Image, ImageDraw, ImageFont

# ——— CONFIG ———
IMG_PATH       = "area.png"               # 1024×1024 input
OUTPUT_PATH    = "grid_highres_hl.png"    # output file
CELLS          = 256                      # grid cells per side
OFFSET         = 64                       # world coords offset
LABEL_EVERY    = 8                       # label & highlight interval
BASE_FONT_SIZE = 6                       # font size at scale=1
SCALE          = 4                        # ↑ adjust for higher res

# ——— DERIVED ———
ORIG_SIZE      = 1024
SCALED_SIZE    = ORIG_SIZE * SCALE
PX_PER_CELL    = SCALED_SIZE // CELLS
FONT_SIZE      = BASE_FONT_SIZE * SCALE
LINE_WIDTH     = max(1, SCALE // 2)

def main():
    # Load & upscale base image
    img = Image.open(IMG_PATH).convert("RGBA")
    img = img.resize((SCALED_SIZE, SCALED_SIZE), resample=Image.NEAREST)

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()

    # Draw grid lines
    for i in range(CELLS + 1):
        p = i * PX_PER_CELL
        draw.line([(p, 0), (p, SCALED_SIZE)], fill="white", width=LINE_WIDTH)
        draw.line([(0, p), (SCALED_SIZE, p)], fill="white", width=LINE_WIDTH)

    # Label & highlight cells at intervals
    for col in range(0, CELLS, LABEL_EVERY):
        for row in range(0, CELLS, LABEL_EVERY):
            # Compute pixel bounds of this cell
            x0 = col * PX_PER_CELL
            y0 = row * PX_PER_CELL
            x1 = x0 + PX_PER_CELL
            y1 = y0 + PX_PER_CELL

            # Draw semi‐transparent yellow fill
            draw.rectangle(
                [(x0, y0), (x1, y1)],
                fill=(255, 255, 0, 80),      # RGBA: yellow at 31% opacity
                outline="yellow",
                width=LINE_WIDTH
            )

            # Compute world‐coords label
            world_x = col - OFFSET
            world_z = row - OFFSET

            # Draw the text inset a few pixels from top‐left of cell
            text_x = x0 + SCALE
            text_y = y0 + SCALE
            draw.text(
                (text_x, text_y),
                f"{world_x},{world_z}",
                fill="yellow",
                font=font
            )

    # Save result
    img.save(OUTPUT_PATH)
    print(f"Saved highlighted grid overlay to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
"""