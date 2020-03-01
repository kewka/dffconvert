import bpy
import sys

def main():
    args = sys.argv

    try:
        args = args[args.index("--") + 1:]
    except ValueError:
        args = []

    if len(args) < 3:
        print('Use: blender -b -P plugin.py -P script.py -- [path_to_dff] [path_to_output] [mode]')
        exit(1)

    [dff, output, mode] = args
    available_modes = dir(bpy.ops.export_scene)

    if mode not in available_modes:
        print('Available modes:', available_modes)
        exit(1)

    # Select all objects
    for obj in bpy.context.scene.objects:
        obj.select = True

    # Delete selected objects
    bpy.ops.object.delete()

    # Import dff object
    bpy.ops.import_rw.dff(
        'EXEC_DEFAULT', filepath=dff)

    # Export scene.
    getattr(bpy.ops.export_scene, mode)(filepath=output, path_mode = 'STRIP')


if __name__ == '__main__':
    main()
