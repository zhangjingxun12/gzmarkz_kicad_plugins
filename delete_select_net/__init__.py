try:
	from .delete_select_net import Deleteselectnet
	Deleteselectnet().register()
except Exception as e:
    import os
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'delete_select_net.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))