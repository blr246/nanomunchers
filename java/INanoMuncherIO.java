import java.util.List;

public interface INanoMuncherIO 
{
	void serialize(List<MuncherPresenter> nanoMuncherRepresenters);
	List<MuncherPresenter> deserialize(String input);
	List<MunchGraph> readInput(String filename);
}
