import traceback
try:
    from fuse import core, state_manager, choices
    # Initialize state manager with some defaults if necessary
    for key, value in choices.ui_layout_set.items():
        state_manager.init_item(key, value)
    
    state_manager.init_item('log_level', 'debug')
    state_manager.init_item('processors', ['face_swapper']) # example
    
    print(f'Common pre-check: {core.common_pre_check()}')
    print(f'Processors pre-check: {core.processors_pre_check()}')
except Exception as e:
    traceback.print_exc()
