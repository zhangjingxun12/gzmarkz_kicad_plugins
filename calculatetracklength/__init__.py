try:
	from .calculatetracklength import Calculatetracklength
	Calculatetracklength().register()
except Exception as e:
    import os
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'calculate_track_length.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))