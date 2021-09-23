import wx
import os
import pcbnew as pcb

	
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
		zones = [board.GetArea(i) for i in range(board.GetAreaCount())]
		if len(net)==0:
			net = [zone.GetNetname() for zone in zones if zone.IsSelected()]
		if len(net) :
			netcode = board.GetNetcodeFromNetname(net[0])
			tracks_on_net = board.TracksInNet(netcode)
			for track in tracks_on_net:
				board.Remove(track)
			for zone in zones:
				if net[0] == zone.GetNetname():
					board.Remove(zone)
			filler = pcb.ZONE_FILLER(board)
			filler.Fill(board.Zones())
			#pcb.Refresh() 
		else:
			wx.MessageBox("没有选中的连线或焊盘")
