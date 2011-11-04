package hps.nanomunchers.test;

import static org.junit.Assert.*;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.junit.Test;

import hps.nanomunchers.architecture.INanoMuncherIO;
import hps.nanomunchers.architecture.Instructions;
import hps.nanomunchers.architecture.MunchGraph;
import hps.nanomunchers.architecture.NanoMuncherIO;
import hps.nanomunchers.architecture.Point;
import hps.nanomunchers.architecture.Vertex;
import hps.nanomunchers.architecture.MuncherPresenter;;

public class NanoMuncherIOTest {

	@Test
	public void testReadInput() 
	{
		String filename = "src/hps/nanomunchers/test/inputsample.txt";
		int numVertices = 127;
		int numEdges = 131;
		NanoMuncherIO nmio = new NanoMuncherIO();
		MunchGraph graph = nmio.readInput(filename);
		
		/* Sanity checks */
		assertNotNull(graph);
		
		/* Read right number of vertices? */
		assertEquals(numVertices, graph.vertices.size());
		
		/* Read right number of edges? */
		assertEquals(numEdges,graph.edges.size());
		
		/* Test an element */
		Vertex v = graph.vertices.get(10);
		int nodeid = 10;
		int x = 9;
		int y=9;
		assertEquals(nodeid, v.getNodeId());
		assertEquals(x, v.getLocation().getX());
		assertEquals(y, v.getLocation().getY());
		
		/* Test last Element */
		v = graph.vertices.get(graph.vertices.size()-1);
		nodeid = 126;
		x = 16;
		y = 6;
		assertEquals(nodeid, v.getNodeId());
		assertEquals(x, v.getLocation().getX());
		assertEquals(y, v.getLocation().getY());
	}
	
	@Test
	public void testSerialize()
	{
		List<MuncherPresenter> nmunchPresenters = new ArrayList<MuncherPresenter>();
		
		nmunchPresenters.add(new MuncherPresenter(0, new Point(7,3), new Instructions("LURD")));
		nmunchPresenters.add(new MuncherPresenter(12, new Point(17,30), new Instructions("RULD")));
		
		INanoMuncherIO nmIo = new NanoMuncherIO();
		String actual = nmIo.serialize(nmunchPresenters);
		String expected = "2\n0 7 3 LURD\n12 17 30 RULD\n";
		assertEquals(expected, actual);
		
	}

}
