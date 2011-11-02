package hps.nanomunchers.architecture;

import java.util.List;

public class Instructions 
{
	private List<String> instructions;

	public List<String> getInstructions() {
		return instructions;
	}

	public void setInstcructions(List<String> instructions) {
		this.instructions = instructions;
	}
	
	public void addInstruction(String instruction)
	{
		assert(instructions.size() < Common.MAX_INSTRUCTION_SIZE) : "Instruction set already has 4 instructions";
		// also assert to check if there are more than two repetitive instructions.
		instructions.add(instruction);
	}

	@Override
	public String toString() 
	{
		String retVal = "(";
		for (int i=0;i<instructions.size();++i)
		{
			retVal += instructions.get(i) + ",";
		}
		retVal += instructions.size()-1 + ")";
		
		return retVal;
	}

}
