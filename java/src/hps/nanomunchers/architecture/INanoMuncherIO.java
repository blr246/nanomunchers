package hps.nanomunchers.architecture;

import java.util.List;
import java.util.Map;

public interface INanoMuncherIO 
{
	String serialize(List<MuncherPresenter> nanoMuncherRepresenters);
	List<MuncherPresenter> deserialize(String input);
	MunchGraph readInput(String filename);
}
