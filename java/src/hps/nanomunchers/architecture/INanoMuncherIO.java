package hps.nanomunchers.architecture;

import java.util.List;

public interface INanoMuncherIO 
{
	String serialize(List<MuncherPresenter> nanoMuncherRepresenters);
	List<MuncherPresenter> deserialize(String input);
	MunchGraph readInput(String filename);
}
