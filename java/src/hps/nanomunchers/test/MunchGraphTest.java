package hps.nanomunchers.test;

import static org.junit.Assert.*;
import java.util.List;
import java.util.Map;

import hps.nanomunchers.architecture.MunchGraph;
import hps.nanomunchers.architecture.NanoMuncherIO;

import org.junit.Test;

public class MunchGraphTest {

	@Test
	public void testGetEdgeMap() 
	{
		String filename = "src/hps/nanomunchers/test/inputsample.txt";
		NanoMuncherIO nmio = new NanoMuncherIO();
		MunchGraph graph = nmio.readInput(filename);
		Map<Integer,List<Integer>> edgeMap = graph.getEdgeMap();
		int numEdges = 78;
		/* sanity check */
		assertNotNull(edgeMap);
		assertEquals(numEdges, edgeMap.size());
		
		int key = 65;
		List<Integer> neighbours = edgeMap.get(65);
		assertNotNull(neighbours);
		assertEquals(3,neighbours.size());
		int value0 = neighbours.get(0);
		int value1 = neighbours.get(1);
		int value2 = neighbours.get(2);
		
		assertEquals(79,value0);
		assertEquals(102,value1);
		assertEquals(115,value2);
		
		int[] keys  = {0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,
						16,17,18,19,20,22,23,25,27,28,
						29,30,31,32,33,34,35,36,37,38};
		
		for(int i=0;i<keys.length;++i)
		{
			System.out.println(keys[i]);
			assertNotNull(edgeMap.get(keys[i]));
		}
		
		
	}

}
