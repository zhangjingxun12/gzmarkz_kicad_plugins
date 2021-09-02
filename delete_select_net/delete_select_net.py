import wx
import os
import pcbnew as pcb

'''
	此处参考泪滴插件的magicid
	参考插件 kicad_scripts-master\teardrops
'''
MAGIC_TEARDROP_ZONE_ID = 0x4242

	
	
class Deleteselectnet(pcb.ActionPlugin):
	def defaults(self):
		self.name = '删除选中的网络连线'
		self.category = '删除选中的网络连线'
		self.description = '删除选中的网络连线'
		self.show_toolbar_button = True
		self.icon_file_name = os.path.join(os.path.dirname(__file__), 'delete_select_net.png')
	def Run(self):
		board = pcb.GetBoard()
		pads = board.GetPads()
		net = [pad.GetNetname() for pad in pads if pad.IsSelected()]
		if len(net)==0:
			tracks = board.GetTracks()
			net = [t.GetNetname() for t in tracks if t.IsSelected()]
		if len(net) :
			netcode = board.GetNetcodeFromNetname(net[0])
			tracks_on_net = board.TracksInNet(netcode)
			length = 0
			for t in tracks_on_net:
				t.SetSelected()
			
			all_tracks = board.GetTracks()
			delete_tracks = [x for x in all_tracks if x.IsSelected()]

			all_zones = []
			for zoneid in range(board.GetAreaCount()):
				all_zones.append(board.GetArea(zoneid))
			delete_zones = [x for x in all_zones if x.IsSelected()]

			all_modules = board.GetFootprints()
			delete_modules = [x for x in all_modules if x.IsSelected()]
			
			
			teardrops_zones = {}
			for zone in [board.GetArea(i) for i in range(board.GetAreaCount())]:
				if zone.GetPriority() == MAGIC_TEARDROP_ZONE_ID:
					netname = zone.GetNetname()
					if netname not in teardrops_zones.keys():
						teardrops_zones[netname] = []
					teardrops_zones[netname].append(zone)
			for netname in teardrops_zones:
				if netname == net[0]:
					for teardrop in teardrops_zones[netname]:
						board.Remove(teardrop)
			
			filler = pcb.ZONE_FILLER(board)
			filler.Fill(board.Zones())
			
			for track in delete_tracks:
				board.Remove(track)
			for zone in delete_zones:
				board.Remove(zone)
			for mod in delete_modules:
				board.Remove(mod)
				
		else:
			wx.MessageBox("No pad or track selected")
