package hps.nanomunchers.architecture;

import java.util.ArrayList;
import java.util.List;

public class Instructions 
{
	private List<String> m_instructions;

	public Instructions()
	{}
	
	public Instructions(String instructions)
	{
		this.m_instructions = new ArrayList<String>();
		init(instructions);
	}
	
	private void init(String instructions)
	{
		for (int i=0;i<instructions.length();++i)
		{
			m_instructions.add(Character.toString(instructions.charAt(i)));
		}
	}
	
	public List<String> getInstructions() {
		return m_instructions;
	}

	public void setInstcructions(List<String> instructions) {
		this.m_instructions = instructions;
	}
	
	public void addInstruction(String instruction)
	{
		assert(m_instructions.size() < Common.MAX_INSTRUCTION_SIZE) : "Instruction set already has 4 instructions";
		// also assert to check if there are more than two repetitive instructions.
		m_instructions.add(instruction);
	}

	public int Size()
	{
		return m_instructions.size();
	}
	
	@Override
	public String toString() 
	{
		String retVal = "";
		for (int i=0;i<m_instructions.size();++i)
		{
			retVal += m_instructions.get(i);
		}
		
		return retVal;
	}

}
