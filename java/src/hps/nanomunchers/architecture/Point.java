package hps.nanomunchers.architecture;

public class Point 
{
	private int m_x;
	private int m_y;
	
	public Point()
	{}
	
	public Point(int xLoc, int yLoc)
	{
		this.m_x = xLoc;
		this.m_y = yLoc;
	}
	
	@Override
	public String toString() {
		return m_x + " " + m_y;
	}
	public int getX() {
		return m_x;
	}
	public void setX(int x) {
		assert(x >= Common.BOARD_XMIN && x <= Common.BOARD_XMAX): "Cannot drop a Nano muncher to the left or right of the board.";
		this.m_x = x;
	}
	public int getY() {
		return m_y;
	}
	public void setY(int y) {
		assert(y >= Common.BOARD_YMIN && y <= Common.BOARD_YMAX): "Cannot drop a Nano muncher above or below the board.";
		this.m_y = y;
	}
}
