# DFF Convert (dffconvert)

Convert dff file to another format.

## Usage
```sh
# available modes: autodesk_3ds, fbx, obj, x3d
blender -b -P plugin.py -P script.py -- [path_to_dff] [path_to_output] [mode]
```

Environment variables:
- `TEXTURES_DIR` - This is a directory with images from a TXD file in PNG format. Used to correctly describe textures in the MTL file. Default: [path_to_dff]_tex

## Dependencies

- [Blender (<2.80)](https://www.blender.org/)
- [Blender DFF IO For III/VC/SA](https://www.gtagarage.com/mods/show.php?id=21598)
