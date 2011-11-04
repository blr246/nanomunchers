package hps.nanomunchers.architecture;

import java.util.HashSet;

public class MuncherPresenter 
{
	
	private int m_time;
	private Point m_location;
	private Instructions m_instructions;
	
	public MuncherPresenter()
	{}
	
	public MuncherPresenter(int time, Point location, Instructions instructions)
	{
		this.m_time = time;
		this.m_location = location;
		this.m_instructions = instructions;
	}
	
	public int getTime() {
		return m_time;
	}
	public void setTime(int time) {
		this.m_time = time;
	}
	public Point getLocation() {
		return m_location;
	}
	public void setLocation(Point location) {
		this.m_location = location;
	}
	
	public Instructions getInstructions() {
		return m_instructions;
	}
	
	public void setInstructions(Instructions instructions) {
		assert(instructions.Size() == 4):"Instruction set can only be 4 instruction long.";
		assert(allDistinct(instructions)):"Your instruction set: " + instructions.toString() + ", contains duplicate elements";
		assert(isValidInstructionSet(instructions)):"Instruction must be a permutation of L U R D, your set: " + instructions.toString();
		this.m_instructions = instructions;
	}
	
	public void addInstruction(String instruction)
	{
		this.m_instructions.addInstruction(instruction);
	}
	
	@Override
	public String toString() {
		return m_time + " " + m_location.toString()
				+ " " + m_instructions.toString();
	}
	
	private boolean allDistinct(Instructions instructions) 
	{
		HashSet<String> nonDups = new HashSet<String>(instructions.getInstructions());
		return (nonDups.size() == instructions.Size());
	}
	
	private boolean isValidInstructionSet(Instructions instructions) 
	{
		String program = instructions.toString();
		return program.contains("L") || program.contains("U") || program.contains("R") || program.contains("D");
	}
	
}

