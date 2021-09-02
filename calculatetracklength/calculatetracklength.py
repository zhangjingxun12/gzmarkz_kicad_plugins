import wx
import os
import pcbnew as pcb

class Calculatetracklength(pcb.ActionPlugin):
	def defaults(self):
		self.name = '计算当前选中的网络走线长度'
		self.category = 'Calculate_track_length'
		self.description = 'Calculate_track_length'
		self.show_toolbar_button = True
		self.icon_file_name = os.path.join(os.path.dirname(__file__), 'calculate_track_length.png')
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
				length = length + t.GetLength()
			result = "【%s】长度: \n\t"%net[0] + "%.3f mm\n\t"%pcb.ToMM(length) + "%.2f mils"%pcb.ToMils(length)
			wx.MessageBox(result)
		else:
			wx.MessageBox("No pad or track selected")
