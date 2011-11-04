package hps.nanomunchers.architecture;

public class Vertex 
{
	private int m_nodeId;
	private Point m_location;
	
	public Vertex()
	{}
	
	public Vertex(int nodeId, Point location)
	{
		this.m_nodeId = nodeId;
		this.m_location = location;
	}
	
	public int getNodeId() {
		return m_nodeId;
	}
	public void setNodeId(int nodeId) {
		this.m_nodeId = nodeId;
	}
	public Point getLocation() {
		return m_location;
	}
	public void setLocation(Point location) {
		this.m_location = location;
	}
}
