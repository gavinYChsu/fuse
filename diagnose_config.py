from fuse import state_manager, config, program
import argparse

# Mocking the command line to use the run command
print("Config path:", state_manager.get_item('config_path'))
ui_layouts = config.get_str_list('uis', 'ui_layouts', 'default')
print(f"ui_layouts from config: {ui_layouts}")

p = program.create_program()
args = p.parse_args(['run'])
print(f"ui_layouts from parsed args: {args.ui_layouts}")
