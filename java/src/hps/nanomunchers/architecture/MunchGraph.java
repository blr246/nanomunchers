package hps.nanomunchers.architecture;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MunchGraph 
{
	public List<Vertex> vertices;
	public List<Edge> edges;
	public MunchGraph()
	{
		vertices = new ArrayList<Vertex>();
		edges = new ArrayList<Edge>();
	}
	
	public Map<Integer,List<Integer>> getEdgeMap()
	{
		Map<Integer, List<Integer>> edgeMap = new HashMap<Integer, List<Integer>>();
		for(int i=0;i<edges.size();++i)
		{
			Edge edge = edges.get(i);
			if(edgeMap.get(edge.sourceNodeId) != null)
			{
				edgeMap.get(edge.sourceNodeId).add(edge.sinkNodeInd);
			}
			else
			{
				List<Integer> sinkNodes = new ArrayList<Integer>();
				sinkNodes.add(edge.sinkNodeInd);
				edgeMap.put(edge.sourceNodeId, sinkNodes);
			}
		}
		
		return edgeMap;
	}
}
