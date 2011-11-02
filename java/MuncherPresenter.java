public class MuncherPresenter 
{
	private int nanoMuncherId;
	private int time;
	private Point location;
	private Instructions instructions;
	
	
	public int getNanoMuncherId() {
		return nanoMuncherId;
	}
	public void setNanoMuncherId(int nanoMuncherId) {
		this.nanoMuncherId = nanoMuncherId;
	}
	public int getTime() {
		return time;
	}
	public void setTime(int time) {
		this.time = time;
	}
	public Point getLocation() {
		return location;
	}
	public void setLocation(Point location) {
		this.location = location;
	}
	
	public Instructions getInstructions() {
		return instructions;
	}
	public void setInstructions(Instructions instructions) {
		this.instructions = instructions;
	}
	
	@Override
	public String toString() {
		return "(" + nanoMuncherId
				+ "," + time + "," + location.toString()
				+ "," + instructions.toString() + "]";
	}

}
