package hps.nanomunchers.architecture;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.List;
import java.util.Scanner;

public class NanoMuncherIO implements INanoMuncherIO
{

	@Override
	public String serialize(List<MuncherPresenter> nanoMuncherRepresenters)
	{
		assert(nanoMuncherRepresenters != null) : "MunchPresenters are null";
		StringBuffer sb = new StringBuffer();
		sb.append(Integer.toString(nanoMuncherRepresenters.size()) + "\n");
		for(int i = 0;i<nanoMuncherRepresenters.size();++i)
		{
			sb.append(nanoMuncherRepresenters.get(i).toString() + "\n");
		}
		
		return sb.toString();
	}

	@Override
	public List<MuncherPresenter> deserialize(String input) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public MunchGraph readInput(String filename) 
	{
		MunchGraph graph = new MunchGraph();
		try 
		{
			FileReader reader = new FileReader(filename);
			Scanner sc = new Scanner(reader);
			sc.next();
			while(sc.hasNext())
			{
				String next = sc.next();
				if(next.contains("nodeid1"))
				{
					break;
				}
				Vertex v = new Vertex();
				createVertex(next,v);
				graph.vertices.add(v);
			}
			while(sc.hasNext())
			{
				Edge edge = new Edge();
				createEdges(sc.next(),edge);
				graph.edges.add(edge);
			}
		} 
		catch (FileNotFoundException e) 
		{
			e.printStackTrace();
		}
		return graph;
	}

	private void createEdges(String next, Edge outEdge)
	{
		Scanner sc = new Scanner(next);
		sc.useDelimiter(",");
		int nodeid1 = sc.nextInt();
		int nodeid2 = sc.nextInt();
		outEdge.sourceNodeId = nodeid1;
		outEdge.sinkNodeInd = nodeid2;
		
	}

	private void createVertex(String next, Vertex outVertex) 
	{
		Scanner sc = new Scanner(next);
		sc.useDelimiter(",");
		int nodeid = sc.nextInt();
		int xLoc = sc.nextInt();
		int yLoc = sc.nextInt();
		outVertex.setNodeId(nodeid);
		outVertex.setLocation(new Point(xLoc,yLoc));
	}

}
