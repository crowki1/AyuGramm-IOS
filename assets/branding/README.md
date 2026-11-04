# Umogram iOS artwork

`Brand.png` (1254 × 1254, opaque) is the launcher artwork: the owner's crystal mark — four
glass wedges on a near-black tile — cropped out of the 1024 px source render and upscaled.

`AyuGram-logo.png`, `AyuGram-blue.png` and `AyuGram-graphite.png` are kept under their old
file names so the patches keep referencing them; all three now hold the same mark.

`previews/Brand.png`, `previews/Blue.png` and `previews/Graphite.png` are the 300 px versions
shown in the in-app icon picker.

The badge (`ExteraBadge.imageset`, `ExteraDeveloperBadge.imageset`) is a template-rendered
white silhouette of the same mark on a transparent canvas, so iOS tints it with the chat's
accent colour like every other credibility badge. Sizes are 16/32/48 px.

The native app receives these files through `ci/prepare.py`, which copies them over the
icon bundles the patches ship. Icon Composer applies the platform mask, so the artwork is
full-bleed with no pre-applied rounded corners.
