package hps.nanomunchers.architecture;

import java.util.ArrayList;
import java.util.List;

public class MunchGraph 
{
	public List<Vertex> vertices;
	public List<Edge> edges;
	public MunchGraph()
	{
		vertices = new ArrayList<Vertex>();
		edges = new ArrayList<Edge>();
	}
}
