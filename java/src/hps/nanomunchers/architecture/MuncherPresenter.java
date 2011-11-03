package hps.nanomunchers.architecture;

public class MuncherPresenter 
{
	private int time;
	private Point location;
	private Instructions instructions;
	
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
		return time + " " + location.toString()
				+ " " + instructions.toString();
	}

}
