package hps.nanomunchers.architecture;

import java.util.List;

public interface INanoMuncherIO 
{
	void serialize(List<NanoMuncherRepresenter> nanoMuncherRepresenters);
	List<NanoMuncherRepresenter> deserialize(String input);
	List<MunchGraph> readInput(String filename);
}
