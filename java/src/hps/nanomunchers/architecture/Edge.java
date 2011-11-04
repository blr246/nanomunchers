package hps.nanomunchers.architecture;

public class Edge 
{
	public Edge()
	{}
	
	public Edge(int source, int sink)
	{
		this.sourceNodeId = source;
		this.sinkNodeInd = sink;
	}
	public int sourceNodeId;
	public int sinkNodeInd;
}
