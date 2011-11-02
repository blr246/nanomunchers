public class Point 
{
	private int x;
	private int y;
	
	@Override
	public String toString() {
		return "(" + x + "," + y + ")";
	}
	public int getX() {
		return x;
	}
	public void setX(int x) {
		this.x = x;
	}
	public int getY() {
		return y;
	}
	public void setY(int y) {
		this.y = y;
	}
}
