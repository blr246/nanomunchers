'''
Interactive plot for nanomunchers game.
There are no command line arguments to this script.
'''
import sys
import xml.dom.minidom as xmlminidom
import Tkinter as tk
import time

def xml_get_ele_dom(dom, ele, idx=0):
    ''' Extract the xml node object with the given name. '''
    return dom.getElementsByTagName(ele).item(idx)

def xml_get_ele_val_str(dom, ele, idx=0, child_idx=0):
    ''' Extract xml node value from the node with the given name. '''
    node_list_item = dom.getElementsByTagName(ele).item(idx)
    if node_list_item is not None:
        node = node_list_item.childNodes.item(child_idx)
        if node is not None:
            return node.nodeValue
        else:
            return None
    else:
        return None

def write_stdout(message):
    ''' Write a line to stdout. '''
    sys.stdout.write(message)
    sys.stdout.flush()

def read_stdin():
    ''' Read a line from stdin. '''
    try:
        line = raw_input()
        return line
    except EOFError:
        print "Stdin was closed."
        return None
    
class NanoVis(object):
    ''' Visualization for the nanomunchers game using Matplotlib.  '''

    class SetupParams(object):
        ''' Setup parameters for the nanomunchers game. '''

        def __init__(self, dimx, dimy):
            self._dimx = dimx
            self._dimy = dimy

        @classmethod
        def from_dom(cls, dom):
            ''' Create a SetupParams from an xml dom. '''
            dimx = int(xml_get_ele_val_str(dom, 'DimX'))
            dimy = int(xml_get_ele_val_str(dom, 'DimY'))
            return cls(dimx, dimy)

        def get_dimx(self):
            return self._dimx
        def get_dimy(self):
            return self._dimy

        dimx = property(get_dimx, doc="Board dimension x.")
        dimy = property(get_dimy, doc="Board dimension y.")


    class GameUpdate(object):
        ''' A board state update. '''

        def __init__(self, munchers, nodes, edges):
            self._munchers = munchers
            self._nodes = nodes
            self._edges = edges

        @classmethod
        def from_dom(cls, dom):
            ''' Create a GameUpdate from an xml dom. '''
            munchers = eval(xml_get_ele_val_str(dom, 'Munchers'))
            live_nodes = eval(xml_get_ele_val_str(dom, 'LiveNodes'))
            dead_nodes = eval(xml_get_ele_val_str(dom, 'DeadNodes'))
            edges = xml_get_ele_val_str(dom, 'Edges')
            return cls(munchers, live_nodes, dead_nodes, edges)

        def get_munchers(self):
            return self._munchers
        def get_live_nodes(self):
            return self._live_nodes
        def get_dead_nodes(self):
            return self._dead_nodes
        def get_edges(self):
            return self._edges

        munchers = property(get_munchers, doc="Munchers currently on the board")
        live_nodes = property(get_live_nodes, doc="Food remaining on the board")
        dead_nodes = property(get_dead_nodes, doc="Food that has been removed from the board")
        edges = property(get_nodes, doc="Edges between nodes")

    def __init__(self, setup_params):
        ''' Setup the game visualization plot. '''
        self._root = tk.Tk()
        self._root.title('NanoMunchers')
        self._setup_params = setup_params
        self._boardPts = [(0.,0.), (setup_params.dimx,0.),
                          (setup_params.dimx,setup_params.dimy),
                          (0.,setup_params.dimy), (0., 0.)]
        self._vo_x = 0.05 * setup_params.dimx
        self._vo_y = 0.05 * setup_params.dimy

        self._canvas = tk.Canvas(self._root,
                                 width=self._setup_params.dimx + 2*self._vo_x,
                                 height=self._setup_params.dimy + 2*self._vo_y,
                                 bg='black')
        self._canvas.pack()
        self._draw_board()
        self._canvas.update()

    def _draw_board(self):
        EDGE_WIDTH = 2
        mins = (self._vo_x - EDGE_WIDTH, self._vo_y - EDGE_WIDTH)
        maxs = (self._vo_x + self._setup_params.dimx + EDGE_WIDTH,
                self._vo_y + self._setup_params.dimy + EDGE_WIDTH)
        self._canvas.create_rectangle(mins, maxs,
                                      outline='white', width=EDGE_WIDTH)

    def redraw(self):
        ''' Draw the canvas again. '''
        self._canvas.update()

    def update(self, game_update):
        '''
        Update the game visualization from the GameUpdate data using
        canvas blit.
        '''
        self._canvas.delete(tk.ALL)
        for edge in edges
          self._canvas.create_line(edge[0][0], edge[0][1],
                                   edge[1][0], edge[1][1],
                                   dash=2, fill='black')
        for node in live_nodes
          self._canvas.create_oval(self._vo_x + node[0] - 4,
                                   self._vo_y + node[1] - 4,
                                   self._vo_x + node[0] + 4,
                                   self._vo_y + node[1] + 4,
                                   stipple='gray50', width=0, fill='green')

        for node in dead_nodes
          self._canvas.create_oval(self._vo_x + node[0] - 4,
                                   self._vo_y + node[1] - 4,
                                   self._vo_x + node[0] + 4,
                                   self._vo_y + node[1] + 4,
                                   stipple='gray50', width=0, fill='gray')

        for muncher in munchers
          self._canvas.create_oval(self._vo_x + muncher[0] - 1,
                                   self._vo_y + muncher[1] - 1,
                                   self._vo_x + muncher[0] + 1,
                                   self._vo_y + muncher[1] + 1,
                                   width=0, fill='red')
        self._draw_board()
        self._canvas.update()


def main():
    # Read the setup parameters from stdin and create setup class.
    setup_xml_str = read_stdin()
    setup_doc = xmlminidom.parseString(setup_xml_str)
    setup_dom = xml_get_ele_dom(setup_doc, 'NanoVis.SetupParams')
    vis_setup_params = NanoVis.SetupParams.from_dom(setup_dom)
    vis = NanoVis(vis_setup_params)
    # Read input and update visualization until the pipe closes.
    while True:
        line = read_stdin()
        if line is None:
            break
        else:
            try:
                update_doc = xmlminidom.parseString(line)
                upd_dom = xml_get_ele_dom(update_doc, 'NanoVis.GameUpdate')
                update = NanoVis.GameUpdate.from_dom(upd_dom)
                vis.update(update)
            except:
                if len(line) is not 0 and line is not None:
                    print "Failed parsing game update."
                    print "Update string:", line
                    raise
                break
    # Hold the view.
    t_start = time.time()
    t_now = time.time()
    while (t_now - t_start) < 1.0:
        vis.redraw()
        t_now = time.time()
        time.sleep(0.032)


if __name__ == "__main__":
    main()

