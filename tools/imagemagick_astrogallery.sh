#!/usr/bin/env bash
read -rp "Source folder path: " SRC
OUT="$SRC/converted"
mkdir -p "$OUT"

count=1
# include videos in search so numbering stays consistent
find "$SRC" -maxdepth 1 -type f \( \
    -iname '*.jpg'  -o -iname '*.jpeg' -o -iname '*.png'  -o -iname '*.tif' -o -iname '*.tiff' -o -iname '*.webp' \
    -o -iname '*.mp4' -o -iname '*.mov' \) -print0 |
  sort -z |
  while IFS= read -r -d '' file; do
    printf -v num "%03d" "$count"
    ext="${file##*.}"
    lc_ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    case "$lc_ext" in
      jpg|jpeg|png|tif|tiff|webp)
        magick "$file" -resize 1600x1600\> -quality 82 "$OUT/$num.webp"
        ;;
      mp4|mov)
        # simply copy the video without conversion, preserving extension
        cp "$file" "$OUT/$num.$lc_ext"
        ;;
    esac
    ((count++))
  done

echo "Done. Processed webp images to $OUT/"